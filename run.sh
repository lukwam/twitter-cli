#!/bin/sh

sudo docker run -it --rm \
    -e GOOGLE_APPLICATION_CREDENTIALS=/usr/src/service_account.json \
    -e PATH=/usr/src:$PATH \
    -v $(pwd):/usr/src \
    -w /usr/src \
    twitter-cli \
    "$*"
