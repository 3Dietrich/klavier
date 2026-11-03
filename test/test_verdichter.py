# Headless-Test (Playwright, webkit/chromium) gegen die lokale index.html; Bilder nach .shots/
from pathlib import Path
SEITE = (Path(__file__).resolve().parent.parent / 'index.html').as_uri()
SHOTS = str(Path(__file__).resolve().parent.parent / '.shots')
Path(SHOTS).mkdir(exist_ok=True)
import asyncio
from playwright.async_api import async_playwright
# Einzelton und Akkord durch die echte Kette (offline nachgebaut) schicken: Verstärkungsabsenkung des Verdichters messen
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        pg = await b.new_page()
        await pg.goto(SEITE)
        r = await pg.evaluate('''async () => {
            const aus = {};
            for (const [name, noten, sch] of [['einzel30', [60], 30], ['einzel100', [24], 100], ['dreiklang30', [60, 64, 67], 30], ['acht100', [48,52,55,60,64,67,72,76], 100]]) {
                const oc = new OfflineAudioContext(1, 48000, 48000);
                const comp = oc.createDynamicsCompressor();
                comp.threshold.value = 0; comp.knee.value = 6; comp.ratio.value = 8; comp.attack.value = 0.003; comp.release.value = 0.15;
                const bus = oc.createGain(); bus.connect(comp).connect(oc.destination);
                for (const n of noten) { const q = oc.createBufferSource(); q.buffer = await klavierRechnen(n, sch); q.connect(bus); q.start(0); }
                let minRed = 0; const t0 = performance.now();
                const pr = oc.startRendering();
                // Reduktion während des Renderns lässt sich offline nicht abfragen: Ein- und Ausgang vergleichen
                const outD = (await pr).getChannelData(0);
                const oc2 = new OfflineAudioContext(1, 48000, 48000);
                for (const n of noten) { const q = oc2.createBufferSource(); q.buffer = await klavierRechnen(n, sch); q.connect(oc2.destination); q.start(0); }
                const inD = (await oc2.startRendering()).getChannelData(0);
                let pi = 0, po = 0; for (let i = 0; i < inD.length; i++) { pi = Math.max(pi, Math.abs(inD[i])); po = Math.max(po, Math.abs(outD[i])); }
                aus[name] = { ein_dB: +(20*Math.log10(pi)).toFixed(1), aus_dB: +(20*Math.log10(po)).toFixed(1) };
            }
            return aus;
        }''')
        for k, v in r.items(): print(k, v)
        await b.close()
asyncio.run(main())
