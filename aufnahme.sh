#!/bin/zsh
# Klang über das MacBook-Air-Mikrofon aufnehmen und auf Knackser untersuchen (@dd 20261102).
# Aufruf: ./aufnahme.sh [Sekunden, Standard 30] [Name]
# Ablage: ~/alltag/.shots/klavier/aufnahmen/JJJJMMTT_HHMMSS[_name].wav + _spektrum.png
set -e
cd "${0:A:h}"
sek=${1:-30}
ziel=~/alltag/.shots/klavier/aufnahmen
mkdir -p $ziel
datei=$ziel/$(date +%Y%m%d_%H%M%S)${2:+_$2}.wav
ffmpeg -hide_banner -loglevel error -f avfoundation -i ":MacBook Air-Mikrofon" -t $sek -ac 1 -ar 48000 -y $datei
python3 -I ./analyse.py $datei
