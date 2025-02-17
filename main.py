import asyncio, os, re

from config import VARS
from core import init_browser
from core.resource.login import login
from core.resource.search import search, people, connections
 

async def apply_connections(page, mode):
    await people(page)
    await asyncio.sleep(2)

    connect = 0
    ended = False

    while True:
        page, connect, ended = await connections(page, connect, mode)

        if ended: print("Limite de convites atingido"); break

        await asyncio.sleep(1)

        await page.wait_for_selector('//button[@aria-label="Avançar"]', state="visible")
        next_btn = await page.query_selector('//button[@aria-label="Avançar"]')

        await next_btn.click()
        await asyncio.sleep(2)


async def scraping_works(page, container):
    await asyncio.sleep(1)

    count = 0

    for work in container:
        count += 1
        #await work.wa('//a[@aria-label]')
        html = await work.inner_html()
        tag = await work.query_selector('//a[@aria-label]')
        pattern = r'href=(?P<url>\"[\w\S]+\") id=\"[\w\d]+\" class=\".+\" aria-label=\"(?P<name>[\w\s]+)\"'
        aaa = re.search(pattern, html)
        print(aaa)

        if not tag: continue

        href = "https://www.linkedin.com/" + (await tag.get_attribute("href"))

        title = (await tag.get_attribute("aria-label"))
        print(title)
        await asyncio.sleep(1)
    print(count)


async def main():
    page, browser, play = await init_browser()

    await page.goto("https://www.linkedin.com/feed/")

    await asyncio.sleep(2)

    if (await page.query_selector("#username")):
        await login(page)
        await asyncio.sleep(60)
    
    if VARS.MODE  in (1, 2):
        await search(page, VARS.SEARCH, value=VARS.QUERY_ATTR_VALUE)
        await apply_connections(page, mode=VARS.MODE)
    
    elif VARS.MODE == 3:
        await page.goto("https://www.linkedin.com/jobs/search/?refresh=true")
        await asyncio.sleep(1)

        await search(page, VARS.SEARCH, value=VARS.QUERY_ATTR_VALUE)

        filters = await page.query_selector('//button[@aria-label="Exibir todos os filtros. Ao clicar neste botão, todas as opções de filtro serão exibidas."]')
        await filters.click()
        await asyncio.sleep(1)

        await page.click('label[for="advanced-filter-timePostedRange-r604800"]')

        await page.click('label[for="advanced-filter-experience-1"]')
        await page.click('label[for="advanced-filter-experience-2"]')
        await page.click('label[for="advanced-filter-experience-3"]')
        await page.click('label[for="advanced-filter-experience-4"]')

        await page.click('label[for="advanced-filter-workplaceType-2"]')
        
        await page.click('//div[@class="artdeco-toggle artdeco-toggle--32dp artdeco-toggle--default ember-view"]')
        await asyncio.sleep(1)
        await page.click('//button[@data-test-reusables-filters-modal-show-results-button="true"]')

        #print(VARS.SEARCH, VARS.QUERY_ATTR_VALUE)
        
        await page.query_selector('//div/div[2]/div[1]/div/ul')

        container_works = await page.query_selector_all('//li[contains(@class, "ember-view")]')
        await scraping_works(page, container_works)
    
    await browser.close()
    await play.stop()


if __name__ == "__main__":
    asyncio.run(main())