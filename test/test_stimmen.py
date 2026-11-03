# Headless-Test (Playwright, webkit/chromium) gegen die lokale index.html; Bilder nach .shots/
from pathlib import Path
SEITE = (Path(__file__).resolve().parent.parent / 'index.html').as_uri()
SHOTS = str(Path(__file__).resolve().parent.parent / '.shots')
Path(SHOTS).mkdir(exist_ok=True)
import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        for name in ['webkit', 'chromium']:
            b = await getattr(p, name).launch(headless=True)
            pg = await b.new_page(viewport={'width': 844, 'height': 390})
            errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto(SEITE)
            await pg.wait_for_timeout(3000)
            await pg.mouse.click(400, 300)  # entsperren
            # 20 Töne gehalten (Finger-IDs simuliert), dann loslassen
            r = await pg.evaluate('''async () => {
                const noten = [...new Set([...tasten.querySelectorAll('[data-note]')].map(k => +k.dataset.note))].slice(0, 20);
                noten.forEach((n, i) => drueck(1000 + i, n));
                const gehalten = aktiv.length;
                noten.forEach((n, i) => loslass(1000 + i));
                s.stimmen = 4; stimmenKappen(4);
                const nachKappen = aktiv.length;
                await new Promise(r => setTimeout(r, 1500));
                return { stimmen: 8, gehalten, nachKappen, nachAusklang: aktiv.length };
            }''')
            print(name, r, errs)
            await b.close()
asyncio.run(main())
