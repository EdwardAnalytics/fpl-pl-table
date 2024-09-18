import os
import numpy as np
import pandas as pd


def load_table_data(season):
    """
    Load FPL and actual Premier League table data for a given season.

    Parameters
    ----------
    season : str
        The season to process, formatted as 'YYYY-YY'.

    Returns
    -------
    fpl_pl_table : pd.DataFrame
        FPL data for the specified season.
    actual_pl_table : pd.DataFrame
        Actual Premier League data for the specified season.
    """
    fpl_pl_table = pd.read_csv(f"data/fpl_premier_league_tables/{season}.csv")
    actual_pl_table = pd.read_csv(f"data/actual_premier_league_tables/{season}.csv")
    return fpl_pl_table, actual_pl_table


def map_team_names(fpl_pl_table, team_name_mapping):
    """
    Map FPL team names to actual Premier League team names.

    Parameters
    ----------
    fpl_pl_table : pd.DataFrame
        FPL data containing team names.
    team_name_mapping : dict
        A dictionary mapping FPL team names to actual Premier League team names.

    Returns
    -------
    fpl_pl_table : pd.DataFrame
        DataFrame with the mapped team names.
    """
    fpl_pl_table["mapped_team"] = fpl_pl_table["team"].map(team_name_mapping)
    return fpl_pl_table


def merge_tables(fpl_pl_table, actual_pl_table):
    """
    Merge FPL data with actual Premier League data.

    Parameters
    ----------
    fpl_pl_table : pd.DataFrame
        FPL data with mapped team names.
    actual_pl_table : pd.DataFrame
        Actual Premier League data.

    Returns
    -------
    merged_table : pd.DataFrame
        Merged DataFrame with both FPL and actual Premier League data.
    """
    merged_table = fpl_pl_table.merge(
        right=actual_pl_table, left_on="mapped_team", right_on="Team"
    )
    merged_table.rename(columns={"Pos": "Actual Pos"}, inplace=True)
    return merged_table


def sort_and_rank(fpl_pl_table):
    """
    Sort the FPL table by ranking metrics and assign positions.

    Parameters
    ----------
    fpl_pl_table : pd.DataFrame
        Merged FPL and Premier League data.

    Returns
    -------
    fpl_pl_table_sorted : pd.DataFrame
        DataFrame with assigned ranks based on sorting by specified metrics.
    """
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

    fpl_pl_table_sorted = fpl_pl_table.sort_values(
        by=ranking_columns, ascending=[False] * len(ranking_columns)
    )
    fpl_pl_table_sorted["Pos"] = range(1, len(fpl_pl_table_sorted) + 1)
    return fpl_pl_table_sorted.reset_index(drop=True)


def calculate_rank_difference(fpl_pl_table):
    """
    Calculate the difference between FPL and actual positions.

    Parameters
    ----------
    fpl_pl_table : pd.DataFrame
        DataFrame with FPL and actual positions.

    Returns
    -------
    fpl_pl_table : pd.DataFrame
        DataFrame with the calculated rank difference added as a new column.
    """
    fpl_pl_table["Difference"] = fpl_pl_table["Actual Pos"] - fpl_pl_table["Pos"]
    fpl_pl_table["Difference"] = np.where(
        fpl_pl_table["Difference"] > 0,
        fpl_pl_table["Difference"].apply(lambda x: f"⬆️ +{x}"),
        np.where(
            fpl_pl_table["Difference"] < 0,
            fpl_pl_table["Difference"].apply(lambda x: f"⬇️ {x}"),
            " ",
        ),
    )
    return fpl_pl_table


def reorder_and_rename_columns(fpl_pl_table):
    """
    Reorder and rename columns in the DataFrame.

    Parameters
    ----------
    fpl_pl_table : pd.DataFrame
        DataFrame with rank difference.

    Returns
    -------
    fpl_pl_table : pd.DataFrame
        DataFrame with reordered and renamed columns.
    """
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

    fpl_pl_table = fpl_pl_table[desired_column_order]
    fpl_pl_table.rename(columns=column_rename_mapping, inplace=True)

    # Remove 'Team Value' column if needed
    fpl_pl_table = fpl_pl_table.drop(
        columns=["Team Value (Latest GW)"], errors="ignore"
    )
    return fpl_pl_table


def join_table_data(season, team_name_mapping):
    """
    Join Fantasy Premier League (FPL) data with actual Premier League data for a specific season.

    Parameters
    ----------
    season : str
        The season to process, formatted as 'YYYY-YY'.
    team_name_mapping : dict
        A dictionary mapping FPL team names to actual Premier League team names.

    Returns
    -------
    final_table : pd.DataFrame
        A DataFrame containing the joined and processed data with rankings and differences.
    """
    # Load, map, and merge data
    fpl_pl_table, actual_pl_table = load_table_data(season)
    fpl_pl_table = map_team_names(fpl_pl_table, team_name_mapping)
    merged_table = merge_tables(fpl_pl_table, actual_pl_table)

    # Sort, rank, and calculate rank differences
    ranked_table = sort_and_rank(merged_table)
    ranked_table = calculate_rank_difference(ranked_table)

    # Reorder and rename columns
    final_table = reorder_and_rename_columns(ranked_table)

    return final_table


def get_list_of_seasons():
    """
    Retrieve a list of seasons based on the available CSV files in the FPL data folder.

    Returns
    -------
    seasons : list of str
        A list of season identifiers (e.g., '2023-24') derived from CSV file names.
    """
    folder_path = "data/fpl_premier_league_tables"
    seasons = [season.replace(".csv", "") for season in os.listdir(folder_path)]
    return seasons


def join_all_seasons(team_name_mapping):
    """
    Process and join FPL data with actual Premier League data for all available seasons.

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
        final_table = join_table_data(season, team_name_mapping)
        final_table.to_csv(
            f"data/fpl_premier_league_tables_joined/{season}.csv", index=False
        )
