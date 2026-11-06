# Headless-Test (Playwright, webkit): Einstellungen offen, Tasten daneben spielbar, Stimmen in einer Reihe,
# Schließen nur mit Fertig. Quer und gedreht (Breit, hochkant gehalten). Bilder nach .shots/
from pathlib import Path
SEITE = (Path(__file__).resolve().parent.parent / 'index.html').as_uri()
SHOTS = str(Path(__file__).resolve().parent.parent / '.shots')
Path(SHOTS).mkdir(exist_ok=True)
import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.webkit.launch(headless=True)
        for name, vp, aus in [('quer', (844, 390), 'auto'), ('gedreht', (390, 844), 'quer'), ('hoch', (390, 844), 'auto')]:
            pg = await b.new_page(viewport={'width': vp[0], 'height': vp[1]}, has_touch=True, is_mobile=True)
            errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.add_init_script(f"localStorage.setItem('klavier.einst', JSON.stringify({{stand:2, ausrichtung:'{aus}'}}))")
            await pg.goto(SEITE); await pg.wait_for_timeout(400)
            await pg.evaluate("einstAuf()")
            await pg.evaluate("$('stimmenWahl').scrollIntoView()")
            zeilen = await pg.evaluate("new Set([...$('stimmenWahl').children].map(k => Math.round(istGedreht() ? k.getBoundingClientRect().left : k.getBoundingClientRect().top))).size")
            # Taste weit weg von den Einstellungen antippen (quer: rechts unten, gedreht: links unten, hoch: unten Mitte)
            x, y = {'quer': (vp[0] - 40, vp[1] - 30), 'gedreht': (30, vp[1] - 60), 'hoch': (vp[0] / 2, vp[1] - 40)}[name]
            await pg.touchscreen.tap(x, y)
            await pg.wait_for_timeout(100)
            offen = await pg.evaluate("$('einst').classList.contains('offen')")
            gespielt = await pg.evaluate(f"noteBei({x}, {y})")
            await pg.screenshot(path=f'{SHOTS}/einst_offen_{name}.png')
            await pg.click('#fertig')
            zu = not await pg.evaluate("$('einst').classList.contains('offen')")
            print(name, 'Stimmen-Zeilen', zeilen, '| Taste daneben', gespielt, '| bleibt offen', offen, '| Fertig schließt', zu, errs)
            await pg.close()
        await b.close()
asyncio.run(main())
