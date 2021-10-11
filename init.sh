#!/bin/bash

echo Create and start mongodb docker service
docker-compose -f docker/docker-compose.yml up --detach
python run.py create-db-collections
python run.py process-data-from-file-to-db  words_clean.txt
python run.py runserver