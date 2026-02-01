import os
from playwright.sync_api import sync_playwright

def verify_converter():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the local HTML file
        file_path = os.path.abspath("maritime_calc/www/index.html")
        page.goto(f"file://{file_path}")

        # Click on the 'Convertisseur' tab
        page.click("text=Convertisseur")

        # Wait for tab content to be visible
        page.wait_for_selector("#converter.active")

        # Fill in the form
        # Volume: 1000
        page.fill("#converter #initialVolume", "1000")
        # Temp: 25
        page.fill("#converter #temperature", "25")
        # Density: 0.850
        page.fill("#converter #density15", "0.850")

        # Click Calculate - being specific to the converter tab
        page.click("#converter button.action-btn")

        # Wait for result
        page.wait_for_selector("#resultConverter", state="visible")

        # Take screenshot
        screenshot_path = os.path.abspath("verification/converter_result.png")
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    verify_converter()
