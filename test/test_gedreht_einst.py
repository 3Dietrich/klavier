# Headless-Test (Playwright, webkit): Ausrichtung Breit, iPhone hochkant gehalten (Seite gedreht).
# Einstellungen scrollen mit dem Finger 1:1, Regler folgt dem Finger (Weg über die ganze Reglerlänge = ganzer Bereich).
# Finger per synthetischen PointerEvents. Bilder nach .shots/
from pathlib import Path
SEITE = (Path(__file__).resolve().parent.parent / 'index.html').as_uri()
SHOTS = str(Path(__file__).resolve().parent.parent / '.shots')
Path(SHOTS).mkdir(exist_ok=True)
import asyncio
from playwright.async_api import async_playwright
WISCH = """async ([sel, wege]) => {
  const el = document.querySelector(sel), r = el.getBoundingClientRect();
  let x = r.left + r.width / 2, y = r.top + r.height / 2;
  const ev = (typ) => el.dispatchEvent(new PointerEvent(typ, { pointerId: 7, clientX: x, clientY: y, bubbles: true, button: 0, pointerType: 'touch' }));
  ev('pointerdown');
  for (const [dx, dy] of wege) { x += dx; y += dy; ev('pointermove'); await new Promise(r => setTimeout(r, 16)); }
  ev('pointerup');
}"""
async def main():
    async with async_playwright() as p:
        b = await p.webkit.launch(headless=True)
        pg = await b.new_page(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True)
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.add_init_script("localStorage.setItem('klavier.einst', JSON.stringify({stand:2, ausrichtung:'quer'}))")
        await pg.goto(SEITE); await pg.wait_for_timeout(500)
        await pg.evaluate("einstAuf()"); await pg.wait_for_timeout(200)
        print('gedreht', await pg.evaluate("istGedreht()"), 'scrollTop', await pg.evaluate("$('einst').scrollTop"))
        # Seiten-senkrecht = Bildschirm waagrecht: Finger 20 x 6 px nach rechts = Seite 120 px nach oben gezogen -> scrollt 120 zurück
        await pg.evaluate(WISCH, ['#einst h2', [[6, 0]] * 20])
        await pg.wait_for_timeout(50)
        print('nach Wisch scrollTop (erwartet ~120 minus Anlauf 8)', await pg.evaluate("$('einst').scrollTop"))
        # Regler Lautstärke: Seiten-waagrecht = Bildschirm senkrecht nach unten
        await pg.evaluate("$('einst').scrollTop = 0")
        w = await pg.evaluate("$('laut').offsetWidth")
        vor = await pg.evaluate("+$('laut').value")
        await pg.evaluate("$('laut').closest('.zeile').scrollIntoView()")
        await pg.evaluate(WISCH, ['#laut', [[0, -2]] * 5 + [[0, -w / 40]] * 10])
        nach = await pg.evaluate("+$('laut').value")
        print('Regler Lautstärke', vor, '->', nach, f'(Finger {w/4:.0f} von {w} px = erwartet etwa -25)')
        await pg.screenshot(path=f'{SHOTS}/gedreht_einst.png')
        print(errs)
        await b.close()
asyncio.run(main())
