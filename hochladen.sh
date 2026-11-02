#!/bin/zsh
# Klavier auf pankd.de/klavier hochladen (@dd 20261102).
# Setzt vorher VERSION in index.html auf Datum_Uhrzeit (z.B. 20261102_2240); die Nummer steht
# in den Einstellungen oben neben dem Titel und zeigt, ob das iPhone schon die neue Fassung hat.
set -e
cd "${0:A:h}"
ver=$(date +%Y%m%d_%H%M)
sed -i '' -E "s/^const VERSION = '[0-9_]+';/const VERSION = '$ver';/" index.html
grep -q "const VERSION = '$ver';" index.html
cp -p index.html ~/Documents/pankd.de/webseite/klavier/index.html
printf -- 'put -p index.html pankd.de/httpdocs/klavier/index.html\n' | sftp -q -o BatchMode=yes -o ConnectTimeout=15 \
    -b - "$ZIEL" >/dev/null
# Kontrolle: liefert der Server die neue Nummer aus?
if curl -s "https://pankd.de/klavier/?$(date +%s)" | grep -q "const VERSION = '$ver';"; then
    echo "online: $ver"
else
    echo "FEHLER: Server liefert $ver nicht aus" >&2; exit 1
fi
