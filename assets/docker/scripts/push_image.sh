#!/usr/bin/env bash

set -e

lib="$1"
version="$2"

img_name=ghcr.io/biosimulators/bio-compose-server-"$lib"
current_img="$img_name":"$version"
latest_img="$img_name":latest

# push current img version
docker push "$current_img"

# push newest latest to GHCR
docker tag "$current_img" "$latest_img"
docker push "$latest_img"

