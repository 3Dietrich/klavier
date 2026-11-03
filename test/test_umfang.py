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
        for name, vp, aus, start in [('quer', (844, 390), 'auto', 4), ('hoch', (390, 844), 'auto', 36), ('hoch_oben', (390, 844), 'auto', 100)]:
            pg = await b.new_page(viewport={'width': vp[0], 'height': vp[1]})
            errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
            lage = 'quer' if vp[0] > vp[1] else 'hoch'
            await pg.add_init_script(f"localStorage.setItem('klavier.einst', JSON.stringify({{stand:2, {lage}:{{start:{start}}}}}))")
            await pg.goto(SEITE)
            await pg.wait_for_timeout(2500)
            await pg.screenshot(path=f'{SHOTS}/umfang_{name}.png')
            r = await pg.evaluate("() => ({reihen: tasten.children.length, lage: $('lage').textContent, aus: tasten.querySelectorAll('.aus').length, oben: hoechsterTon(), puffer: puffer.size, w: tasten.querySelector('.w').getBoundingClientRect().width|0, h: tasten.querySelector('.w').getBoundingClientRect().height|0})")
            print(name, r, errs)
        await b.close()
asyncio.run(main())
