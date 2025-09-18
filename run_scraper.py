# run_scraper.py
from scrapers.walmart_scraper import WalmartScraper
from scrapers.amazon_scraper import AmazonScraper
from scrapers.ebay_scraper import EbayScraper

# Central dictionary of product URLs
PRODUCT_URLS = {
    "walmart": [
        "https://www.walmart.com/ip/EXAMPLE1",
        "https://www.walmart.com/ip/EXAMPLE2",
    ],
    "amazon": [
        "https://www.amazon.com/dp/EXAMPLEASIN1",
        "https://www.amazon.com/dp/EXAMPLEASIN2",
    ],
    "ebay": [
        "https://www.ebay.com/itm/EXAMPLEITEM1",
        "https://www.ebay.com/itm/EXAMPLEITEM2",
    ],
}

# Map site name -> scraper class
SCRAPER_CLASSES = {
    "walmart": WalmartScraper,
    "amazon": AmazonScraper,
    "ebay": EbayScraper,
}

def main():
    print("🚀 Starting scraping run...")

    for site, urls in PRODUCT_URLS.items():
        print(f"\n🔎 Running scraper for: {site}")

        scraper_class = SCRAPER_CLASSES.get(site)
        if not scraper_class:
            print(f"⚠️ No scraper found for {site}, skipping...")
            continue

        scraper = scraper_class()
        for url in urls:
            try:
                scraper.scrape_product(url)
            except Exception as e:
                print(f"❌ Error scraping {url}: {e}")

        scraper.close_scraper()  # important cleanup

    print("\n✅ Scraping run finished.")

if __name__ == "__main__":
    main()
