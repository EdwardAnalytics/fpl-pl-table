import streamlit as st
import base64
import altair as alt
import pandas as pd
from src.data_prep.fpl_pl_table_players import get_season_string
from src.data_prep.join_table_data import get_list_of_seasons

# Get most recent available data
seasons = get_list_of_seasons()
latest_season = max(seasons)
latest_season = int(latest_season[:4])


def generate_streamlit_tables(season_index):
    season_start = latest_season - season_index
    season = get_season_string(season_start)
    # Load data
    try:
        league_table = pd.read_csv(
            f"data/fpl_premier_league_tables_joined/{season}.csv"
        )
        player_stats = pd.read_csv(f"data/fpl_premier_league_player_data/{season}.csv")
    except:
        return
    # Display the output tables
    league_name = f"{season}"
    st.header(league_name, divider="grey")

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
        st.write("")

        st.dataframe(player_stats_filtered, hide_index=True)


def main():
    st.title("FPL Premier League Table")

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


if __name__ == "__main__":
    main()
