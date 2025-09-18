from .base_scraper import BaseScraper
import re

class EbayScraper(BaseScraper):
    def __init__(self):
        super().__init__("ebay")

    def scrape_product(self, url: str):
        print(f"Scraping eBay URL: {url}")

        # Possible selectors for price
        price_selectors = [
            'span[itemprop="price"]',
            'span#prcIsum',
            'span#mm-saleDscPrc',
            'span#prcIsum_bidPrice'
        ]

        # Possible selectors for product name
        name_selectors = [
            'h1[itemprop="name"]',
            'h1#itemTitle',
            'h1[class*="x-item-title"]'
        ]

        price_text = None
        name_text = None

        # Try different selectors
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

        # Clean price (e.g., US $1,234.56 → 1234.56)
        try:
            price_match = re.search(r'[\d,]+\.\d{2}', price_text)
            if price_match:
                price = float(price_match.group().replace(",", ""))
            else:
                raise ValueError("Price format not recognized")
        except (AttributeError, ValueError) as e:
            print(f"⚠️ Could not convert price '{price_text}' to number. Error: {e}")
            return

        product_name = name_text.replace("Details about  \xa0", "").strip()

        # Save to DB
        self.save_to_db(product_name, price, url)
        print(f"✅ Saved: {product_name} - ${price}")

    def close_scraper(self):
        self.close()


# Example usage
if __name__ == "__main__":
    scraper = EbayScraper()
    test_url = "https://www.ebay.com/itm/EXAMPLEITEM"
    scraper.scrape_product(test_url)
    scraper.close_scraper()
