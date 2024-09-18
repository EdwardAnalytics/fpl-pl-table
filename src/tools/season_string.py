def get_season_string(season_start):
    """
    Generate a season string in the format YYYY-YY.

    Parameters
    ----------
    season_start : int
        The start year of the season. Must be a four-digit integer (e.g., 2023).

    Returns
    -------
    season_string : str
        The season string in the format "YYYY-YY".

    Raises
    ------
    ValueError
        If season_start is not a four-digit integer.
    """
    # Check if the input is a valid four-digit integer
    if not (isinstance(season_start, int) and len(str(season_start)) == 4):
        raise ValueError("season_start must be a four-digit integer (e.g., 2023).")

    # Generate the season end year string (last two digits of the following year)
    season_end = season_start + 1
    season_end_string = str(season_end)[-2:]

    # Return the formatted season string
    return f"{season_start}-{season_end_string}"
