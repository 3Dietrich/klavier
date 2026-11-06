# Klavier auf pankd.de: Text für die Projektseite

Stand 2026-11-06. Ziel: `~/Documents/pankd.de/webseite/projekte.html`, Abschnitt `<article id="klavier">`.
Die Gliederung folgt dem bestehenden Eintrag (Kopfzeile, Bilder, Absatz, „Meine Entscheidung darin“, Links, Stack).

## Kopfzeile

Nov 2026  
Web-App für die Chorprobe  
im Einsatz

## Überschrift

Klavier - ein Tongeber für den Chor

## Bilder (drei Handy-Bilder, hochkant)

Große Tasten  
Alt-Text: Hochkant mehrere Reihen Klaviertasten mit breiten Tasten, je Reihe eine Oktave ab C

Bis 10 Hz hinunter  
Alt-Text: Reihen von Tasten bis 10,3 Hz hinunter, die tiefsten Tasten mit Hertz-Zahlen beschriftet

Einstellungen, daneben wird gespielt  
Alt-Text: Offene Einstellungen mit Reglern für Tastenbreite, schwarze Tasten und Reihen, daneben die spielbare Tastatur

Das bisherige Einstellungsbild zeigt noch Knöpfe für die Reihenzahl. Neu aufnehmen mit
`.shots/homepage/bilder.py` im Klavier-Repo (Einstellungen offen, Reihen-Regler sichtbar).

## Absatz

Für den Chor brauchte ich neben den Noten einen Tongeber, bei dem man sich beim Spielen von Melodien
und Akkorden nicht die Finger bricht. Darum lassen sich Breite und Länge der Tasten einstellen, quer
wie hochkant, und der Klang reicht von weich bis durchdringend, damit er auch in einer lauten Umgebung
trägt. Ich spiele ihn vom iPhone über eine kleine Bluetooth-Box.

Die Reihen schließen lückenlos aneinander an oder liegen eine Oktave, Quinte oder Quarte
auseinander. Die Pfeile verschieben alles in Halbtönen, eine Reihe kann also auch auf Fis beginnen.
Solange die Einstellungen offen sind, bleibt die Tastatur daneben spielbar, jede Änderung ist sofort
zu hören.

## Meine Entscheidung darin

Erst die Tastengröße, dann die Klaviatur: Aus der Tastenbreite ergibt sich, wie viele Reihen
übereinander passen, höchstens so viele, dass die weißen Tasten noch mindestens quadratisch sind.
Mehrstimmig knackt nichts, weil die Zahl der Stimmen begrenzt ist und zuerst der älteste losgelassene
Ton weicht. Bricht der Ton mitten in der Probe weg, baut er sich beim nächsten Antippen selbst wieder
auf.

## Links

Ausprobieren → https://pankd.de/klavier/  
Quellcode → https://github.com/3Dietrich/klavier

## Stack

JavaScript · Web Audio (Klang selbst gerechnet, vorab in Puffer) · eine einzige HTML-Datei, ohne Bibliotheken
