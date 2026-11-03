# Headless-Test (Playwright, webkit/chromium) gegen die lokale index.html; Bilder nach .shots/
from pathlib import Path
SEITE = (Path(__file__).resolve().parent.parent / 'index.html').as_uri()
SHOTS = str(Path(__file__).resolve().parent.parent / '.shots')
Path(SHOTS).mkdir(exist_ok=True)
import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.webkit.launch(headless=True)
        pg = await b.new_page(viewport={'width': 844, 'height': 390}, device_scale_factor=2)
        await pg.add_init_script("localStorage.setItem('klavier.einst', JSON.stringify({quer:{sBreite:100}}))")
        await pg.goto(SEITE)
        await pg.wait_for_timeout(800)
        await pg.screenshot(path=SHOTS + '/schwarz_100.png', clip={'x': 0, 'y': 38, 'width': 420, 'height': 180})
        await b.close()
asyncio.run(main())
