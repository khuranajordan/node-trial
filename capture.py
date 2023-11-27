import asyncio
import os
from pyppeteer import launch


async def capture_webpage(url):
    browser = await launch()
    page = await browser.newPage()

    await page.goto(url, waitUntil='domcontentloaded')

    body_handle = await page.querySelector('body')
    height = await page.evaluate('(element) => element.getBoundingClientRect().height', body_handle)

    await page.setViewport({'width': 1920, 'height': 1024})

    screenshot_directory = os.path.join(
        os.path.dirname(__file__), 'screenshots')
    os.makedirs(screenshot_directory, exist_ok=True)

    for fold_number in range(1, (height // 1024) + 1):
        await page.evaluate(f'window.scrollTo(0, {fold_number * 1024})')

        screenshot_path = os.path.join(
            screenshot_directory, f'Fold_{fold_number}.png')
        await page.screenshot({'path': screenshot_path})

        print(f'Captured Fold {fold_number}: {screenshot_path}')

    await browser.close()

if __name__ == "__main__":
    import asyncio
    url_to_capture = 'https://rohankhurana.netlify.app'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(capture_webpage(url_to_capture))
