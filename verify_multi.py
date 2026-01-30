from playwright.sync_api import sync_playwright
import os

def test_multi_simultaneous(page):
    # Get absolute path to the HTML file
    repo_path = os.getcwd()
    file_path = os.path.join(repo_path, "calcul chargement 2.html")
    url = f"file://{file_path}"

    print(f"Navigating to {url}")
    page.goto(url)

    # Click on the "Multi-Simultané" tab
    print("Clicking 'Multi-Simultané' tab")
    page.get_by_role("button", name="Multi-Simultané").click()

    # The first row should be present by default
    print("Filling first row (Tank 1)")
    row1 = page.locator(".multi-row").nth(0)
    row1.locator(".m-name").fill("Tank 1 (Diesel)")
    row1.locator(".m-vol").fill("10000") # 10000 m3
    row1.locator(".m-rate").fill("1000") # 1000 m3/h -> 10h

    # Add a second row
    print("Adding second row")
    page.get_by_role("button", name="+ Ajouter une ligne").click()

    print("Filling second row (Tank 2)")
    row2 = page.locator(".multi-row").nth(1)
    row2.locator(".m-name").fill("Tank 2 (Essence)")
    row2.locator(".m-vol").fill("5000") # 5000 m3
    row2.locator(".m-rate").fill("1000") # 1000 m3/h -> 5h

    # Add a third row
    print("Adding third row")
    page.get_by_role("button", name="+ Ajouter une ligne").click()

    print("Filling third row (Tank 3)")
    row3 = page.locator(".multi-row").nth(2)
    row3.locator(".m-name").fill("Tank 3 (HFO)")
    row3.locator(".m-vol").fill("20000") # 20000 m3
    row3.locator(".m-rate").fill("1000") # 1000 m3/h -> 20h

    # Calculate
    print("Clicking Calculate")
    page.get_by_role("button", name="Calculer et Comparer").click()

    # Wait for results
    page.wait_for_selector("#resultMulti", state="visible")

    # Verify results
    # Expected order: Tank 2 (5h), Tank 1 (10h), Tank 3 (20h)

    # Only look inside resultMulti
    results = page.locator("#resultMulti .result-item")
    count = results.count()
    print(f"Found {count} result items")
    assert count == 3

    first_result = results.nth(0).inner_text()
    last_result = results.nth(2).inner_text()

    print(f"First result: {first_result}")
    print(f"Last result: {last_result}")

    assert "Tank 2" in first_result
    assert "PREMIER" in first_result
    assert "Tank 3" in last_result
    assert "DERNIER" in last_result

    # Take screenshot
    print("Taking screenshot")
    output_dir = "/home/jules/verification"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    page.screenshot(path=os.path.join(output_dir, "multi_simultaneous_result.png"), full_page=True)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_multi_simultaneous(page)
            print("Verification successful!")
        except Exception as e:
            print(f"Verification failed: {e}")
        finally:
            browser.close()
