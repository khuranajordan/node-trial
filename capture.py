import asyncio
from pyppeteer import launch
import os

async def capture_webpage(url):
    browser = await launch()
    page = await browser.newPage()

    await page.goto(url, waitUntil='domcontentloaded')

    # Get the total height of the page
    body_handle = await page.querySelector('body')
    height = await page.evaluate('(element) => element.getBoundingClientRect().height', body_handle)
    await body_handle.dispose()

    # Convert height to an integer
    height = int(height)

    # Set the viewport size to 1920x1024
    await page.setViewport({'width': 1920, 'height': 1024})

    # Create a directory to save screenshots if it doesn't exist
    screenshot_directory = os.path.join(os.path.dirname(__file__), 'screenshots')
    os.makedirs(screenshot_directory, exist_ok=True)

    # Capture each fold and save it with a unique name
    scroll_step = 500  # Adjust as needed
    fold_number = 1
    for scroll_top in range(0, height, scroll_step):
        await page.evaluate(f'window.scrollTo(0, {scroll_top})')

        # Capture the fold
        screenshot_path = os.path.join(screenshot_directory, f'Fold_{fold_number}.png')
        await page.screenshot({'path': screenshot_path})

        print(f'Captured Fold {fold_number}: {screenshot_path}')
        fold_number += 1

    await browser.close()

if __name__ == "__main__":
    url_to_capture = 'https://www.promptsmith.co'
    asyncio.get_event_loop().run_until_complete(capture_webpage(url_to_capture))
