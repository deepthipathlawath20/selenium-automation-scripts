import time, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Demo site
DEMO_URL = "https://www.saucedemo.com/"

# Credentials
VALID_USER = "standard_user"
VALID_PWD  = "secret_sauce"
INVALID_USER = "invalid_user"
INVALID_PWD  = "wrong_pass"

def take_screenshot(driver, name="screenshot.png"):
    """
    Always save screenshots to the /screenshots folder (one level above /src).
    Creates the folder if it doesn't exist.
    """
    base = os.path.dirname(__file__)                 # -> .../<repo>/src
    shots = os.path.join(base, "..", "screenshots")  # -> .../<repo>/screenshots
    os.makedirs(shots, exist_ok=True)
    path = os.path.join(shots, name)
    driver.save_screenshot(path)
    print(f"📸 Screenshot saved to {os.path.abspath(path)}")

def test_valid_login():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(DEMO_URL)

    # Perform login with valid creds
    driver.find_element(By.ID, "user-name").send_keys(VALID_USER)
    driver.find_element(By.ID, "password").send_keys(VALID_PWD)
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)  # quick wait for navigation

    try:
        assert "inventory" in driver.current_url.lower()
        print("✅ Valid Login Test: PASS")
        take_screenshot(driver, "valid_login_pass.png")
    except AssertionError:
        print("❌ Valid Login Test: FAIL")
        take_screenshot(driver, "valid_login_fail.png")
        raise
    finally:
        driver.quit()

def test_invalid_login():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(DEMO_URL)

    # Perform login with invalid creds
    driver.find_element(By.ID, "user-name").send_keys(INVALID_USER)
    driver.find_element(By.ID, "password").send_keys(INVALID_PWD)
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)  # allow error to render

    try:
        error_box = driver.find_element(By.CLASS_NAME, "error-message-container")
        msg = error_box.text.strip()
        assert "epic sadface" in msg.lower()
        print("✅ Invalid Login Test: PASS (error displayed)")
        take_screenshot(driver, "invalid_login_pass.png")
    except Exception as e:
        print(f"❌ Invalid Login Test: FAIL ({e})")
        take_screenshot(driver, "invalid_login_fail.png")
        raise
    finally:
        driver.quit()

if __name__ == "__main__":
    test_valid_login()
    test_invalid_login()
