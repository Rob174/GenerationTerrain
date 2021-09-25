#!/bin/bash


script="import datetime;now = datetime.datetime.now();print(now.strftime('%A %b %d %Y'))"
date=$(python -c "$script" 2>&1)

short_hash=$(git rev-parse --short HEAD)
long_hash=$(git rev-parse HEAD)
repo_path=$(git config --get remote.origin.url)
repo_path=$(echo "${repo_path%.*}")
url="$repo_path/tree/$long_hash"
commit="[$short_hash]($url)"

printf "# $date\n$commit\n" | clip.exe