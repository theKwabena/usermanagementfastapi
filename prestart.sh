#!/usr/bin/env bash

#Let DB Start
# python /home/app/app/backend_pre_start.py
python -m app.backend_pre_start
#Run migrations
alembic upgrade head


#Create initial Data
# python /home/app/app/initial_data.py
python -m app.initial_data
