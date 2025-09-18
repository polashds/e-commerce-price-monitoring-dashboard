# import random
# from datetime import datetime, timedelta
# from database.models import SessionLocal, ProductPrice

# def seed_price_history():
#     session = SessionLocal()
#     now = datetime.utcnow()

#     # Config for each site: (product_name, base_price, url)
#     sites = [
#         ("Walmart Sample Product", 19.99, "https://walmart.com/test1", "walmart"),
#         ("Amazon Sample Product", 29.99, "https://amazon.com/test2", "amazon"),
#         ("eBay Sample Product", 9.99, "https://ebay.com/test3", "ebay"),
#     ]

#     for product_name, base_price, url, site in sites:
#         for i in range(100):  # 100 fake data points
#             # Small random fluctuation around base price
#             price = round(base_price + random.uniform(-2, 2), 2)

#             entry = ProductPrice(
#                 product_name=product_name,
#                 price=price,
#                 website=site,
#                 product_url=url,
#                 timestamp=now - timedelta(hours=(100 - i))  # oldest → newest
#             )
#             session.add(entry)

#     session.commit()
#     session.close()
#     print("✅ Seeded 100 fake price points per site (Walmart, Amazon, eBay)")

# if __name__ == "__main__":
#     seed_price_history()


import random
from datetime import datetime, timedelta
from database.models import SessionLocal, ProductPrice

def seed_price_history():
    session = SessionLocal()
    now = datetime.utcnow()

    # Config for each site: (product_name, base_price, base_url, site)
    sites = [
        ("Walmart Sample Product", 19.99, "https://walmart.com/test1", "walmart"),
        ("Amazon Sample Product", 29.99, "https://amazon.com/test2", "amazon"),
        ("eBay Sample Product", 9.99, "https://ebay.com/test3", "ebay"),
    ]

    for product_name, base_price, base_url, site in sites:
        for i in range(100):  # 100 fake data points
            # Small random fluctuation around base price
            price = round(base_price + random.uniform(-2, 2), 2)

            entry = ProductPrice(
                product_name=product_name,
                price=price,
                website=site,
                # 👇 Make URL unique for each row
                product_url=f"{base_url}?t={i}",
                timestamp=now - timedelta(hours=(100 - i))  # oldest → newest
            )
            session.add(entry)

    session.commit()
    session.close()
    print("✅ Seeded 100 fake price points per site (Walmart, Amazon, eBay)")

if __name__ == "__main__":
    seed_price_history()
