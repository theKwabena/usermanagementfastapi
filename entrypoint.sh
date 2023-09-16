#!/bin/bash

# Run your initialization scripts
#Let DB Start
echo "Checking db status..."
python -m app.backend_pre_start

echo "Applying migrations..."
alembic upgrade head

echo "Seeding database..."
python -m app.initial_data

echo "Starting FastAPI server..."
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Keep the container running
tail -f /dev/null
