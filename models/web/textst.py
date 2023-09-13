import bs4
from playwright.async_api import async_playwright
import asyncio


async def scrape_text_with_playwright(url):
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36")
            # await page.route("**/*", intercept_route)
            await page.goto(url)
            await page.wait_for_timeout(60000)
            page_content = await page.content()
            text = await get_text(page_content)
            print(text)
            return page, text
        except Exception as e:
            print("error in scrape text:", e)

async def get_text(page_content):
    soup = bs4.BeautifulSoup(page_content, "html.parser")
    text = ""
    tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'p']
    for element in soup.find_all(tags):
        text += element.text + "\n\n"
    return text


loop = asyncio.get_event_loop()
loop.run_until_complete(scrape_text_with_playwright("https://www.indeed.com/career-advice/career-development/types-of-operating-systems"))