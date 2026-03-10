import re
import time
import logging
import threading
from datetime import datetime

from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)

PAGE_URL = (
    "https://mercyrelief.org.uk/en/fundraising/"
    "university-of-birmingham-isoc/1000105-ubisoc-gaza-appeal"
)
SCRAPE_INTERVAL_SECONDS = 30

_state = {
    "current_total": None,
    "last_updated": None,
    "last_error": None,
    "donors": [],
}
_state_lock = threading.Lock()


def parse_amount(text: str) -> float:
    cleaned = re.sub(r"[£,\s]", "", text.strip())
    return float(cleaned)


def scrape_once() -> dict:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(PAGE_URL, wait_until="domcontentloaded", timeout=30000)

            # Wait for the total to populate
            page.wait_for_function(
                """() => {
                    const h3 = document.querySelector('n3o-crowdfunder-progress h3');
                    return h3 && h3.innerText.includes('£');
                }""",
                timeout=25000,
            )

            # --- Scrape total ---
            h3_text = page.inner_text("n3o-crowdfunder-progress h3")
            total = parse_amount(h3_text)

            # --- Scrape last 5 donors ---
            donors = []
            items = page.query_selector_all(".fcauseDonors__item")
            for item in items[:5]:
                name_el = item.query_selector(".fcauseDonors__item-name h6")
                name = name_el.inner_text().strip() if name_el else "Anonymous"

                amount_el = item.query_selector(".fcauseDonors__item-info h6")
                try:
                    amount = parse_amount(amount_el.inner_text()) if amount_el else None
                except ValueError:
                    amount = None

                time_el = item.query_selector(".fcauseDonors__item-info p")
                time_ago = time_el.inner_text().strip() if time_el else ""

                msg_el = item.query_selector(".fcauseDonors__item-text p")
                message = msg_el.inner_text().strip() if msg_el else None

                donors.append({
                    "name": name,
                    "amount": amount,
                    "time_ago": time_ago,
                    "message": message,
                })

            return {"total": total, "donors": donors}
        finally:
            browser.close()


def get_state() -> dict:
    with _state_lock:
        return dict(_state)


def _scraper_loop():
    while True:
        try:
            result = scrape_once()
            now = datetime.utcnow()
            with _state_lock:
                _state["current_total"] = result["total"]
                _state["donors"] = result["donors"]
                _state["last_updated"] = now
                _state["last_error"] = None
            print(f"[{now.strftime('%H:%M:%S')}] Scraped total: £{result['total']:,.2f} | {len(result['donors'])} donors")

        except Exception as exc:
            timestamp = datetime.utcnow().strftime("%H:%M:%S")
            error_msg = str(exc)
            with _state_lock:
                _state["last_error"] = error_msg
            print(f"[{timestamp}] Scrape failed (keeping previous value): {error_msg}")
            logger.error("Scrape error: %s", error_msg)

        time.sleep(SCRAPE_INTERVAL_SECONDS)


def start_background_scraper():
    thread = threading.Thread(target=_scraper_loop, daemon=True)
    thread.start()
    logger.info("Background scraper started (interval: %ds)", SCRAPE_INTERVAL_SECONDS)
    return thread