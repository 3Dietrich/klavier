# klavier: Einstiegs-Karte

Web-Klavier fürs iPhone (Chorprobe, Ausgabe über Bose SoundLink Mini), live auf `pankd.de/klavier/`.
Stand und offene Fäden: `~/brain/themen/klavier.md`.

- **Einzige Quelle ist `index.html` hier.** Die Kopie in `~/Documents/pankd.de/webseite/klavier/` schreibt
  `hochladen.sh` mit; dort nie ändern.  
- Nach jeder Änderung `./hochladen.sh` (prüft, ob der Server die neue Version ausliefert), dann committen.
  Bis @dd „released“ sagt, ohne Rückfrage hochladen (@dd 2026-11-02).  
- Repo ist öffentlich (github.com/3Dietrich/klavier): keine Zugangsdaten. Server und Schlüssel stehen in
  `hochladen.local` (gitignoriert). Vor jedem Push Skill `github` (fetch, nie force).  
- Vorstellung auf der Homepage: `~/Documents/pankd.de/webseite/projekte.html#klavier`, Bilder
  `bilder/klavier_*.webp` (erzeugt mit `.shots/homepage/bilder.py`), hochladen dort mit `abgleich.py`.  
- Tests: `python3 test/test_*.py` (Playwright headless). Prüfbilder und Aufnahmen nach `.shots/` (gitignoriert).  
- Oberfläche folgt dem Skill `oberflaeche` (große Trefferflächen, Tab/Esc, ?-Hilfe).
