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
        for name, vp in [('quer', (844, 390)), ('hoch', (390, 844))]:
            pg = await b.new_page(viewport={'width': vp[0], 'height': vp[1]})
            errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto(SEITE)
            await pg.click('#einstKnopf'); await pg.wait_for_timeout(200)
            await pg.screenshot(path=f'{SHOTS}/einst_{name}.png')
            z = await pg.locator('.zeile.regel').first.bounding_box()
            vor = await pg.eval_on_selector('#breite', 'e => e.value')
            # in der Beschriftung anfassen und waagrecht ziehen
            await pg.mouse.move(z['x'] + 20, z['y'] + z['height'] / 2); await pg.mouse.down()
            for i in range(1, 11): await pg.mouse.move(z['x'] + 20 + i * 12, z['y'] + z['height'] / 2)
            await pg.mouse.up()
            nach = await pg.eval_on_selector('#breite', 'e => e.value')
            # senkrecht: Wert darf sich nicht ändern
            await pg.mouse.move(z['x'] + 100, z['y'] + 10); await pg.mouse.down()
            for i in range(1, 8): await pg.mouse.move(z['x'] + 100 + i, z['y'] + 10 + i * 6)
            await pg.mouse.up()
            senk = await pg.eval_on_selector('#breite', 'e => e.value')
            sh = await pg.eval_on_selector('#einst', 'e => [e.scrollHeight, e.clientHeight]')
            print(name, 'breite', vor, '->', nach, 'senkrecht', senk, 'scroll/sichtbar', sh, errs)
        await b.close()
asyncio.run(main())
