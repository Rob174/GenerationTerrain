#!/usr/bin/env bash
script="import datetime;now = datetime.datetime.now();print(now.strftime('%A %b %d %Y'))"
python -c "$script" 2>&1 | clip.exe