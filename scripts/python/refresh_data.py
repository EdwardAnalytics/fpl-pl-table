from src.data_prep.reload_data import (
    get_current_season_start_year,
    get_season_string,
    get_current_gameweek,
    check_and_update_metadata,
    get_current_season_fpl,
    get_current_season_actual,
    get_completed_seasons_fpl,
    get_completed_seasons_actual,
)
from src.tools.yaml_loader import load_yaml_file
from src.data_prep.join_table_data import join_all_seasons

# Get Team name mapping
team_name_mapping_path = "conf/team_name_mapping.yaml"
team_name_mapping = load_yaml_file(team_name_mapping_path)

season_start = get_current_season_start_year()
season_string = get_season_string(season_start)

current_gameweek = get_current_gameweek(season_string)

check_and_update_metadata(current_gameweek)

# Get completed seasons fpl
# get_completed_seasons_fpl(first_season_start=2016, latest_season_start=2023)

# Get current season fpl
# Only run if new player data run
get_current_season_fpl(season_start=season_start)

# Get completed seasons actual
# get_completed_seasons_actual(first_season_start=2016, latest_season_start=2023)

# Get current season actual
# Only run if new player data run
get_current_season_actual(season_start=season_start)

# Join league table data
join_all_seasons(team_name_mapping=team_name_mapping)
