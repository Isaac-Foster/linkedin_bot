import asyncio

from config import VARS


async def login(page):
    await asyncio.sleep(1)
    await page.fill('#username', VARS.LOGIN)
    await asyncio.sleep(1)
    await page.fill('#password', VARS.PASSWD)
    submit = await page.query_selector('//button[@aria-label="Entrar"]')
    await submit.click() 