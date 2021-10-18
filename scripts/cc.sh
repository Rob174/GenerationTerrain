#!/bin/bash
short_hash=$(git rev-parse --short HEAD)
long_hash=$(git rev-parse HEAD)
repo=$(git config --get remote.origin.url)
url=$(python -c "import os;print(os.path.splitext('${repo}')[0]+'/tree/$long_hash')")
echo "[$short_hash]($url)" | clip.exe

