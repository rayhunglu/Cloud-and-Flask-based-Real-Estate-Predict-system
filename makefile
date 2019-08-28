#!/bin/bash
if [ -n $(sudo docker ps | grep mlflask | awk  -F ' ' '{print $1}') ]; then
    echo "container id not empty, stop it firstly"
    sudo docker stop $(sudo docker ps | grep mlflask | awk  -F ' ' '{print $1}')
else
    echo "empty container id"
fi
sudo docker build --pull -t mlflask .
sudo docker run -p 5000:5000 mlflask
