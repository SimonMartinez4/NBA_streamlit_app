
# -*- coding: utf-8 -*-
"""

@author: Simon Martinez
"""

# Import packages
import streamlit as st
from functions import list_seasons
from functions import get_roster
from functions import draw_chart
from functions import draw_chart_tend
from functions import stats_tab
from functions import get_min_season
from functions import get_max_season


def run():

    # Parameters selectboxes
    st.header("Select Player",)
    # Creating two columns
    col1, col2 = st.columns([0.5,0.5], gap='medium')

    with col1:
       
        team_options = ['PHI','CHI','MIL','CLE','BOS','ATL','MIA','CHA','NYK','ORL','BKN','IND','DET','TOR','WAS','LAC','MEM','UTA','SAC','LAL','DAL','DEN','NOP','HOU','SAS','PHO','OKC','MIN','POR','GSW']
        team = st.selectbox('Team', team_options)
        season_options = list_seasons(get_min_season(team), get_max_season(team))
        season = st.selectbox('Season', season_options)
    with col2:
        player_options = get_roster(team,season)
        player = st.selectbox('Players', player_options)
        season_type_options = ['Regular Season', 'Pre Season', 'Playoffs']
        season_type = st.selectbox('Season Type', season_type_options)
    
    # Button to draw chart
    draw_chart_button=st.button("Draw Chart")
              
    if draw_chart_button:
            st.header(f"Shot Chart : {player} - {team} - {season} {season_type}")
            col1, col2 = st.columns([0.5,0.5], gap='medium')
            with col1 :
                draw_chart(player, team, season, season_type)
            with col2:
                draw_chart_tend(player, team, season, season_type)
    
    if draw_chart_button:
        st.header("Summary")
        stats_tab(player, team, season, season_type) 
            