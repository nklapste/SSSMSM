#!/usr/bin/env bash

echo 'Docker Login - BEGIN'
docker login -u "$DOCKER_USERNAME" -p "$DOCKER_PASSWORD"
echo 'Docker Login - END'

echo 'Docker Push - BEGIN'
docker push nklapste/ghast:$TRAVIS_TAG
echo 'Docker Push - END'