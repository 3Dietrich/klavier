# Klavier

Ein Tongeber für die Chorprobe, im Browser auf dem Handy. Für den Chor brauchte ich neben
den Noten etwas, bei dem man sich beim Spielen von Melodien und Akkorden nicht die Finger
bricht. Darum lassen sich Breite und Länge der Tasten einstellen, und der Klang reicht von
weich bis durchdringend, damit er auch in einer lauten Umgebung trägt.

**Ausprobieren:** [pankd.de/klavier](https://pankd.de/klavier/), am besten als Web-App vom
Startbildschirm. Die Noten dazu kommen aus dem [Chor-Trainer](https://github.com/3Dietrich/chortrainer).

## Was es kann

- Tastengröße je Lage (quer, hochkant) einstellbar: weiße Tasten, Breite und Länge der schwarzen.  
- Reihen übereinander per Regler, höchstens so viele, dass die weißen Tasten noch quadratisch sind;
  „Auto“ macht sie etwas länger als breit.  
- Nächste Reihe schließt an oder liegt eine Oktave, Quinte oder Quarte höher; mit „Anschließen“ springt
  sie in diesen Schritten bis kurz vor das Ende der Reihe darunter.  
- ‹ › verschieben in Halbtönen, eine Reihe kann auch mit einer schwarzen Taste beginnen.  
- Umfang von E-1 (10,3 Hz, unten mit Hz-Zahlen) bis zum höchsten Ton, der sich ohne Spiegelfrequenzen
  rechnen lässt (bei 48 kHz fis'''''' mit etwa 11,8 kHz). Was darüber oder darunter liegt, ist ausgegraut.
  Passt der ganze Umfang auf den Bildschirm, steht er in der Mitte.  
- Einstellungen schließen mit „Fertig“; solange sie offen sind, lässt sich daneben spielen.  
- Zwei Klänge, Klavier und Weich, jeweils mit Regler von rund bis scharf.  
- Mehrstimmig mit begrenzter Stimmenzahl (4 bis 16): Ist sie erreicht, weicht zuerst der älteste
  losgelassene Ton. Ein Verdichter greift erst über dem Pegel eines Einzeltons.  
- Wischen über die Tasten spielt die Töne nacheinander.  
- Ausrichtung Auto, Hoch oder Breit, auch bei gesperrter Bildschirmdrehung.  
- Fällt der Ton aus (Anruf, Bluetooth, Safari im Hintergrund), baut sich der Klang beim nächsten
  Antippen neu auf; dazu ein Knopf „Klang neu starten“.  
- Hilfemodus über „?“.

Auf dem iPhone sollte unter Bedienungshilfen „Zoomen“ aus sein: Der Dreifinger-Doppeltipp ruft sonst
die Lupe und blockiert Dreiklänge.

## Aufbau

- `index.html`: das ganze Programm in einer Datei, ohne Bibliotheken. Klang per Web Audio:
  Klaviertöne werden einmal per `OfflineAudioContext` in Puffer gerechnet (bis zu 96, von c'
  nach außen), danach nur noch abgespielt.  
- `hochladen.sh`: setzt die Versionsnummer (Datum_Uhrzeit, sichtbar in den Einstellungen) und lädt
  per sftp hoch. Der Zugang steht in `hochladen.local`, das nicht im Repo liegt.  
- `aufnahme.sh`, `analyse.py`: nimmt den Klang über das Mac-Mikrofon auf und sucht Knackser
  (Hochpass, Hüllkurve, Spitzen gegen den gleitenden Median), dazu ein Spektrogramm.  
- `test/`: Prüfungen mit Playwright (headless, WebKit und Chromium) gegen die lokale `index.html`,
  z.B. `python3 test/test_stimmen.py`. Bilder landen in `.shots/`.

## Lizenz

MIT, siehe [LICENSE](LICENSE).
