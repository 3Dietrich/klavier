#!/usr/bin/env python3
"""Knackser in einer Aufnahme finden (@dd 20261102).

Knacksen vom iPhone (Aussetzer im Audio-Puffer) zeigt sich als kurzer, breitbandiger Spitzenwert im
Hochton, viel steiler als ein Klavieranschlag. Gesucht wird darum im Bereich über 6 kHz: Hüllkurve in
1-ms-Fenstern, verglichen mit ihrem gleitenden Median über 0,3 s. Liegt ein Fenster weit darüber und
fällt sofort wieder ab, zählt es als Knackser. Ausgabe: Liste mit Zeitpunkten + Spektrogramm-Bild.
Aufruf: python3 analyse.py aufnahme.wav
"""
import subprocess, sys, wave
import numpy as np
from scipy.signal import butter, medfilt, sosfiltfilt

datei = sys.argv[1]
w = wave.open(datei)
rate = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768
dauer = len(x) / rate
spitze = 20 * np.log10(np.abs(x).max() + 1e-12)
print(f'{datei}\n{dauer:.1f} s, Spitze {spitze:.1f} dBFS')
if spitze < -40:
    print('Sehr leise: Box lauter stellen oder Mikrofon näher. Analyse trotzdem.')

hoch = sosfiltfilt(butter(4, 6000, 'highpass', fs=rate, output='sos'), x)
fenster = rate // 1000                              # 1 ms
n = len(hoch) // fenster
huelle = np.sqrt((hoch[:n * fenster].reshape(n, fenster) ** 2).mean(axis=1))
grund = medfilt(huelle, 301)                        # 0,3 s gleitender Median
grund = np.maximum(grund, np.median(huelle) * 0.5 + 1e-6)
verh = huelle / grund
# Knackser: mindestens 8-fach über dem Umfeld, nach höchstens 4 ms wieder unten
kandidaten = np.where(verh > 8)[0]
treffer, letzter = [], -100
for i in kandidaten:
    if i - letzter < 20:                            # innerhalb 20 ms nur einmal zählen
        continue
    if verh[i + 1:i + 5].min(initial=0) < 3:
        treffer.append(i)
        letzter = i

print(f'Knackser: {len(treffer)}' + (f' (etwa {len(treffer) / dauer * 60:.0f} pro Minute)' if treffer else ''))
for i in treffer[:60]:
    print(f'  {i / 1000:7.3f} s   {20 * np.log10(verh[i]):5.1f} dB über Umfeld')
if len(treffer) > 60:
    print(f'  … und {len(treffer) - 60} weitere')

bild = datei.rsplit('.', 1)[0] + '_spektrum.png'
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', datei, '-lavfi',
                'showspectrumpic=s=1600x600:legend=1:scale=log:fscale=lin', bild], check=True)
print(f'Spektrogramm: {bild}')
