import requests
from bs4 import BeautifulSoup
import pandas as pd


def fetch_html_from_wikipedia(season):
    """
    Fetch HTML content from a Wikipedia page for the given season.

    Parameters
    ----------
    season : str
        The season string in the format "YYYY-YY".

    Returns
    -------
    html_content : str
        The HTML content of the Wikipedia page.

    Raises
    ------
    requests.exceptions.RequestException
        If the HTTP request to fetch the page fails.
    """
    url = f"https://en.wikipedia.org/wiki/{season}_Premier_League"
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses
    return response.content


def parse_table_from_html(html_content):
    """
    Parse tables from the given HTML content and return as DataFrames.

    Parameters
    ----------
    html_content : str
        The HTML content to parse.

    Returns
    -------
    df : pd.DataFrame
        A DataFrame containing the Premier League table data.

    Raises
    ------
    ValueError
        If no table with the columns 'Pos', 'Team', and 'Pts' is found.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    tables = soup.find_all("table", {"class": "wikitable"})

    for table in tables:
        df = pd.read_html(str(table))[0]
        if set(["Pos", "Pts"]).issubset(df.columns):
            if "Teamvte" in df.columns:
                df.rename(columns={"Teamvte": "Team"}, inplace=True)

            df = df[["Pos", "Team", "Pts"]]
            df["Team"] = df["Team"].str.replace(" (C)", "", case=False)
            df["Team"] = df["Team"].str.replace(" (R)", "", case=False)
            df = df.replace(r"\[.*?\]", "", regex=True).applymap(
                lambda x: x.strip() if isinstance(x, str) else x
            )
            return df

    raise ValueError("No table with the columns Pos, Team, and Pts was found.")


def get_actual_premier_league_table(season):
    """
    Get and process the Premier League table for the given season.

    Parameters
    ----------
    season : str
        The season string in the format "YYYY-YY".

    Returns
    -------
    df : pd.DataFrame
        A DataFrame containing the processed Premier League table data.
    """
    html_content = fetch_html_from_wikipedia(season)
    return parse_table_from_html(html_content)


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


def save_season_data(season_start, file_path):
    """
    Fetch and save Premier League table data for a given season.

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
    season_df = get_actual_premier_league_table(season=season_string)
    season_df.to_csv(file_path, index=False)


def get_completed_seasons_actual(first_season_start, latest_season_start):
    """
    Fetch and save Premier League table data for a range of seasons.

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
        save_season_data(
            season_start,
            f"data/actual_premier_league_tables/{get_season_string(season_start)}.csv",
        )


def get_current_season_actual(season_start):
    """
    Fetch and save Premier League table data for the current season.

    Parameters
    ----------
    season_start : int
        The start year of the current season.

    Returns
    -------
    None
    """
    save_season_data(
        season_start,
        f"data/actual_premier_league_tables/{get_season_string(season_start)}.csv",
    )
