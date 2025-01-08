#!/usr/bin/env bash

set -e

lib="$1"
version="$2"
# gh_username="$3"
explicit_version=1

if [ "$version" == "" ]; then
  version=$(cat "$lib"/.VERSION)
  explicit_version=0
fi

img_name=ghcr.io/biosimulators/bio-compose-server-"$lib"
current_img="$img_name":"$version"
latest_img="$img_name":latest

# push current img version
docker push "$current_img"

# push newest latest to GHCR
docker tag "$current_img" "$latest_img"
docker push "$latest_img"

# handle version
if [ "$lib" == "base" ]; then
  VERSION_FILE=./assets/.BASE_VERSION
else
  VERSION_FILE=./"$lib"/.VERSION
fi

if [ "$explicit_version" == 1 ]; then
  echo "Updating internal version of $lib with specified version."
  echo "$version" > "$VERSION_FILE"
fi

echo "Updated version: $version"
