import asyncio
from datetime import timedelta

from crawlee import Request, ConcurrencySettings
from crawlee.crawlers import PlaywrightCrawler, PlaywrightCrawlingContext, BeautifulSoupCrawler, BeautifulSoupCrawlingContext

async def main() -> None:
    crawler = PlaywrightCrawler(
        # max_requests_per_crawl=40,
        headless=True,
        request_handler_timeout=timedelta(seconds=30),
        # concurrency_settings=ConcurrencySettings(min_concurrency=1, max_concurrency = 1),
    )

    @crawler.router.default_handler
    async def listing_handler(context: PlaywrightCrawlingContext) -> None:
        url = context.request.url
        page_num = url.split('Page=')[1] if 'Page=' in url else '1'

        items = await context.page.query_selector_all('div.alist.newsrelease div.item')
        for item in items:
            href_el = await item.query_selector('div.title a')
            date_el = await item.query_selector('span.date')
            href = await href_el.get_attribute('href') if href_el else ''
            date = (await date_el.inner_text()).strip() if date_el else ''
            if href:
                await context.add_requests([
                    Request.from_url(href, label='DETAIL', user_data={'page_num': page_num, 'date': date})
                ])

        await context.enqueue_links(selector='ul.pagination a')

    @crawler.router.handler('DETAIL')
    async def detail_handler(context: PlaywrightCrawlingContext) -> None:
        page_num = context.request.user_data.get('page_num', '?')
        date = context.request.user_data.get('date', '?')
        href = context.request.url

        content_el = await context.page.query_selector('div.adetail.news div.body')
        content = (await content_el.inner_text()).strip() if content_el else ''

        context.log.info(f'Page {page_num} | {date} | {href} | {content[:10]}')

    await crawler.run(['https://www.centcom.mil/MEDIA/PRESS-RELEASES/'])
    
# 'https://crawlee.dev/'
# 'https://warehouse-theme-metal.myshopify.com/collections'
# 'https://www.centcom.mil/MEDIA/PRESS-RELEASES/'

if __name__ == "__main__":
    asyncio.run(main())
