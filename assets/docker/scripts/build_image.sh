#!/usr/bin/env bash


# Run at root of repo!

set -e

lib="$1"
version="$2"
push="$3"

if [ "$lib" == "" ]; then
  echo "No service specified."
  exit 1
fi

if [ "$version" == "" ]; then
  version=$(python3 .github/parse_container_version.py "$lib")
fi

if [ "$push" == "--push" ]; then
  echo "Push enabled!"
fi

img_name=ghcr.io/biosimulators/bio-compose-server-"$lib":"$version"
latest_name=ghcr.io/biosimulators/bio-compose-server-"$lib":latest

echo "Building $lib image..."
docker build --no-cache --platform linux/amd64 -f ./"$lib"/Dockerfile-"$lib" -t "$img_name" .
echo "Built $lib image."

echo "Tagging new $lib version as latest..."
docker tag "$img_name" "$latest_name"

if [ "$push" == "--push" ]; then
  # push version to GHCR
  docker push "$img_name"

  # push newest latest to GHCR
  docker push "$latest_name"
fi

