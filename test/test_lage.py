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
        for name, vp, aus in [('quer', (844, 390), 'auto'), ('hoch', (390, 844), 'auto'), ('gedreht', (390, 844), 'quer')]:
            pg = await b.new_page(viewport={'width': vp[0], 'height': vp[1]})
            errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.add_init_script(f"localStorage.setItem('klavier.einst', JSON.stringify({{ausrichtung:'{aus}'}}))")
            await pg.goto(SEITE)
            await pg.wait_for_timeout(1200)
            await pg.screenshot(path=f'{SHOTS}/lage_{name}.png')
            h = await pg.evaluate("() => $('leiste').getBoundingClientRect().height")
            print(name, 'leiste', h, errs)
        await b.close()
asyncio.run(main())
