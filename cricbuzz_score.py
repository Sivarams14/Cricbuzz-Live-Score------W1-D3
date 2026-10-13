
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from pathlib import Path

# Project folder
from pathlib import Path

OUTPUT_DIR = Path(r"C:\Users\sivar\Downloads\Gen AI SE\Week1\Day 3\Playwright Assignment")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

URL = "https://www.cricbuzz.com/"

# Selector verified in Chrome DevTools
MATCH_SELECTOR = 'a[href*="/live-cricket-scores/"]'

with sync_playwright() as p:

    print("Launching Chromium browser...")

    browser = p.chromium.launch(headless=False)

    page = browser.new_page(
        viewport={"width": 1440, "height": 900}
    )

    try:
        print("Opening Cricbuzz...")

        page.goto(
            URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        print("Waiting for cricket match cards...")

        page.locator(MATCH_SELECTOR).first.wait_for(
            state="visible",
            timeout=20000
        )

        # Wait until at least one detailed card is available
        page.wait_for_function(
            """selector => {
                const cards = [...document.querySelectorAll(selector)];
                return cards.some(card =>
                    card.innerText.trim().split('\\n').length >= 5
                );
            }""",
            arg=MATCH_SELECTOR,
            timeout=20000
        )

        # Extract all match cards
        cards = page.locator(MATCH_SELECTOR).all_inner_texts()

        # Keep only detailed match cards
        detailed_matches = [
            card.strip()
            for card in cards
            if len(card.strip().splitlines()) >= 5
        ]

        print(f"\nTotal detailed matches: {len(detailed_matches)}")

        for index, match in enumerate(detailed_matches, 1):
            print(f"\n===== MATCH {index} =====")
            print(match)

        # Save screenshot
        screenshot_path = OUTPUT_DIR / "score.png"

        page.screenshot(
            path=str(screenshot_path),
            full_page=True
        )

        print(f"\nScreenshot saved: {screenshot_path}")

    except PlaywrightTimeoutError:
        print("No detailed cricket match cards appeared within the timeout.")

    finally:
        browser.close()

print("\nAutomation completed!")
