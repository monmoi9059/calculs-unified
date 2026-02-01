import os
from playwright.sync_api import sync_playwright

def verify_default_tanks():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the local HTML file
        file_path = os.path.abspath("maritime_calc/www/index.html")
        page.goto(f"file://{file_path}")

        # Verify Configuration Tab is active
        page.wait_for_selector("#config.active")

        # Scenario 1: Leave tanks empty
        page.fill("#shipDwt", "50000")
        page.fill("#tankHeight", "20")
        page.fill("#numTanks", "") # Explicitly empty

        # Click Save Config
        page.click("button:has-text('Sauvegarder Configuration')")

        # Trigger calculation to verify the used 'tanks' value indirectly
        # VolumePerTank = TotalVol / Tanks
        # If Tanks=14, VolPerTank should reflect that.

        page.click("button:has-text('Calcul 1m (m³)')")
        page.click("button:has-text('Calculer le Volume pour 1m')")

        # Get result
        vol_one_tank = page.text_content("#volOneTank1m")
        print(f"Volume per tank (Empty Input): {vol_one_tank}")

        # Calculation:
        # DWT = 50000, Density = 1.025 => TotalVol = 48780.4878
        # Tanks = 14 (Default)
        # VolPerTank = 48780.4878 / 14 = 3484.32
        # Height = 20
        # VolPerMeter = 3484.32 / 20 = 174.21

        expected_vol_per_meter = "174.22" # approx

        if expected_vol_per_meter in vol_one_tank:
            print("SUCCESS: Default tanks=14 used when input is empty.")
        else:
            print(f"FAILURE: Expected {expected_vol_per_meter} but got {vol_one_tank}")

        # Scenario 2: Enter 0
        page.click("button:has-text('Configuration')")
        page.fill("#numTanks", "0")
        page.click("button:has-text('Sauvegarder Configuration')")

        page.click("button:has-text('Calcul 1m (m³)')")
        page.click("button:has-text('Calculer le Volume pour 1m')")

        vol_one_tank_zero = page.text_content("#volOneTank1m")
        print(f"Volume per tank (Input 0): {vol_one_tank_zero}")

        if expected_vol_per_meter in vol_one_tank_zero:
             print("SUCCESS: Default tanks=14 used when input is 0.")
        else:
             print(f"FAILURE: Expected {expected_vol_per_meter} but got {vol_one_tank_zero}")

        browser.close()

if __name__ == "__main__":
    verify_default_tanks()
