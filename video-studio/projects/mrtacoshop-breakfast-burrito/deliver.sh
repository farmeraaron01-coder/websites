#!/usr/bin/env bash
# Delivery encode + split, so the hand-off is reproducible.
#
# edit/final.mp4 is ~8.3 Mbps and 170 MB, which is more than YouTube will keep
# and more than the chat channel will carry. This re-encodes the picture at
# 5.4 Mbps (visually indistinguishable at 1080p24 for this material) and
# STREAM-COPIES the audio, so the mix never takes a second lossy generation.
#
# The split exists only because the file has to travel through chat, which caps
# a single attachment. 27 MiB parts; recombine on Windows with:
#   cmd /c copy /b part00+part01+part02+part03+part04 Albertos...mp4
set -euo pipefail
cd "$(dirname "$0")"

SRC=edit/final.mp4
OUT=edit/deliver/AlbertosBreakfastBurrito_1080p.mp4
mkdir -p edit/deliver
rm -f "$OUT" "$OUT".part*

ffmpeg -y -v error -stats -i "$SRC" \
    -c:v libx264 -preset slow -b:v 5400k -maxrate 7000k -bufsize 12000k \
    -pix_fmt yuv420p -c:a copy -movflags +faststart "$OUT"

split -b 27M -d -a 2 "$OUT" "$OUT".part
ls -l "$OUT" "$OUT".part*
md5sum "$OUT"
