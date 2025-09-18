from database.models import SessionLocal, ProductPrice
from datetime import datetime

def seed_test_data():
    session = SessionLocal()

    test_data = [
        ProductPrice(
            product_name="Walmart Sample Product",
            price=19.99,
            website="walmart",
            product_url="https://www.walmart.com/ip/test123",
            timestamp=datetime.utcnow()
        ),
        ProductPrice(
            product_name="Amazon Sample Product",
            price=29.99,
            website="amazon",
            product_url="https://www.amazon.com/dp/test456",
            timestamp=datetime.utcnow()
        ),
        ProductPrice(
            product_name="eBay Sample Product",
            price=9.99,
            website="ebay",
            product_url="https://www.ebay.com/itm/test789",
            timestamp=datetime.utcnow()
        ),
    ]

    try:
        session.add_all(test_data)
        session.commit()
        print("✅ Sample data inserted successfully!")
    except Exception as e:
        session.rollback()
        print(f"⚠️ Error inserting data: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed_test_data()
