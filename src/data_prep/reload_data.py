import pandas as pd
from src.tools.yaml_loader import load_yaml_file
from src.data_prep.fpl_pl_table_players import (
    get_completed_seasons_fpl,
    get_current_season_fpl,
)
from src.data_prep.actual_pl_table import (
    get_completed_seasons_actual,
    get_current_season_actual,
)
from datetime import datetime
import sys
import json


def get_current_season_start_year():
    """Get the start year of the current Premier League season."""
    today = datetime.now()
    current_year = today.year
    current_month = today.month

    if current_month >= 8:
        return current_year
    else:
        return current_year - 1


def get_season_string(season_start):
    """
    Generate a season string in the format YYYY-YY.

    Parameters
    ----------
    season_start : int
        The start year of the season.

    Returns
    -------
    season_string : str
        The season string in the format "YYYY-YY".
    """
    season_end = season_start + 1
    season_end_string = str(season_end)[-2:]
    return f"{season_start}-{season_end_string}"


def get_current_gameweek(season_string):
    """
    Fetch the latest scored gameweek from the data source.

    Parameters
    ----------
    season_string : str
        The season string in the format "YYYY-YY".

    Returns
    -------
    current_gameweek : int
        The latest gameweek number.
    """
    try:
        df = pd.read_csv(
            f"https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/{season_string}/gws/merged_gw.csv",
            encoding="utf-8",
        )
        return int(df["GW"].max())
    except Exception as e:
        print(
            f"Current data up to date: First Gameweek data not yet available. Error: {e}"
        )
        sys.exit()  # Exit the script


def check_and_update_metadata(current_gameweek):
    """
    Check if the metadata for scoring needs to be updated and update if necessary.

    Parameters
    ----------
    current_gameweek : int
        The latest gameweek number.
    """
    # Check if data updated:
    file_path = "data/scoring_meta.json"

    # Read the JSON data from the file
    with open(file_path, "r") as file:
        scoring_meta = json.load(file)

    if scoring_meta.get("scoring_data_gameweek") == current_gameweek:
        print("Model training up to date.")
        sys.exit()  # Exit the script

    # Store metadata for scoring
    file_path = "data/scoring_meta.json"
    scoring_meta = {"scoring_data_gameweek": current_gameweek}
    with open(file_path, "w") as file:
        json.dump(scoring_meta, file)
