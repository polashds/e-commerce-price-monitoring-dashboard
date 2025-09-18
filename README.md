# e-commerce-price-monitoring-dashboard

# Real-Time E-Commerce Price Monitoring System

A scalable, automated system that tracks product prices across major retailers, stores the data in a cloud database, and displays it on an interactive dashboard.

## Features
- **Scrapers:** Custom-built for Walmart, Amazon, and eBay using Selenium and Scrapy.
- **Robustness:** Built-in retry logic, proxy rotation, and anti-detection measures.
- **Database:** Cloud-hosted PostgreSQL instance for reliable data storage.
- **Dashboard:** Interactive Plotly Dash web app with real-time price history charts.
- **Scheduling:** Fully automated, runs hourly without manual intervention.

## Architecture
![Architecture Diagram](https://via.placeholder.com/500x300?text=System+Architecture+Diagram) 
*(You can create a simple diagram on draw.io)*

## For Developers: Adding a New Product
1.  Add the product URL to the appropriate list in `run_scraper.py`.
2.  The system will automatically begin tracking it on the next scheduled run.

## Maintenance
*Websites change their layout frequently. If a scraper breaks:*
1.  The system will log errors.
2.  You will be notified.
3.  The CSS selectors in the relevant scraper file (`scrapers/amazon_scraper.py`) will need to be updated.

## Links
- **Live Dashboard:** [https://your-dashboard-name.onrender.com](https://your-dashboard-name.onrender.com)
- **Support:** Contact [Your Name] at [your.email@domain.com] for any issues.