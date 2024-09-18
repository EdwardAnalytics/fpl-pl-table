#!/bin/bash

# Pull the latest changes from the remote repository
git pull

# Set PYTHONPATH and run the Python script
export PYTHONPATH=$(pwd)
python scripts/python/refresh_data.py

# Get the score GW
gameweek=$(python -c "import json; import sys; print(json.load(open('data/scoring_meta.json'))['scoring_data_gameweek'])")

# Add all changes to the staging area
git add .

# Commit changes with a dynamic message
git commit -m "Rescoring for Gameweek $gameweek"

# Push changes to the current branch
git push

#Print
echo "Retrained for: Gameweek $gameweek"