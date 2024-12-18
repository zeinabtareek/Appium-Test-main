from appium.webdriver.webdriver import AppiumOptions
from login_automation import login_webview_automation
from home_automation import home_webview_automation
from fastapi import FastAPI, HTTPException,BackgroundTasks
from pydantic import BaseModel
import logging
from fastapi.middleware.cors import CORSMiddleware
from appium import webdriver

app = FastAPI()

# Enable CORS for all origins (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins. Replace with specific domains for security.
    allow_methods=["*"],  # Allow all HTTP methods.
    allow_headers=["*"],  # Allow all headers.
)

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Request model validation
class AutomationRequest(BaseModel):
    serverUrl: str
    loginId: str
    userId: str
    password: str
    app: str
    deviceName: str
    driverPath: str
    captchaText: str
    websiteUrl: str

def initiate_appium_session(request_data:AutomationRequest) -> webdriver:
    options = AppiumOptions()
    options.set_capability("platformName", "Android")
    options.set_capability("appium:deviceName", request_data.deviceName)
    options.set_capability("appium:app", request_data.app)
    options.set_capability("appium:automationName", "UiAutomator2")
    options.set_capability("appium:noReset", True)
    options.set_capability("appium:fullReset", False)
    options.set_capability("appium:chromedriverExecutable", request_data.driverPath)
    options.set_capability("appium:ensureWebviewsHavePages", True)
    options.set_capability("appium:newCommandTimeout", 3600)
    options.set_capability("appium:appWaitPackage", "com.example")
    options.set_capability("appium:appWaitActivity", "com.example.MainActivity")
    options.set_capability("appium:uiautomator2ServerLaunchTimeout", 30000)
    driver = webdriver.Remote(request_data.serverUrl, options=options)
    return driver

def run_automation(request_data: AutomationRequest):
    driver = initiate_appium_session(request_data= request_data)
    # Run the automation task
    if request_data.websiteUrl == "https://www.iobnet.co.in/ibanking/corplogin.do":
        login_webview_automation(
            appium_driver=driver,
            login_id=request_data.loginId,
            user_id=request_data.userId,
            password=request_data.password,
            captcha_text=request_data.captchaText,
        )
    elif request_data.websiteUrl == "https://www.iobnet.co.in/ibanking/loginsuccess.do":
        home_webview_automation(
            appium_driver= driver,
        )

@app.post("/click-button")
async def click_button(request: AutomationRequest , background_tasks: BackgroundTasks):
    """
    Endpoint to handle automation requests for Appium.
    """
    logger.info("Received automation request.")
    try:
        # Add the automation task to run in the background
        background_tasks.add_task(
            run_automation,
            request,
        )
        logger.info("Button clicked successfully.")
        return {"status": "success", "message": "Button clicked successfully!"}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# Run the app in ASGI mode (use uvicorn for production)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6000)