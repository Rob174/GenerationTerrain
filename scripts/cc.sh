#!/bin/bash
short_hash=$(git rev-parse --short HEAD)
long_hash=$(git rev-parse HEAD)
url="https://github.com/Rob174/GenerationTerrain/tree/$long_hash"
echo "[$short_hash]($url)" | clip.exe

