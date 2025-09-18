from scrapers.walmart_scraper import WalmartScraper
from scrapers.amazon_scraper import AmazonScraper
from scrapers.ebay_scraper import EbayScraper
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def run_all():
    # Example test product URLs (replace with real ones as needed)
    walmart_url = "https://www.walmart.com/ip/123456789"
    amazon_url = "https://www.amazon.com/dp/B08N5WRWNW"
    ebay_url = "https://www.ebay.com/itm/1234567890"

    scrapers = [
        WalmartScraper(),
        AmazonScraper(),
        EbayScraper(),
    ]

    test_urls = [walmart_url, amazon_url, ebay_url]

    try:
        for scraper, url in zip(scrapers, test_urls):
            logger.info(f"Running scraper for {scraper.website_name} ...")
            scraper.scrape_product(url)
            scraper.close()

        logger.info("✅ All scrapers finished successfully!")

    except Exception as e:
        logger.error(f"⚠️ Error running scrapers: {e}")


if __name__ == "__main__":
    run_all()
