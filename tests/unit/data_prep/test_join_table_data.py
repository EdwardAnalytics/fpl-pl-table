import pytest
import pandas as pd
from unittest.mock import patch
from src.data_prep.join_table_data import (
    load_table_data,
    map_team_names,
    merge_tables,
    sort_and_rank,
    calculate_rank_difference,
    reorder_and_rename_columns,
    join_all_seasons,
    join_table_data,
    get_list_of_seasons,
)


def test_load_table_data(mocker):
    # Sample data to use for testing
    fpl_data = pd.DataFrame({"Team": ["Team A", "Team B"], "Points": [70, 65]})
    actual_data = pd.DataFrame({"Team": ["Team A", "Team B"], "Points": [68, 64]})

    # Mock the pd.read_csv function to return the sample data
    mocker.patch("pandas.read_csv", side_effect=[fpl_data, actual_data])

    # Call the function with a sample season
    fpl_pl_table, actual_pl_table = load_table_data("2023-24")

    # Assertions to check if the returned data matches the sample data
    pd.testing.assert_frame_equal(fpl_pl_table, fpl_data)
    pd.testing.assert_frame_equal(actual_pl_table, actual_data)


def test_map_team_names():
    # Sample data to use for testing
    fpl_data = pd.DataFrame({"team": ["Team A", "Team B"]})
    team_name_mapping = {"Team A": "Actual Team A", "Team B": "Actual Team B"}
    expected_data = pd.DataFrame(
        {
            "team": ["Team A", "Team B"],
            "mapped_team": ["Actual Team A", "Actual Team B"],
        }
    )

    # Call the function with the sample data
    result = map_team_names(fpl_data, team_name_mapping)

    # Assertions to check if the returned data matches the expected data
    pd.testing.assert_frame_equal(result, expected_data)


def test_merge_tables():
    # Sample data to use for testing
    fpl_data = pd.DataFrame(
        {
            "team": ["Team A", "Team B"],
            "mapped_team": ["Actual Team A", "Actual Team B"],
            "Points": [70, 65],
        }
    )
    actual_data = pd.DataFrame(
        {"Team": ["Actual Team A", "Actual Team B"], "Pos": [1, 2], "Points": [68, 64]}
    )
    expected_data = pd.DataFrame(
        {
            "team": ["Team A", "Team B"],
            "mapped_team": ["Actual Team A", "Actual Team B"],
            "Points_x": [70, 65],
            "Team": ["Actual Team A", "Actual Team B"],
            "Actual Pos": [1, 2],
            "Points_y": [68, 64],
        }
    )

    # Call the function with the sample data
    result = merge_tables(fpl_data, actual_data)

    # Assertions to check if the returned data matches the expected data
    pd.testing.assert_frame_equal(result, expected_data)


def test_sort_and_rank():
    # Sample data to use for testing
    fpl_data = pd.DataFrame(
        {
            "team": ["Team A", "Team B", "Team C"],
            "total_points": [100, 90, 95],
            "goals_scored": [50, 45, 48],
            "assists": [30, 25, 28],
            "clean_sheets": [15, 10, 12],
            "yellow_cards": [5, 7, 6],
            "red_cards": [1, 2, 1],
            "goals_conceded": [20, 25, 22],
            "own_goals": [0, 1, 0],
            "penalties_missed": [1, 0, 1],
            "penalties_saved": [2, 1, 2],
            "saves": [100, 90, 95],
            "bonus_points": [10, 8, 9],
        }
    )
    expected_data = pd.DataFrame(
        {
            "team": ["Team A", "Team C", "Team B"],
            "total_points": [100, 95, 90],
            "goals_scored": [50, 48, 45],
            "assists": [30, 28, 25],
            "clean_sheets": [15, 12, 10],
            "yellow_cards": [5, 6, 7],
            "red_cards": [1, 1, 2],
            "goals_conceded": [20, 22, 25],
            "own_goals": [0, 0, 1],
            "penalties_missed": [1, 1, 0],
            "penalties_saved": [2, 2, 1],
            "saves": [100, 95, 90],
            "bonus_points": [10, 9, 8],
            "Pos": [1, 2, 3],
        }
    ).reset_index(drop=True)

    # Call the function with the sample data
    result = sort_and_rank(fpl_data)

    # Assertions to check if the returned data matches the expected data
    pd.testing.assert_frame_equal(result, expected_data)


def test_calculate_rank_difference():
    # Sample data to use for testing
    fpl_data = pd.DataFrame(
        {
            "team": ["Team A", "Team B", "Team C"],
            "Pos": [1, 2, 3],
            "Actual Pos": [2, 1, 3],
        }
    )
    expected_data = pd.DataFrame(
        {
            "team": ["Team A", "Team B", "Team C"],
            "Pos": [1, 2, 3],
            "Actual Pos": [2, 1, 3],
            "Difference": ["⬆️ +1", "⬇️ -1", " "],
        }
    )

    # Call the function with the sample data
    result = calculate_rank_difference(fpl_data)

    # Assertions to check if the returned data matches the expected data
    pd.testing.assert_frame_equal(result, expected_data)


def test_reorder_and_rename_columns():
    # Sample data to use for testing
    fpl_data = pd.DataFrame(
        {
            "Pos": [1, 2],
            "team": ["Team A", "Team B"],
            "total_points": [100, 90],
            "Actual Pos": [1, 2],
            "Difference": [" ", " "],
            "gk_points": [10, 9],
            "def_points": [20, 18],
            "mid_points": [30, 27],
            "fwd_points": [40, 36],
            "goals_scored": [50, 45],
            "assists": [25, 22],
            "clean_sheets": [15, 12],
            "yellow_cards": [5, 7],
            "red_cards": [1, 2],
            "goals_conceded": [20, 25],
            "own_goals": [0, 1],
            "penalties_missed": [1, 0],
            "penalties_saved": [2, 1],
            "saves": [100, 90],
            "bonus_points": [10, 8],
            "value_latest_gw": [105.0, 95.0],
        }
    )

    expected_data = pd.DataFrame(
        {
            "Pos": [1, 2],
            "Team": ["Team A", "Team B"],
            "Points": [100, 90],
            "Actual Pos": [1, 2],
            "Difference": [" ", " "],
            "GK Points": [10, 9],
            "DEF Points": [20, 18],
            "MID Points": [30, 27],
            "FWD Points": [40, 36],
            "Goals Scored": [50, 45],
            "Assists": [25, 22],
            "Clean Sheets": [15, 12],
            "Yellow Cards": [5, 7],
            "Red Cards": [1, 2],
            "Goals Conceded": [20, 25],
            "Own Goals": [0, 1],
            "Penalties Missed": [1, 0],
            "Penalties Saved": [2, 1],
            "Saves": [100, 90],
            "Bonus Points": [10, 8],
        }
    )

    # Call the function with the sample data
    result = reorder_and_rename_columns(fpl_data)

    # Assertions to check if the returned data matches the expected data
    pd.testing.assert_frame_equal(result, expected_data)


def test_join_table_data(mocker):
    # Sample data to use for testing
    fpl_data = pd.DataFrame(
        {
            "team": ["Team A", "Team B"],
            "Points": [70, 65],
            "mapped_team": ["Actual Team A", "Actual Team B"],
        }
    )
    actual_data = pd.DataFrame(
        {"Team": ["Actual Team A", "Actual Team B"], "Pos": [1, 2], "Points": [68, 64]}
    )
    team_name_mapping = {"Team A": "Actual Team A", "Team B": "Actual Team B"}
    expected_data = pd.DataFrame(
        {
            "Pos": [1, 2],
            "Team": ["Team A", "Team B"],
            "Points": [70, 65],
            "Actual Pos": [1, 2],
            "Difference": [" ", " "],
            "GK Points": [10, 9],
            "DEF Points": [20, 18],
            "MID Points": [30, 27],
            "FWD Points": [40, 36],
            "Goals Scored": [50, 45],
            "Assists": [25, 22],
            "Clean Sheets": [15, 12],
            "Yellow Cards": [5, 7],
            "Red Cards": [1, 2],
            "Goals Conceded": [20, 25],
            "Own Goals": [0, 1],
            "Penalties Missed": [1, 0],
            "Penalties Saved": [2, 1],
            "Saves": [100, 90],
            "Bonus Points": [10, 8],
        }
    )

    # Mock the functions to return the sample data
    mocker.patch(
        "src.data_prep.join_table_data.load_table_data",
        return_value=(fpl_data, actual_data),
    )
    mocker.patch("src.data_prep.join_table_data.map_team_names", return_value=fpl_data)
    mocker.patch("src.data_prep.join_table_data.merge_tables", return_value=fpl_data)
    mocker.patch("src.data_prep.join_table_data.sort_and_rank", return_value=fpl_data)
    mocker.patch(
        "src.data_prep.join_table_data.calculate_rank_difference", return_value=fpl_data
    )
    mocker.patch(
        "src.data_prep.join_table_data.reorder_and_rename_columns",
        return_value=expected_data,
    )

    # Call the function with the sample data
    result = join_table_data("2023-24", team_name_mapping)

    # Assertions to check if the returned data matches the expected data
    pd.testing.assert_frame_equal(result, expected_data)


def test_get_list_of_seasons(mocker):
    # Sample data to use for testing
    sample_files = ["2023-24.csv", "2022-23.csv", "2021-22.csv"]
    expected_seasons = ["2023-24", "2022-23", "2021-22"]

    # Mock the os.listdir function to return the sample files
    mocker.patch("os.listdir", return_value=sample_files)

    # Call the function
    result = get_list_of_seasons()

    # Assertions to check if the returned data matches the expected data
    assert result == expected_seasons
