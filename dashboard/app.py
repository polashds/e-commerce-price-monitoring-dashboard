import dash
from dash import dcc, html, Input, Output
import plotly.express as px
from database.models import SessionLocal, ProductPrice
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Price Monitor Dashboard"

# Layout
app.layout = html.Div([
    html.H1("📊 Real-Time Price Monitor", style={'textAlign': 'center', 'marginBottom': 30}),
    
    dcc.Dropdown(
        id='website-selector',
        options=[
            {'label': 'All', 'value': 'ALL'},
            {'label': 'Walmart', 'value': 'walmart'},
            {'label': 'Amazon', 'value': 'amazon'},
            {'label': 'eBay', 'value': 'ebay'},
        ],
        value='ALL',
        style={'width': '50%', 'margin': 'auto'}
    ),
    
    dcc.Graph(id='price-history-graph', style={'height': '600px'}),
    
    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # Update every 1 minute
        n_intervals=0
    )
], style={'padding': '20px'})

# Callback to update graph
@app.callback(
    Output('price-history-graph', 'figure'),
    Input('website-selector', 'value'),
    Input('interval-component', 'n_intervals')
)
def update_graph(selected_website, n):
    session = SessionLocal()
    try:
        # Query database
        if selected_website == 'ALL':
            results = session.query(ProductPrice).all()
        else:
            results = (
                session.query(ProductPrice)
                .filter(ProductPrice.website == selected_website)
                .all()
            )

        # Convert to DataFrame
        df = pd.DataFrame([{
            'Product': r.product_name,
            'Price': r.price,
            'Website': r.website,
            'Timestamp': r.timestamp
        } for r in results])

        if df.empty:
            return px.scatter(title="⚠️ No Data Available Yet")

        # Ensure time ordering
        df = df.sort_values(by="Timestamp")

        # Create chart
        fig = px.line(
            df,
            x="Timestamp",
            y="Price",
            color="Product",
            line_dash="Website",
            title=f"Price History ({selected_website})",
            labels={"Price": "Price ($)", "Timestamp": "Date"},
        )
        fig.update_layout(legend_title="Product")
        return fig

    finally:
        session.close()


if __name__ == "__main__":
    app.run(debug=True)
