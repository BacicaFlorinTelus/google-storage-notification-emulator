#!/bin/bash

docker build -t bacicaflorin/google-storage-notification-emulator:$1 .
docker push bacicaflorin/google-storage-notification-emulator:$1