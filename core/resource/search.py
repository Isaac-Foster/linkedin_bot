import asyncio, re

from config import VARS


async def search(page, query: str, attribute: str = "aria-label", value: str = "Pesquisar"):
    search = await page.query_selector(f'//input[@{attribute}="{value}"]')
    await search.fill(query)
    await search.press("Enter")


async def people(page):
    #id="jobs-search-box-keyword-id-ember138"

    await asyncio.sleep(3)

    await page.wait_for_selector('//div[@id="search-reusables__filters-bar"]') 
    
    buttons = page.locator('//div[@id="search-reusables__filters-bar"]//button')

    count = await buttons.count()

    for i in range(count):
        text = await buttons.nth(i).text_content()

        if "Pessoas" in text.strip(): 
            await buttons.nth(i).click()
            break


async def disable(invite):
    if (await invite.is_disabled()):
        close = await page.query_selector('//button[@aria-label="Fechar"]')
        await close.click()


async def connections(page, connect, mode):
    await page.wait_for_selector('div.search-results-container')

    buttons = page.locator('div.search-results-container li')

    count = await buttons.count()

    for i in range(count):
        item = buttons.nth(i)
        await asyncio.sleep(0.01)
        invite_button = item.locator('button[aria-label*="Convidar"], button[aria-label*="Conectar"], button[aria-label*="Adicionar"]',)

        if await invite_button.count() > 0:
            # Aqui você pode clicar no botão, se necessário:
            aria_label = await invite_button.first.get_attribute('aria-label')
            name = re.search(r'Convidar (?P<name>[\w\s\.]+) para', aria_label)

            if name: name: str = name["name"].strip()

            await invite_button.first.click()

            html = await page.content()

            await asyncio.sleep(0.4)


            if mode == 1:
                await page.wait_for_selector('//button[@aria-label="Enviar sem nota"]')
                invite = await page.query_selector('//button[@aria-label="Enviar sem nota"]')

                if (await invite.is_disabled()):
                    close = await page.query_selector('//button[@aria-label="Fechar"]')
                    await close.click()
                    continue

                print(f"✅ {'\033[33m'}Mandou conexão para: {'\033[95m'}{name}")

            
            elif mode == 2:
                await page.wait_for_selector('//button[@aria-label="Adicionar nota"]')

                invite = await page.query_selector('//button[@aria-label="Enviar sem nota"]')

                if (await invite.is_disabled()):
                    close = await page.query_selector('//button[@aria-label="Fechar"]')
                    await close.click()
                    continue

                invite = await page.query_selector('//button[@aria-label="Adicionar nota"]')
                await invite.click()
                template = VARS.TEMPLATE.format(name=name)
                await page.fill('//textarea[@name="message"]', template)
                await page.click('//button[@aria-label="Enviar convite"]')
                print(f"💬 {'\033[32m'}Mandou conexão com nota para: {'\033[95m'}{name}")

            try:
                existis = page.query_selector('//button[@aria-label="Entendi"]')
                if existis:
                    await page.click('//button[@aria-label="Entendi"]')
            except:
                pass
            
            await asyncio.sleep(0.3)
            await invite.click()

            try:
                await asyncio.sleep(0.5)
                text = await page.query_selector('//h2[@id="ip-fuse-limit-alert__header"]')
                html = await text.inner_html()

                if text and "limite" in html and not "prestes" in html:
                    return page, connect, True
                    
            except: 
                pass
            connect += 1

    return page, connect, False