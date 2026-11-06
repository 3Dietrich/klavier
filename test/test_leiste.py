# Headless-Test (Playwright, webkit, iPhone quer mit Touch): Leistenknöpfe lösen beim Aufsetzen aus,
# auch ganz oben am Rand; ‹ › gehen in Halbtönen, Reihe kann mit schwarzer Taste beginnen. Bilder nach .shots/
from pathlib import Path
SEITE = (Path(__file__).resolve().parent.parent / 'index.html').as_uri()
SHOTS = str(Path(__file__).resolve().parent.parent / '.shots')
Path(SHOTS).mkdir(exist_ok=True)
import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.webkit.launch(headless=True)
        pg = await b.new_page(viewport={'width': 844, 'height': 390}, has_touch=True, is_mobile=True)
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.add_init_script("localStorage.setItem('klavier.einst', JSON.stringify({stand:2, quer:{start:41}}))")
        await pg.goto(SEITE); await pg.wait_for_timeout(500)
        lage = lambda: pg.evaluate("[$('lage').textContent, prof().start, tasten.querySelector('.reihe').firstElementChild.className]")
        print('start F', await lage())
        # oberster Pixel des ›-Knopfs antippen
        box = await pg.locator('#tonHoch').bounding_box()
        await pg.touchscreen.tap(box['x'] + box['width'] / 2, 1)
        print('› oben am Rand', await lage())
        await pg.screenshot(path=f'{SHOTS}/leiste_fis.png')
        box = await pg.locator('#tonRunter').bounding_box()
        await pg.touchscreen.tap(box['x'] + box['width'] / 2, 2)
        await pg.touchscreen.tap(box['x'] + box['width'] / 2, 2)
        print('‹‹', await lage())
        box = await pg.locator('#einstKnopf').bounding_box()
        await pg.touchscreen.tap(box['x'] + box['width'] / 2, 1)
        print('⚙ offen', await pg.evaluate("$('einst').classList.contains('offen')"))
        await pg.keyboard.press('Escape')
        print('Esc zu', not await pg.evaluate("$('einst').classList.contains('offen')"))
        await pg.focus('#tonHoch'); await pg.keyboard.press('Enter')
        print('Enter auf ›', await lage())
        # schwarze Taste ganz links spielbar?
        print('Taste links unten', await pg.evaluate("(() => { const r = tasten.querySelector('.reihe').getBoundingClientRect(); return noteBei(r.left + 4, r.top + 10); })()"))
        print(errs)
        await b.close()
asyncio.run(main())
