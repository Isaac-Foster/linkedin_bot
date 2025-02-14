import os
from playwright.async_api import async_playwright

from config import VARS


async def init_browser():
    user_data_dir = os.path.join(VARS.ROOT_PATH, VARS.DIR_NAME)

    chromium_options = {
        "headless": False,
        "args": [
            '--disable-blink-features=AutomationControlled',
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--disable-popup-blocking',
        ]
    }

    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch_persistent_context(
        user_data_dir,
        **chromium_options
    )
    
    # Redimensiona a janela explicitamente
    page = browser.pages[0] if browser.pages else await browser.new_page()
    await page.set_viewport_size({"width": 1920, "height": 1080})
    
    return page, browser, playwright
