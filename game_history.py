# -*- coding: utf-8 -*-
"""

@author: Simon Martinez
"""

# Import packages
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

# Import functions
from functions import list_seasons
from functions import get_roster
from functions import get_team_id
from functions import lastg_find
from functions import get_matchups
from functions import get_min_season
from functions import get_max_season
from functions import timecode
from functions import get_game_rota
from functions import get_teams_id
from functions import get_teams_colors
from functions import convert_clock_to_seconds
from functions import score_diff
from functions import game_hist
from functions import get_season_games

st.cache_data

# Loading teams colors hexacodes file

colors = pd.read_excel('https://raw.githubusercontent.com/SimonMartinez4/NBA_streamlit_app/main/src/NBA_Teams_Colors.xlsx', sheet_name='Feuil1')

def run():

    # Parameters selectboxes
    st.header("Game History Module",)

    method = st.radio("Choose method", ("Find a team's last game", "Find matchups between 2 teams", "Find games by date"))

    if method == "Find a team's last game" :
        team_options = ['PHI','CHI','MIL','CLE','BOS','ATL','MIA','CHA','NYK','ORL','BKN','IND','DET','TOR','WAS','LAC','MEM','UTA','SAC','LAL','DAL','DEN','NOP','HOU','SAS','PHO','OKC','MIN','POR','GSW']
        team = st.selectbox('Team', team_options)
        get_lastg_button = st.button("Get last game")
        if get_lastg_button :
            game_id=lastg_find(team)
            game_hist(game_id)
            st.table(colors)

    elif method == "Find matchups between 2 teams":
        team_1_opt = ['PHI','CHI','MIL','CLE','BOS','ATL','MIA','CHA','NYK','ORL','BKN','IND','DET','TOR','WAS','LAC','MEM','UTA','SAC','LAL','DAL','DEN','NOP','HOU','SAS','PHO','OKC','MIN','POR','GSW']
        team_1 = st.selectbox('Team 1', team_1_opt)
        team_2_opt = [team for team in team_1_opt if team != team_1]
        team_2 = st.selectbox('Team 2', team_2_opt)

        min_season_t1 = get_min_season(team_1)
        min_season_t2 = get_min_season(team_2)
        if min_season_t1 > min_season_t2 :
            min_season = min_season_t1
        else :
            min_season = min_season_t2

        max_season_t1 = get_max_season(team_1)
        max_season_t2 = get_max_season(team_2)
        if max_season_t1 < max_season_t2 :
            max_season = max_season_t1
        else :
            max_season = max_season_t2
        season_options = list_seasons(min_season, max_season)

        season = st.selectbox('Season', season_options)

        season_type_options = ['Regular Season', 'Pre Season', 'Playoffs']
        season_type = st.selectbox('Season Type', season_type_options)

        get_matchups_button = st.button("Get matchups")

        try :

            if "update_state" not in st.session_state :
                st.session_state.update_state = False
            
            if get_matchups_button or st.session_state.update_state :
                st.session_state.update_state = True

                matchups = get_matchups(team_1, team_2, season, season_type)

                # AgGrid Setup
                gb = GridOptionsBuilder.from_dataframe(matchups)
                gb.configure_selection(selection_mode='single', use_checkbox=False)
                gb.configure_pagination(enabled=True)
                gb.configure_auto_height(False)
                #gb.configure_side_bar(filters_panel=False, columns_panel = False)
                gb.configure_default_column(groupable=False, editable=False, filter=False, sortable=True)
                gb.configure_column(field = 'GAME_DATE ', filter = 'agDateColumnFilter')
                gb.configure_column(field = "GAME_ID", hide = True)
                gb.configure_column(field = "GAME_DATE ", hide = True)
                gridOptions = gb.build()

                # Display the table
                grid = AgGrid(
                    matchups,
                    gridOptions=gridOptions,
                    update_mode=GridUpdateMode.SELECTION_CHANGED,
                    allow_unsafe_jscode=True,
                    theme='material',
                    height=300
                )

                selected_row = grid['selected_rows']

                if pd.DataFrame(selected_row).empty:
                    st.write('No game picked')
                else :
                    game_hist(selected_row['GAME_ID'])

        except ValueError as e :
            st.error("No games matching your criterias")

    elif method == "Find games by date" :
        max_season = get_max_season('LAL')
        season_options = list_seasons(1996,max_season)
        season = st.selectbox('Season', season_options)

        get_schedule_button = st.button('Get schedule')

        if "update_state" not in st.session_state :
            st.session_state.update_state = False
        
        if get_schedule_button or st.session_state.update_state :
            st.session_state.update_state = True

            games = get_season_games(season)

            # AgGrid Config options
            options = {
                "sideBar": ['filters'],
            }

            # AgGrid Setup
            gb2 = GridOptionsBuilder.from_dataframe(games)
            gb2.configure_selection(selection_mode='single', use_checkbox=False)
            gb2.configure_pagination(enabled=True)
            gb2.configure_auto_height(False)
            gb2.configure_default_column(groupable=False, editable=False, filter=False, sortable=True)
            gb2.configure_column(field = 'GAME_DATE ', filter = 'agDateColumnFilter')
            gb2.configure_column(field = "GAME_ID", hide = True)
            gb2.configure_column(field = "GAME_DATE ", hide = True)
            gb2.configure_grid_options(**options)
            gridOptions2 = gb2.build()

            grid2 = AgGrid(
                games,
                gridOptions=gridOptions2,
                update_mode=GridUpdateMode.SELECTION_CHANGED,
                allow_unsafe_jscode=True,
                theme='material',
                height=300
            )
            
            sel_row = grid2['selected_rows']

            if pd.DataFrame(sel_row).empty:
                st.write('No game picked')
            else :
                game_hist(sel_row['GAME_ID'])
