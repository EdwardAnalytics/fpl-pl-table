import streamlit as st
import base64
import altair as alt
import pandas as pd
from src.data_prep.fpl_pl_table_players import get_season_string
from src.data_prep.join_table_data import get_list_of_seasons
import json

# Get most recent available data
seasons = get_list_of_seasons()
latest_season = max(seasons)
latest_season = int(latest_season[:4])

# Get gameweek data correct up to
file_path = "data/scoring_meta.json"

# Read the JSON data from the file
with open(file_path, "r") as file:
    scoring_meta = json.load(file)
scoring_data_gameweek = scoring_meta.get("scoring_data_gameweek")


def generate_streamlit_tables(season_index):
    season_start = latest_season - season_index
    season = get_season_string(season_start)
    # Load data
    try:
        league_table = pd.read_csv(
            f"data/fpl_premier_league_tables_joined/{season}.csv"
        )
        if season_start <= 2018:
            encoding = "latin-1"
        else:
            encoding = "utf-8"
        player_stats = pd.read_csv(
            f"data/fpl_premier_league_player_data/{season}.csv", encoding=encoding
        )
        # Manual encoding fix due to indexs being added
        player_stats["Player Name"] = player_stats["Player Name"].str.replace(
            r"\s\d+$", "", regex=True
        )

    except:
        return
    # Display the output tables
    league_name = f"{season}"
    st.write("")

    st.subheader(league_name, divider="grey")

    league_table_tab, player_statistics_tab = st.tabs(
        ["📃League Table", "📈 Player Statistics"]
    )

    with league_table_tab:
        st.dataframe(league_table, hide_index=True)

    with player_statistics_tab:
        # Get distinct values using set, convert to list and sort alphabetically
        teams = sorted(
            [team for team in player_stats["Team"].unique() if isinstance(team, str)]
        )

        # Move "All Teams" to the front
        teams.remove("All Teams")
        teams.insert(0, "All Teams")

        selected_team = st.selectbox(label="Select Team", options=teams, index=0)

        player_stats_filtered = player_stats[player_stats["Team"] == selected_team]
        player_stats_filtered = player_stats_filtered.drop(columns=["Team"])

        st.dataframe(player_stats_filtered, hide_index=True)
    if season_index == 0:
        st.markdown(f"_Data up to end of gameweek {scoring_data_gameweek}._")

    st.write("")


def main():
    st.title("FPL Premier League Table")
    st.markdown(
        """
    This shows how the Premier League table would look if teams were ranked by their individual players' Fantasy Premier League points.
    """
    )

    # Add github link and logo
    LOGO_IMAGE = "assets//pwt.png"

    st.markdown(
        """
        <style>
        .container {
            display: flex;
        }
        .logo-text {
            font-weight: 0 !important;
            font-size: 15px !important;
            padding-top: 0px !important;
            margin-left: 0px;
            font-style: italic; 
        }
        .logo-img {
            float:right;
            width: 28px;
            height: 28px;
            margin-right: 8px; 
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="container">
            <img class="logo-img" src="data:assets//pwt.png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
            <p class="logo-text"><a href="https://github.com/EdwardAnalytics/fpl-pl-table">GitHub Repo</a></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Run function for individual seasons
    season_index = 0
    generate_streamlit_tables(season_index=season_index)

    season_index += 1
    generate_streamlit_tables(season_index=season_index)

    season_index += 1
    generate_streamlit_tables(season_index=season_index)

    season_index += 1
    generate_streamlit_tables(season_index=season_index)

    season_index += 1
    generate_streamlit_tables(season_index=season_index)

    season_index += 1
    generate_streamlit_tables(season_index=season_index)

    season_index += 1
    generate_streamlit_tables(season_index=season_index)

    season_index += 1
    generate_streamlit_tables(season_index=season_index)

    season_index += 1
    generate_streamlit_tables(season_index=season_index)

    season_index += 1
    generate_streamlit_tables(season_index=season_index)

    season_index += 1
    generate_streamlit_tables(season_index=season_index)

    season_index += 1
    generate_streamlit_tables(season_index=season_index)

    season_index += 1
    generate_streamlit_tables(season_index=season_index)

    season_index += 1
    generate_streamlit_tables(season_index=season_index)

    season_index += 1
    generate_streamlit_tables(season_index=season_index)

    season_index += 1
    generate_streamlit_tables(season_index=season_index)

    season_index += 1
    generate_streamlit_tables(season_index=season_index)

    season_index += 1
    generate_streamlit_tables(season_index=season_index)

    season_index += 1
    generate_streamlit_tables(season_index=season_index)

    season_index += 1
    generate_streamlit_tables(season_index=season_index)

    season_index += 1
    generate_streamlit_tables(season_index=season_index)

    season_index += 1
    generate_streamlit_tables(season_index=season_index)

    season_index += 1
    generate_streamlit_tables(season_index=season_index)

    season_index += 1
    generate_streamlit_tables(season_index=season_index)

    season_index += 1
    generate_streamlit_tables(season_index=season_index)

    season_index += 1
    generate_streamlit_tables(season_index=season_index)

    # Display the data sources and mention Wikipedia as the actual table source
    st.write("")
    st.markdown("""
        Data sources: _FPL Data: Anand Vaastav, [Fantasy-Premier-League](https://github.com/vaastav/Fantasy-Premier-League)_; _PL Data: Wikipedia_
        """)


if __name__ == "__main__":
    main()
