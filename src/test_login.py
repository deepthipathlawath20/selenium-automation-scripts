import time, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Demo site and credentials
DEMO_URL = "https://www.saucedemo.com/"
USER = "standard_user"
PWD = "secret_sauce"

# Function to take screenshot if test fails
def take_screenshot(driver, name="fail.png"):
    p = os.path.join(os.path.dirname(__file__), "..", "screenshots", name)
    driver.save_screenshot(p)

def main():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(DEMO_URL)
    try:
        # Enter login details
        driver.find_element(By.ID, "user-name").send_keys(USER)
        driver.find_element(By.ID, "password").send_keys(PWD)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(1)

        # Assertion: check if we landed on inventory page
        assert "inventory" in driver.current_url.lower()
        print("Login test: PASS")

    except Exception as e:
        print("Login test: FAIL", e)
        take_screenshot(driver, "login_fail.png")
        raise

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
