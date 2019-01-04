#!/bin/bash

docker build -t transaction-service .;
docker run -p 5002:5000 -it transaction-service;