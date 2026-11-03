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
        pg = await b.new_page()
        await pg.goto(SEITE)
        r = await pg.evaluate('''async () => {
            const aus = {};
            for (const sch of [0, 30, 60, 100]) {
                let mx = 0, wo = 0;
                for (let n = 24; n <= 100; n += 2) {
                    const b = await klavierRechnen(n, sch); const d = b.getChannelData(0);
                    let p = 0; for (let i = 0; i < d.length; i++) p = Math.max(p, Math.abs(d[i]));
                    if (p > mx) { mx = p; wo = n; }
                }
                aus['klavier' + sch] = [+(20 * Math.log10(mx)).toFixed(1), wo];
            }
            // Weich: eine Stimme offline nachbauen
            for (const sch of [0, 30, 60, 100]) {
                let mx = 0;
                for (const n of [36, 48, 60, 72, 84]) {
                    const oc = new OfflineAudioContext(1, 24000, 48000), x = sch / 100, f = freq(n);
                    const g = oc.createGain(), sat = oc.createWaveShaper(); sat.curve = kurve(x); g.connect(sat).connect(oc.destination);
                    const o1 = oc.createOscillator(), o2 = oc.createOscillator(), o3 = oc.createOscillator();
                    const m1 = oc.createGain(), m2 = oc.createGain(), m3 = oc.createGain(), lp = oc.createBiquadFilter();
                    o1.frequency.value = f; m1.gain.value = 1 - 0.4 * x;
                    o2.type = 'triangle'; o2.frequency.value = f * 2; m2.gain.value = 0.1 + 0.1 * x + 0.5 * Math.max(0, Math.min(1, (200 - f) / 130));
                    o3.type = 'sawtooth'; o3.frequency.value = f; m3.gain.value = 0.7 * x;
                    lp.type = 'lowpass'; lp.frequency.value = Math.min(16000, f * (2 + 12 * x));
                    o1.connect(m1).connect(g); o2.connect(m2).connect(g); o3.connect(m3).connect(lp).connect(g);
                    g.gain.value = 0.3 + 0.15 * x; [o1, o2, o3].forEach(o => o.start(0));
                    const d = (await oc.startRendering()).getChannelData(0);
                    for (let i = 0; i < d.length; i++) mx = Math.max(mx, Math.abs(d[i]));
                }
                aus['weich' + sch] = +(20 * Math.log10(mx)).toFixed(1);
            }
            return aus;
        }''')
        print(r)
        await b.close()
asyncio.run(main())
