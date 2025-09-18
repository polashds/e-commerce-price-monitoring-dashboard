from .base_scraper import BaseScraper
import re

class WalmartScraper(BaseScraper):
    def __init__(self):
        super().__init__("walmart")

    def scrape_product(self, url: str):
        print(f"Scraping Walmart URL: {url}")

        # Try different selectors for price
        price_selectors = [
            'span[itemprop="price"]',
            'span[data-automation="buybox-price"]',
            'span[class*="price-characteristic"]'
        ]

        # Try different selectors for product name
        name_selectors = [
            'h1[itemprop="name"]',
            'h1[class*="prod-ProductTitle"]',
            'h1[data-automation="product-title"]'
        ]

        price_text = None
        name_text = None

        # Loop through selectors until one works
        for selector in price_selectors:
            price_text = self._scrape_with_selenium(url, selector)
            if price_text:
                break

        for selector in name_selectors:
            name_text = self._scrape_with_selenium(url, selector)
            if name_text:
                break

        if not price_text or not name_text:
            print("❌ Failed to find product name or price.")
            return

        # Clean the price text (e.g., "$123.45" → 123.45)
        try:
            price_match = re.search(r'[\d,]+\.\d{2}', price_text)  # e.g., 1,234.56
            if price_match:
                price = float(price_match.group().replace(",", ""))
            else:
                raise ValueError("Price format not recognized")
        except (AttributeError, ValueError) as e:
            print(f"⚠️ Could not convert price '{price_text}' to number. Error: {e}")
            return

        product_name = name_text.strip()

        # Save the data
        self.save_to_db(product_name, price, url)
        print(f"✅ Saved: {product_name} - ${price}")

    def close_scraper(self):
        """Call this manually after multiple scrapes."""
        self.close()


# Example usage
if __name__ == "__main__":
    scraper = WalmartScraper()
    test_url = "https://www.walmart.com/ip/Example-Product/123456789"
    scraper.scrape_product(test_url)
    scraper.close_scraper()
