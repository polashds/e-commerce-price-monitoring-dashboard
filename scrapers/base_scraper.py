from sqlalchemy.orm import Session
from database.models import SessionLocal, ProductPrice
from utils.proxy_manager import get_proxy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from urllib.parse import urlparse
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import logging
import os


# =========================
# Logger Setup
# =========================
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# File handler (saves logs to logs/scraper.log)
os.makedirs("logs", exist_ok=True)
file_handler = logging.FileHandler("logs/scraper.log", mode="a", encoding="utf-8")
file_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Attach handlers (avoid duplicates if reloaded)
if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


# =========================
# Scraper Class
# =========================
class BaseScraper:
    def __init__(self, website_name):
        self.website_name = website_name
        self.driver = None
        self.session: Session = SessionLocal()
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        ]

    def _get_selenium_driver(self):
        """Helper to setup a Selenium WebDriver with stealth and proxy support."""
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        # Random User Agent
        chrome_options.add_argument(f"user-agent={random.choice(self.user_agents)}")

        # Proxy integration
        proxy_dict = get_proxy()
        if proxy_dict:
            http_proxy = proxy_dict.get("http", "").replace("http://", "")
            if http_proxy:
                chrome_options.add_argument(f"--proxy-server={http_proxy}")
                logger.info(f"Using proxy: {http_proxy}")

        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver

    @retry(
        stop=stop_after_attempt(3),  # Try 3 times
        wait=wait_exponential(multiplier=1, min=4, max=10),  # Wait: 4s, 8s, etc.
        retry=retry_if_exception_type(Exception),  # Retry on any error
    )
    def _scrape_with_selenium(self, url, css_selector, wait_time: int = 10):
        """Generic method to scrape text using Selenium with retries and WebDriverWait."""
        try:
            logger.info(f"Attempting to scrape: {url}")
            if not self.driver:
                self.driver = self._get_selenium_driver()

            self.driver.get(url)

            # Wait dynamically until element is visible
            element = WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector))
            )

            result = element.text.strip()
            logger.info(f"Successfully scraped: {result}")
            return result

        except Exception as e:
            logger.error(f"Attempt failed for {url}: {e}")
            self.close()  # Clean up broken driver
            self.driver = None  # Force new driver on retry
            raise e

    def save_to_db(self, product_name: str, price: float, product_url: str):
        """Insert or update scraped product data in the DB."""
        try:
            existing = (
                self.session.query(ProductPrice)
                .filter(ProductPrice.product_url == product_url)
                .first()
            )

            if existing:
                existing.price = price
                existing.timestamp = datetime.utcnow()
                self.session.commit()
                logger.info(f"Updated price for {product_name}")
            else:
                new_entry = ProductPrice(
                    product_name=product_name,
                    price=price,
                    website=self.website_name,
                    product_url=product_url,
                )
                self.session.add(new_entry)
                self.session.commit()
                logger.info(f"Data saved for {product_name}")

        except Exception as e:
            self.session.rollback()
            logger.error(f"Error saving to DB: {e}")

    def close(self):
        """Release Selenium driver and DB session."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                logger.warning(f"Error closing driver: {e}")
        self.session.close()
        logger.info("Scraper closed successfully.")
