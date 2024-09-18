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
