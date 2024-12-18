from turtle import isvisible
from appium import webdriver
from appium.webdriver.webdriver import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

# Add any other capabilities you need

def login_webview_automation(appium_driver:webdriver, login_id, user_id, password, captcha_text):
    """
    Automates interaction with a WebView within an Android app using Appium.
    """
    try:

        print("Connecting to Appium server...")
        driver = appium_driver

        # Validate connection
        if not driver:
            raise ConnectionError("Failed to connect to the Appium server.")

        print("Connection successful. Waiting for WebView...")
        # Wait for WebView widget to appear
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((AppiumBy.CLASS_NAME, 'android.webkit.WebView'))
        )

        # Switch to WebView context
        contexts = driver.contexts
        print("Available contexts:", contexts)
        webview_context = next(
            (context for context in contexts if 'WEBVIEW_' in context), None
        )
        if not webview_context:
            raise RuntimeError("No WebView context found.")

        driver.switch_to.context(webview_context)
        print("Switched to WebView context:", webview_context)

        # Refresh if captcha is invalid
        if len(captcha_text) < 6:
            refresh_view(driver)
            return

        # Fill in form fields
        fields = {
            "//*[@id='loginsubmit_loginId']": login_id,
            "//*[@id='loginsubmit_userId']": user_id,
            "//*[@id='password']": password,
            "//*[@id='loginsubmit_captchaid']": captcha_text,
        }
        for xpath, input_text in fields.items():
            insert_data(driver=driver, xpath=xpath, input_text=input_text)

        # Click login button
        click_login_button(driver)

        # Switch back to native context
        driver.switch_to.context("NATIVE_APP")
        print("Switched back to native context:", driver.context)

    except Exception as e:
        print(f"Error during automation: {e}")
    finally:
        # Ensure the driver quits to release resources
        if 'driver' in locals() and driver:
            driver.quit()
            print("Driver session terminated.")

# ------------------------------------------------------------------------------------------------------------- #


def click_login_button(driver):
    """Clicks the login button."""
    try:
        element = driver.find_element(AppiumBy.XPATH, "//*[@id='btnSubmit']")
        print("Login button found. Clicking...")
        element.click()
        print("Login button clicked.")
    except Exception as e:
        print(f"Error clicking login button: {e}")


def click_refresh_button(driver):
    """Clicks the refresh button."""
    try:
        element = driver.find_element(AppiumBy.XPATH, "/html/body/form/div[2]/div[2]/div[1]/div/div[6]/i")
        print("Refresh button found. Clicking...")
        element.click()
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((AppiumBy.XPATH, "//*[@id='loginsubmit_captchaid']"))
        )
        print("Page refreshed.")
    except Exception as e:
        print(f"Error clicking refresh button: {e}")
    

def refresh_view(driver):
    """Refreshes the WebView."""
    try:
        print("Refreshing WebView...")
        driver.execute_script("window.location.reload();")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.CLASS_NAME, 'android.webkit.WebView'))
        )
        print("WebView refreshed.")
    except Exception as e:
        print(f"Error refreshing WebView: {e}")

def insert_data(driver:webdriver, xpath, input_text):
    """Inserts data into an input field."""
    try:
        element = driver.find_element(AppiumBy.XPATH, xpath)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element))
        print(f"Filling field at XPath: {xpath}")
        is_visible = False
        if xpath == "//*[@id='password']":
            element.click()
            print("Finding the Virtual Keyboard: //*[@id='password_keyboard']")
            WebDriverWait(driver, 30).until(EC.visibility_of_element_located((AppiumBy.XPATH,"//*[@id='password_keyboard']")))
            is_visible = True
        if is_visible:
            print("Virtual Keyboard Found")
            element = driver.find_element(AppiumBy.XPATH, "/html/body/div[2]/div[1]/input")
            element.clear()
            element.send_keys(input_text)
            element = driver.find_element(AppiumBy.XPATH, "/html/body/div[2]/div[2]/button[53]")
            element.click()
            return
        element.clear()
        element.send_keys(input_text)
        print(f"Field filled with value: {input_text}")
        return
    except Exception as e:
        print(f"Error inserting data into field {xpath}: {e}")
        return