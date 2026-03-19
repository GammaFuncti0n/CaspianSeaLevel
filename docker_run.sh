#!/bin/bash

source credentials

docker run -it -d \
		--name "$CONTAINER_NAME" \
		-p "$JUPYTER_PORT":8888 \
		-v "$HOST_WORKDIR":"$CONTAINER_WORKDIR" \
		"$IMAGE_NAME"