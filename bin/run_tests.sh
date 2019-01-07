#!/bin/bash

pipenv shell;
# docker run -d -p 5672:5672 rabbitmq
python -m pytest;
behave;
# docker stop