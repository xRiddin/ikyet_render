from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path
from ..web.text_pw import summarize_text
from ..web.config import Config

FILE_DIR = Path(__file__).parent.parent
CFG = Config()


async def get_text(page_content):
    soup = BeautifulSoup(page_content, "html.parser")
    text = ""
    tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'p']
    for element in soup.find_all(tags):
        text += element.text + "\n\n"
    return text


BLOCK_RESOURCE_TYPES = [
  'image',
  'imageset',
  'media',
  'stylesheet'
]


# we can also block popular 3rd party resources like tracking:
BLOCK_RESOURCE_NAMES = [
  'analytics',
  'cdn.api.twitter',
  'facebook',
  'google',
  'google-analytics',
  'googletagmanager',
]


async def intercept_route(route):
    """intercept all requests and abort blocked ones"""
    if route.request.resource_type in BLOCK_RESOURCE_TYPES:
        print(f'blocking background resource {route.request} blocked type "{route.request.resource_type}"')
        await route.abort()
    elif any(key in route.request.url for key in BLOCK_RESOURCE_NAMES):
        print(f"blocking background resource {route.request} blocked name {route.request.url}")
        await route.abort()
    else:
        await route.continue_()


async def scrape_links_with_playwright(page, url):
    page_content = await page.content()
    soup = BeautifulSoup(page_content, "html.parser")
    hyperlinks = [
        (link.text, urljoin(url, link["href"]))
        for link in soup.find_all("a", href=True)
    ]
    return [f"{link_text} ({link_url})" for link_text, link_url in hyperlinks]


async def add_header(page):
    with open(f"{FILE_DIR}/web/overlay.js", "r") as f:
        overlay_script = f.read()
    await page.add_script_tag(content=overlay_script)


async def scrape_text_with_playwright(url):
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page(user_agent=CFG.user_agent)
            # await page.route("**/*", intercept_route)
            await page.goto(url)
            await page.wait_for_timeout(60000)
            page_content = await page.content()
            text = await get_text(page_content)
            print(text)
            return page, text
        except Exception as e:
            print("error in scrape text:", e)


async def browse_website(url: str, question: str):
    if not url:
        return "A URL was not specified, cancelling request to browse website.", None

    try:
        page, text = await scrape_text_with_playwright(url)
        await add_header(page)
        summary_text = summarize_text(url, text, question, page)
        print(summary_text)
        links = await scrape_links_with_playwright(page, url)
        print(links)

        if len(links) > 5:
            links = links[:5]
        return f"Answer gathered from website: {summary_text} \n \n Links: {links}", page

    except Exception as e:
        print("error in browse website:", e)


async def async_browse(url: str, question: str) -> str:
    print(f"Scraping url {url} with question {question}")
    try:
        summary_text, page = await browse_website(url, question)
        return f"Information gathered from url {url}: {summary_text}"
    except Exception as e:
        print(f"An error occurred while processing the url {url}: {e}")
        return f"Error processing the url {url}: {e}"
