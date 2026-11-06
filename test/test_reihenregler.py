# Headless-Test (Playwright, webkit): Reihen-Regler bis quadratische Tasten, Anschließen bei Quinte/Quarte,
# großer Schirm mit Grau unten und oben. Bilder nach .shots/
from pathlib import Path
SEITE = (Path(__file__).resolve().parent.parent / 'index.html').as_uri()
SHOTS = str(Path(__file__).resolve().parent.parent / '.shots')
Path(SHOTS).mkdir(exist_ok=True)
import asyncio, json
from playwright.async_api import async_playwright
INFO = """() => {
  const rs = [...tasten.children].map(r => [...r.querySelectorAll('.w')]);
  const w = tasten.querySelector('.w').getBoundingClientRect();
  return { reihen: rs.length, max: +$('reihen').max, wert: $('reihen').value, label: $('reihenW').textContent,
    lage: $('lage').textContent, w: Math.round(w.width), h: Math.round(w.height),
    grauUnten: rs[0].filter(k => k.classList.contains('aus')).length,
    grauOben: rs.flat().filter(k => k.classList.contains('aus')).length - rs[0].filter(k => k.classList.contains('aus')).length,
    anfaenge: rs.map(r => r[0].dataset.note ?? 'grau'), enden: rs.map(r => r[r.length-1].dataset.note ?? 'grau') };
}"""
async def main():
    async with async_playwright() as p:
        b = await p.webkit.launch(headless=True)
        faelle = [
            ('gross', (1920, 1080), {}),
            ('quer', (844, 390), {}),
            ('quer_7', (844, 390), {'quer': {'reihen': 7}}),
            ('hoch_quinte', (390, 844), {'hoch': {'abstand': 7, 'buendig': False}}),
            ('hoch_quinte_an', (390, 844), {'hoch': {'abstand': 7, 'buendig': True}}),
            ('hoch_oktave_an', (390, 844), {'hoch': {'abstand': 12, 'buendig': True}}),
            ('gross_quarte_an', (1920, 1080), {'quer': {'abstand': 5, 'buendig': True}}),
        ]
        for name, vp, extra in faelle:
            pg = await b.new_page(viewport={'width': vp[0], 'height': vp[1]})
            errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.add_init_script(f"localStorage.setItem('klavier.einst', JSON.stringify({json.dumps({'stand': 2, **extra})}))")
            await pg.goto(SEITE)
            await pg.wait_for_timeout(800)
            await pg.screenshot(path=f'{SHOTS}/reihen_{name}.png')
            print(name, await pg.evaluate(INFO), errs)
            await pg.close()
        await b.close()
asyncio.run(main())
