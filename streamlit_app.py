import streamlit as st
import base64
import altair as alt
import pandas as pd


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

    season = "2016-17"
    # Display the output tables
    league_name = f"{season} FPL Premier League"
    st.header(league_name, divider="grey")

    league_table_tab, player_statistics_tab = st.tabs(
        ["📃League Table", "📈 Player Statistics"]
    )

    # Load data
    league_table = pd.read_csv(f"data/fpl_premier_league_tables_joined/{season}.csv")
    player_stats = pd.read_csv(f"data/fpl_premier_league_player_data/{season}.csv")

    with league_table_tab:
        st.dataframe(league_table, hide_index=True)

    with player_statistics_tab:
        # Add dropdown filter ##########
        st.dataframe(player_stats, hide_index=True)


if __name__ == "__main__":
    main()
