import pandas as pd
import numpy as np


def fetch_data_from_url(url, encoding="ISO-8859-1"):
    """
    Fetch data from a URL and return a DataFrame.

    Parameters
    ----------
    url : str
        The URL to fetch data from.
    encoding : str, optional
        The encoding to use for reading the data (default is 'ISO-8859-1').

    Returns
    -------
    df : pd.DataFrame
        The DataFrame containing the fetched data.
    """
    return pd.read_csv(url, encoding=encoding)


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


def process_fpl_data(df, season_year):
    """
    Process the FPL data by merging and calculating columns.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing raw FPL data.
    season_year : str
        The season year in the format "YYYY-YY".

    Returns
    -------
    summary_df : pd.DataFrame
        A DataFrame containing the processed and aggregated FPL data.
    """
    if "position" not in df.columns:
        df_players = fetch_data_from_url(
            f"https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/{season_year}/players_raw.csv"
        )
        df_players = df_players[["id", "team", "element_type"]]
        df = df.merge(df_players, left_on="element", right_on="id", how="left")

        df_teams = fetch_data_from_url(
            "https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/master_team_list.csv"
        )
        df_teams = df_teams[df_teams["season"] == season_year]
        df = df.merge(df_teams, on="team", how="left")

        df.rename(columns={"team": "team_id", "team_name": "team"}, inplace=True)

        df["position"] = (
            df["element_type"]
            .map({1: "GK", 2: "DEF", 3: "MID", 4: "FWD"})
            .fillna("Unknown")
        )

    df["gk_points"] = df["total_points"].where(df["position"] == "GK", 0)
    df["def_points"] = df["total_points"].where(df["position"] == "DEF", 0)
    df["mid_points"] = df["total_points"].where(df["position"] == "MID", 0)
    df["fwd_points"] = df["total_points"].where(df["position"] == "FWD", 0)

    summary_df = (
        df.groupby("team")
        .agg(
            total_points=("total_points", "sum"),
            gk_points=("gk_points", "sum"),
            def_points=("def_points", "sum"),
            mid_points=("mid_points", "sum"),
            fwd_points=("fwd_points", "sum"),
            goals_scored=("goals_scored", "sum"),
            assists=("assists", "sum"),
            clean_sheets=("clean_sheets", "sum"),
            yellow_cards=("yellow_cards", "sum"),
            red_cards=("red_cards", "sum"),
            goals_conceded=("goals_conceded", "sum"),
            own_goals=("own_goals", "sum"),
            penalties_missed=("penalties_missed", "sum"),
            penalties_saved=("penalties_saved", "sum"),
            saves=("saves", "sum"),
            bonus_points=("bonus", "sum"),
        )
        .reset_index()
    )

    max_gw = df["GW"].max()
    df_max_gw = df[df["GW"] == max_gw]
    value_max_gw_sum = df_max_gw.groupby("team")["value"].sum().reset_index()
    summary_df = summary_df.merge(value_max_gw_sum, on="team", how="left")
    summary_df.rename(columns={"value": "value_latest_gw"}, inplace=True)

    summary_df = summary_df.sort_values(by="total_points", ascending=False).reset_index(
        drop=True
    )

    player_df = (
        df.groupby("name")
        .agg(
            total_points=("total_points", "sum"),
            goals_scored=("goals_scored", "sum"),
            assists=("assists", "sum"),
            clean_sheets=("clean_sheets", "sum"),
            yellow_cards=("yellow_cards", "sum"),
            red_cards=("red_cards", "sum"),
            goals_conceded=("goals_conceded", "sum"),
            own_goals=("own_goals", "sum"),
            penalties_missed=("penalties_missed", "sum"),
            penalties_saved=("penalties_saved", "sum"),
            saves=("saves", "sum"),
            bonus_points=("bonus", "sum"),
        )
        .reset_index()
    )

    player_df = player_df.sort_values(by="total_points", ascending=False).reset_index(
        drop=True
    )

    # Perform the left join with player_df on 'name'
    player_df = player_df.merge(
        df_max_gw[["name", "position", "team"]], on="name", how="left"
    )

    column_order = [
        "name",
        "team",
        "total_points",
        "position",
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
    ]

    # Reorder the DataFrame columns
    player_df = player_df[column_order]

    # Create a copy of the DataFrame with the "team" column set to "All Teams"
    player_df_all_teams = player_df.copy()
    player_df_all_teams["team"] = "All Teams"

    # Stack the original and the modified DataFrame on top of each other
    player_df = pd.concat([player_df, player_df_all_teams], ignore_index=True)

    # Remove _ from names
    player_df["name"] = player_df["name"].str.replace("_", " ")

    return summary_df, player_df


def get_fpl_player_data_aggregated(season_year):
    """
    Fetch and process FPL player data for the given season year.

    Parameters
    ----------
    season_year : str
        The season year in the format "YYYY-YY".

    Returns
    -------
    summary_df : pd.DataFrame
        A DataFrame containing the aggregated FPL player data.
    """
    vaastav_url = f"https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/{season_year}/gws/merged_gw.csv"
    df = fetch_data_from_url(vaastav_url)
    summary_df, player_df = process_fpl_data(df, season_year)
    return summary_df, player_df


def save_season_data(season_start, file_path_team, file_path_player):
    """
    Fetch and save FPL data for a given season.

    Parameters
    ----------
    season_start : int
        The start year of the season.
    file_path : str
        The file path where the CSV should be saved.

    Returns
    -------
    None
    """
    season_string = get_season_string(season_start)
    season_df, player_df = get_fpl_player_data_aggregated(season_year=season_string)
    season_df.to_csv(file_path_team, index=False)
    player_df.to_csv(file_path_player, index=False)


def get_completed_seasons_fpl(first_season_start, latest_season_start):
    """
    Fetch and save FPL data for a range of seasons.

    Parameters
    ----------
    first_season_start : int
        The start year of the first season in the range.
    latest_season_start : int
        The start year of the latest season in the range.

    Returns
    -------
    None
    """
    for season_start in range(first_season_start, latest_season_start + 1):
        file_path_team = (
            f"data/fpl_premier_league_tables/{get_season_string(season_start)}.csv"
        )
        file_path_player = (
            f"data/fpl_premier_league_player_data/{get_season_string(season_start)}.csv"
        )
        save_season_data(
            season_start=season_start,
            file_path_team=file_path_team,
            file_path_player=file_path_player,
        )


def get_current_season_fpl(season_start):
    """
    Fetch and save FPL data for the current season.

    Parameters
    ----------
    season_start : int
        The start year of the current season.

    Returns
    -------
    None
    """
    file_path_team = (
        f"data/fpl_premier_league_tables/{get_season_string(season_start)}.csv"
    )
    file_path_player = (
        f"data/fpl_premier_league_player_data/{get_season_string(season_start)}.csv"
    )
    save_season_data(
        season_start=season_start,
        file_path_team=file_path_team,
        file_path_player=file_path_player,
    )
