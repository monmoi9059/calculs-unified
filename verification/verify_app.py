from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8080")
        page.wait_for_selector("body")
        # Check title
        title = page.title()
        print(f"Page title: {title}")

        # Take screenshot of the main config tab
        page.screenshot(path="verification/app_preview.png")

        # Click on 'Chargement' tab
        page.click("text=Chargement")
        page.wait_for_timeout(500) # Wait for animation
        page.screenshot(path="verification/app_loading_tab.png")

        browser.close()

if __name__ == "__main__":
    run()
