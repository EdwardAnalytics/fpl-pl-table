import numpy as np
import pandas as pd
import os


def join_table_data(season, team_name_mapping):
    """
    Join Fantasy Premier League (FPL) data with actual Premier League data for a specific season.

    This function loads FPL and actual Premier League tables for a given season, maps team names,
    merges the data, sorts by various performance metrics, calculates rank differences, and reorders
    and renames columns for final output.

    Parameters
    ----------
    season : str
        The season to process, formatted as 'YYYY-YY'.
    team_name_mapping : dict
        A dictionary mapping FPL team names to actual Premier League team names.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the joined and processed data with rankings and differences.
    """
    # Load tables
    fpl_pl_table = pd.read_csv(f"data/fpl_premier_league_tables/{season}.csv")
    actual_pl_table = pd.read_csv(f"data/actual_premier_league_tables/{season}.csv")

    # Map team name variations to join
    fpl_pl_table["mapped_team"] = fpl_pl_table["team"].map(team_name_mapping)

    # Join tables and rename position column
    fpl_pl_table = fpl_pl_table.merge(
        right=actual_pl_table, left_on="mapped_team", right_on="Team"
    )
    fpl_pl_table.rename(columns={"Pos": "Actual Pos"}, inplace=True)

    # Define the columns to rank by, in the specified order
    ranking_columns = [
        "total_points",
        "goals_scored",
        "assists",
        "clean_sheets",
        "yellow_cards",
        "red_cards",
        "goals_conceded",
        "own_goals",
        "penalties_missed",
        "penalties_saved",
        "saves",
        "bonus_points",
        "team",
    ]

    # Sort the DataFrame by the ranking columns in descending order
    fpl_pl_table_sorted = fpl_pl_table.sort_values(
        by=ranking_columns, ascending=[False] * len(ranking_columns)
    )

    # Assign ranks based on the sorted DataFrame
    fpl_pl_table_sorted["Pos"] = range(1, len(fpl_pl_table_sorted) + 1)

    # Reset index
    fpl_pl_table_sorted.reset_index(drop=True, inplace=True)

    # Get rank difference
    fpl_pl_table_sorted["Difference"] = (
        fpl_pl_table_sorted["Actual Pos"] - fpl_pl_table_sorted["Pos"]
    )
    fpl_pl_table_sorted["Difference"] = np.where(
        fpl_pl_table_sorted["Difference"] > 0,
        fpl_pl_table_sorted["Difference"].apply(lambda x: f"⬆️ +{x}"),
        np.where(
            fpl_pl_table_sorted["Difference"] < 0,
            fpl_pl_table_sorted["Difference"].apply(lambda x: f"⬇️ {x}"),
            " ",
        ),
    )

    # Reorder columns
    desired_column_order = [
        "Pos",
        "team",
        "total_points",
        "Actual Pos",
        "Difference",
        "gk_points",
        "def_points",
        "mid_points",
        "fwd_points",
        "goals_scored",
        "assists",
        "clean_sheets",
        "yellow_cards",
        "red_cards",
        "goals_conceded",
        "own_goals",
        "penalties_missed",
        "penalties_saved",
        "saves",
        "bonus_points",
        "value_latest_gw",
    ]

    # Reorder the DataFrame columns
    fpl_pl_table_sorted = fpl_pl_table_sorted[desired_column_order]

    # Rename columns
    column_rename_mapping = {
        "Pos": "Pos",
        "team": "Team",
        "total_points": "Points",
        "Actual Pos": "Actual Pos",
        "Difference": "Difference",
        "gk_points": "GK Points",
        "def_points": "DEF Points",
        "mid_points": "MID Points",
        "fwd_points": "FWD Points",
        "goals_scored": "Goals Scored",
        "assists": "Assists",
        "clean_sheets": "Clean Sheets",
        "yellow_cards": "Yellow Cards",
        "red_cards": "Red Cards",
        "goals_conceded": "Goals Conceded",
        "own_goals": "Own Goals",
        "penalties_missed": "Penalties Missed",
        "penalties_saved": "Penalties Saved",
        "saves": "Saves",
        "bonus_points": "Bonus Points",
        "value_latest_gw": "Team Value (Latest GW)",
    }

    # Rename the columns using the mapping
    fpl_pl_table_sorted.rename(columns=column_rename_mapping, inplace=True)

    # Remove value column
    # Some teams are inflated due to red flags/loaned out/sold players etc.
    fpl_pl_table_sorted = fpl_pl_table_sorted.drop(columns=["Team Value (Latest GW)"])

    return fpl_pl_table_sorted


def get_list_of_seasons():
    """
    Retrieve a list of seasons based on the available CSV files in the FPL data folder.

    Returns
    -------
    list of str
        A list of season identifiers (e.g., '2023-24') derived from CSV file names.
    """
    # Path to the folder containing the CSV files
    folder_path = "data/fpl_premier_league_tables"

    # List all files in the folder
    seasons = os.listdir(folder_path)
    seasons = [season.replace(".csv", "") for season in seasons]
    return seasons


def join_all_seasons(team_name_mapping):
    """
    Process and join FPL data with actual Premier League data for all available seasons.

    This function retrieves a list of all seasons and applies the join_table_data function
    to each season using the provided team name mapping. The resulting data for each season
    is saved to a CSV file.

    Parameters
    ----------
    team_name_mapping : dict
        A dictionary mapping FPL team names to actual Premier League team names.

    Returns
    -------
    None
    """
    seasons = get_list_of_seasons()
    for season in seasons:
        fpl_pl_table_sorted = join_table_data(
            season=season, team_name_mapping=team_name_mapping
        )
        fpl_pl_table_sorted.to_csv(
            f"data/fpl_premier_league_tables_joined/{season}.csv", index=False
        )
