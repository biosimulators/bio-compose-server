#!/usr/bin/env bash

img="$1"  # which lib container to run (base, api, compose_worker)
version="$2"

if [ "$version" == "" ]; then
  version=latest
fi

# docker run --platform linux/amd64 -it -p 8000:3001 ghcr.io/biosimulators/bio-check-"$lib"

docker run --name "$img" --platform linux/amd64 --entrypoint /usr/bin/env -it "$img":"$version" bash