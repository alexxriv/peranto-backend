#! /usr/bin/env bash
rm example.db
rm /alembic/versions/*
rm -rf /alembic/versions/__pycache__


# Let the DB start
python ./app/backend_pre_start.py

# Run migrations

alembic revision --autogenerate -m "first migration"

alembic upgrade head


# Create initial data in DB
python ./app/initial_data.py