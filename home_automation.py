from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.webdriver import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def home_webview_automation(appium_driver:webdriver):
    """
    Automates interaction with a WebView within an Android app using Appium.
    """

    # Initialize Appium driver
    print("Connecting to Appium server...")
    driver = appium_driver
    
    # Script logic
    try:
        # Example: Login page
        wait_and_send_keys(driver,AppiumBy.ID, "username_field_id", "YourUsername")
        wait_and_send_keys(driver,AppiumBy.ID, "password_field_id", "YourPassword")
        wait_and_click(driver,AppiumBy.ID, "login_button_id")

        # Example: Funds Transfer
        wait_and_click(driver,AppiumBy.CSS_SELECTOR, ".navbar-toggler")  # Click hamburger menu
        wait_and_click(driver,AppiumBy.CSS_SELECTOR, "#main2 a.menuhref")  # Click 'Funds Transfer'
        wait_and_click(driver,AppiumBy.CSS_SELECTOR, "a.nav-link[href='./ibLeftMenu.do?handleId=2001_IMPSP2A']")  # Click 'IOB Account'

        # Transfer details
        wait_and_send_keys(driver,AppiumBy.ID, "ibIMPSFundsTransfer_amtRs", "400")  # Enter amount
        wait_and_click(driver,AppiumBy.ID, "ibIMPSFundsTransfer_subm")  # Submit transfer

        # Handle OTP entry manually or through automation if possible
        print("Enter the OTP to complete the process.")

        # Logout
        wait_and_click(driver,AppiumBy.CSS_SELECTOR, 'input.action-btn.flt-l[value="Home"]')  # Click 'Home' button
    finally:
        # Close the session
        driver.quit()

# Utility function for dynamic waits
def wait_and_click(driver:webdriver,locator_type, locator_value, timeout=10):
    """Waits for an element to be visible and clicks it."""
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((locator_type, locator_value))
    )
    element.click()

def wait_and_send_keys(driver:webdriver,locator_type, locator_value, text, timeout=10):
    """Waits for an element to be visible and sends keys."""
    element = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((locator_type, locator_value))
    )
    element.send_keys(text)
