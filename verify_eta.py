from playwright.sync_api import sync_playwright
import os
import re

def test_eta(page):
    # Get absolute path to the HTML file
    repo_path = os.getcwd()
    file_path = os.path.join(repo_path, "calcul chargement 2.html")
    url = f"file://{file_path}"

    print(f"Navigating to {url}")
    page.goto(url)

    # 1. Test "Estimation Rapide" ETA
    print("Clicking 'Estimation Rapide' tab")
    page.get_by_role("button", name="Estimation Rapide").click()

    print("Filling inputs for estimation")
    page.locator("#estVol").fill("24000") # 24000 m3
    page.locator("#estRate").fill("1000") # 1000 m3/h -> 24h

    print("Clicking Calculate")
    page.get_by_role("button", name="Calculer Durée").click()

    # Wait for result
    page.wait_for_selector("#resultEst", state="visible")

    est_text = page.locator("#estTime").inner_text()
    print(f"Estimation Result: {est_text}")

    assert "24h 0m" in est_text
    assert "Fin :" in est_text

    # 2. Test "Multi-Simultané" ETA
    print("Clicking 'Multi-Simultané' tab")
    page.get_by_role("button", name="Multi-Simultané").click()

    # Fill first row
    row1 = page.locator(".multi-row").nth(0)
    row1.locator(".m-name").fill("Tank A")
    row1.locator(".m-vol").fill("12000")
    row1.locator(".m-rate").fill("1000") # 12h

    print("Clicking Calculate for Multi")
    page.get_by_role("button", name="Calculer et Comparer").click()

    # Wait for result
    page.wait_for_selector("#resultMulti", state="visible")

    multi_results = page.locator("#resultMulti .result-item")
    first_res = multi_results.nth(0).inner_text()
    print(f"Multi Result: {first_res}")

    assert "Tank A" in first_res
    assert "12h 0m" in first_res
    assert "Fin :" in first_res

    # Take screenshot
    print("Taking screenshot")
    output_dir = "/home/jules/verification"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    page.screenshot(path=os.path.join(output_dir, "eta_result.png"), full_page=True)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_eta(page)
            print("Verification successful!")
        except Exception as e:
            print(f"Verification failed: {e}")
        finally:
            browser.close()
