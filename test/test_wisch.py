# Headless-Test (Playwright, webkit/chromium) gegen die lokale index.html; Bilder nach .shots/
from pathlib import Path
SEITE = (Path(__file__).resolve().parent.parent / 'index.html').as_uri()
SHOTS = str(Path(__file__).resolve().parent.parent / '.shots')
Path(SHOTS).mkdir(exist_ok=True)
import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        ctx = await b.new_context(viewport={'width': 844, 'height': 390}, has_touch=True, is_mobile=True)
        pg = await ctx.new_page()
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(SEITE)
        await pg.wait_for_timeout(1500)
        await pg.evaluate("() => { window.gespielt = []; const alt = drueck; drueck = (id, n) => { gespielt.push(n); alt(id, n); }; }")
        cdp = await ctx.new_cdp_session(pg)
        y = 360
        await cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': 20, 'y': y}]})
        for x in range(20, 800, 15):
            await cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x, 'y': y}]})
            await pg.wait_for_timeout(8)
        await cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        r = await pg.evaluate("({gespielt, aktiv: aktiv.length})")
        print(r, errs)
        await b.close()
asyncio.run(main())
