#!/bin/bash
git pull origin master
cd dochap_tool
git pull origin master
cd ../
docker-compose build
docker-compose down
docker-compose up -d
