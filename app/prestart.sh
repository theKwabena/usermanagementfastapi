#!/usr/bin/env bash

#Let DB Start
python /app/backend_pre_start.py

#Run migrations
alembic upgrade head


#Create initial Data
python /app/inital_data.py