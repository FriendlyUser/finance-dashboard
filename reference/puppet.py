import asyncio
from pyppeteer import launch, errors
import sys

def td_get_tables():
    async def main():
        browser = await launch(headless=False)
        page = await browser.newPage()
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
        await page.goto('https://www.td.com/ca/en/asset-management/funds/solutions/mutual-funds/', timeout=240000)
        await page.screenshot(fullPage=true, path='screenshot.png')
        data = await page.content()
        with open('index.html', 'w',errors='ignore') as f:
            f.write(data)
        await page.screenshot({'path': 'example.png'})
        await browser.close()
    
    success = True
    # try:
    asyncio.get_event_loop().run_until_complete(main())
    # except errors.TimeoutError as e:
    #     print('error message here')
    #     print(e)
    #     success = False
    # except:
    #     print("Unexpected error:", sys.exc_info()[0])
    return success

td_get_tables()