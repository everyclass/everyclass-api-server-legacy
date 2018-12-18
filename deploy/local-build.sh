#!/usr/bin/env bash
docker build . -t everyclass-api-server:$(git describe --tag)