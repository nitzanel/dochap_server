#!/bin/bash
cd dochap_tool
git pull origin master
cd ../
docker-compose up
