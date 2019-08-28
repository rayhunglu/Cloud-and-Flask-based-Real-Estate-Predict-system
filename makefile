#!/bin/bash
if [ -n $(docker ps | grep flask | awk  -F ' ' '{print $1}') ]; then
    echo "container id not empty, stop it firstly"
    docker stop $(docker ps | grep flask | awk  -F ' ' '{print $1}')
else
    echo "empty container id"
fi
docker build --pull -t flask .
docker run -p 5000:5000 flask
