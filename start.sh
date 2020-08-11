#!/bin/sh

# Apply database migrations
echo "Apply database migrations"
./src/manager.py migrate --noinput --settings=configs.settings.local

# Create search index
echo "Create search index"
./src/manager.py search_index --create -f --settings=configs.settings.local

# Create search index
echo "Create search index"
./src/manager.py search_index --rebuild -f --settings=configs.settings.local

# Start server
echo "Starting server"
python3 ./src/manager.py runserver --settings=configs.settings.local --traceback -v 3
