from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError

# Load environment variables from .env file
load_dotenv()

# Create connection URL from environment variables
DB_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

engine = create_engine(DB_URL, echo=True)  # echo=True for SQL debug logs
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ProductPrice(Base):
    __tablename__ = "product_prices"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    website = Column(String, nullable=False)  # e.g., 'amazon', 'walmart'
    product_url = Column(String, unique=True)  # Important for tracking same product
    timestamp = Column(DateTime, default=datetime.utcnow)
    # You can add more fields like stock status, rating, etc.

# Run this only when executing the file directly
if __name__ == "__main__":
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully!")
    except OperationalError as e:
        print("❌ Database connection failed. Make sure the database exists.")
        print(f"Error: {e}")
