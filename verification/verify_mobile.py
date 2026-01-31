from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # Simulate mobile viewport
        page = browser.new_page(viewport={"width": 375, "height": 800})

        # Load file
        file_path = f"file://{os.getcwd()}/calcul chargement 2.html"
        print(f"Loading {file_path}")
        page.goto(file_path)

        # 1. Config Tab (Active by default)
        print("Verifying Estimation Box...")
        est_box = page.locator(".estimation-box")
        est_box.scroll_into_view_if_needed()
        est_box.screenshot(path="verification/mobile_estimation.png")

        # 2. Loading Tab
        print("Verifying Loading Tab...")
        page.click("button[onclick=\"openTab(event, 'loading')\"]")
        page.wait_for_timeout(500) # Wait for fade

        # Screenshot the loading row
        loading_row = page.locator(".load-prod-row").first
        loading_row.scroll_into_view_if_needed()
        loading_row.screenshot(path="verification/mobile_loading.png")

        # 3. Unloading Tab
        print("Verifying Unloading Tab...")
        page.click("button[onclick=\"openTab(event, 'unloading')\"]")
        page.wait_for_timeout(500)

        tank_row = page.locator(".shore-tank-row").first
        tank_row.scroll_into_view_if_needed()
        tank_row.screenshot(path="verification/mobile_unloading.png")

        # Full page
        page.screenshot(path="verification/mobile_full_view.png", full_page=True)

        browser.close()

if __name__ == "__main__":
    run()
