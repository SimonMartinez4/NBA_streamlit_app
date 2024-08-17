# -*- coding: utf-8 -*-
"""

@author: Simon Martinez
"""

## Import packages

# NBA api endpoints
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.endpoints import commonteamyears
from nba_api.stats.endpoints import gamerotation
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import playbyplayv3
from nba_api.stats.static import players
from nba_api.stats.static import teams

# Dataviz
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Other packages
import re
import json
import requests
import numpy as np
from datetime import datetime
from datetime import date
import pandas as pd
import streamlit as st

# Loading floor image
img = plt.imread('./img/topview-working-hand.jpg')

# Loading NBA teams color codes
colors = pd.read_excel('./src/NBA_Teams_Colors.xlsx', sheet_name='Feuil1')

## Function to get team id from the abbreviation
def get_player_id(name) :
    player_id=players.find_players_by_full_name(name)[0]['id']
    return player_id

## Function to get team id from the abbreviation
def get_team_id(abbr) :
    team_id=teams.find_team_by_abbreviation(abbr)['id']
    return team_id

## Function to get team name from the abbreviation
def get_team_name(abbr) :
    team_name=teams.find_team_by_abbreviation(abbr)['full_name']
    return team_name

# Function to get datas for any player for any season
def get_data(player_name,team_abbr,season,season_type):
    shot_json = shotchartdetail.ShotChartDetail(
        team_id = get_team_id(team_abbr),
        player_id = get_player_id(player_name),
        context_measure_simple = 'FG_PCT',
        season_nullable = season,
        season_type_all_star = season_type
    )
    shot_data = json.loads(shot_json.get_json())
    relevant_data = shot_data['resultSets'][0]
    headers = relevant_data['headers']
    rows = relevant_data['rowSet']
    data = pd.DataFrame(rows)
    data.columns = headers
    return data

# Function to draw basketball court
def create_court(ax, color):
    ax.imshow(img,extent=[-250,250,0,470],alpha=0.4)
    # Short corner 3PT lines
    ax.plot([-220, -220], [0, 140], linewidth=1, color=color)
    ax.plot([220, 220], [0, 140], linewidth=1, color=color)
    # 3PT Arc
    ax.add_artist(mpl.patches.Arc((0, 140), 440, 315, theta1=0, theta2=180, facecolor='none', edgecolor=color, lw=1))
    # Lane and Key
    ax.plot([-80, -80], [0, 190], linewidth=1, color=color)
    ax.plot([80, 80], [0, 190], linewidth=1, color=color)
    ax.plot([-60, -60], [0, 190], linewidth=1, color=color)
    ax.plot([60, 60], [0, 190], linewidth=1, color=color)
    ax.plot([-80, 80], [190, 190], linewidth=1, color=color)
    ax.add_artist(mpl.patches.Circle((0, 190), 60, facecolor='none', edgecolor=color, lw=1))
    # Rim
    ax.add_artist(mpl.patches.Circle((0, 60), 15, facecolor='none', edgecolor=color, lw=1))
    # Backboard
    ax.plot([-30, 30], [40, 40], linewidth=1, color=color)
    # Remove ticks
    ax.set_xticks([])
    ax.set_yticks([])
    # Set axis limits
    ax.set_xlim(-250, 250)
    0,ax.set_ylim(0, 470)
    return ax

## Function to draw the shot chart
def draw_chart(player_name,team_abbr,season,season_type) :
    data = get_data(player_name,team_abbr,season,season_type)
    team_name=get_team_name(team_abbr)
    # General plot parameters
    mpl.rcParams['font.family'] = "Verdana"
    mpl.rcParams['font.size'] = 18
    mpl.rcParams['axes.linewidth'] = 1
    fig = plt.figure(figsize=(4, 3.76))
    ax = fig.add_axes([0,0,1,1])
    fig.patch.set_facecolor('none')
    # Plot hexbin of shots
    hexbin_data = ax.hexbin(
        -data['LOC_X'],
        data['LOC_Y'] + 60,
        C=data['SHOT_MADE_FLAG'],
        gridsize=(30, 30),
        extent=(-300, 300, 0, 940),
        cmap='RdYlGn',
        edgecolor='#32435F',
        linewidth=0.5,
        linestyle="dotted",
        reduce_C_function=np.mean)
    ax = create_court(ax, '#32435F')
    colorbar=fig.colorbar(
        hexbin_data,
        location='bottom',
        orientation='horizontal',
        aspect=40,
    )
    text = "Field Goal Percentage"
    ax.text(0, 1.05, text, transform=ax.transAxes, ha='left', va='baseline', c='#32435F')
    colorbar.ax.tick_params(labelsize=12,color='#32435F',labelcolor='#32435F')
    colorbar.ax.set_position([0.2, 0.25, 0.6, 0.03])
    st.pyplot(fig)

## Function to draw a shot tendencies chart
def draw_chart_tend(player_name,team_abbr,season,season_type) :
    data = get_data(player_name,team_abbr,season,season_type)
    team_name=get_team_name(team_abbr)
    # General plot parameters
    mpl.rcParams['font.family'] = "Verdana"
    mpl.rcParams['font.size'] = 18
    mpl.rcParams['axes.linewidth'] = 1
    fig = plt.figure(figsize=(4, 3.76))
    ax = fig.add_axes([0,0,1,1])
    fig.patch.set_facecolor('none')
    # Plot hexbin of shots
    hexbin_data = ax.hexbin(
        -data['LOC_X'],
        data['LOC_Y'] + 60,
        gridsize=(30, 30),
        extent=(-300, 300, 0, 940),
        bins='log',
        cmap='YlOrRd',
        edgecolor='#32435F',
        linewidth=0.5,
        linestyle="dotted")
    ax = create_court(ax, '#32435F')
    text = "Shot tendencies"
    ax.text(0, 1.05, text, transform=ax.transAxes, ha='left', va='baseline', c='#32435F')
    colorbar=fig.colorbar(
        hexbin_data,
        location='bottom',
        orientation='horizontal',
        aspect=40,
    )
    colorbar.ax.tick_params(labelsize=0,color='#32435F',labelcolor='#32435F')
    colorbar.ax.set_position([0.2, 0.25, 0.6, 0.03])
    st.pyplot(fig)

## Function to get a synthesis table
def stats_tab(player_name,team_abbr,season,season_type):
    # Get datas
    data = get_data(player_name,team_abbr,season,season_type)
    # Custom zones
    data['Zone']=np.where(
                    (data['SHOT_DISTANCE']<=4), 'Restricted Area',
                    np.where(
                        (data['SHOT_DISTANCE']>4)&(data['SHOT_DISTANCE']<=8),'Less than 8ft (Non-RA)',
                        np.where(
                            (data['SHOT_ZONE_RANGE']=='8-16 ft.'),'Mid-range (8-16 ft)',
                            np.where(
                                (data['SHOT_ZONE_RANGE']=='16-24 ft.'),'Mid-range (16-24 ft)',
                                np.where(
                                    (data['SHOT_ZONE_RANGE']=='24+ ft.')&((data['SHOT_ZONE_AREA']=='Right Side(R)')|(data['SHOT_ZONE_AREA']=='Left Side(L)')),'Corner 3',
                                    np.where(
                                    (data['SHOT_ZONE_RANGE']=='24+ ft.')&((data['SHOT_ZONE_AREA']!='Right Side(R)')&(data['SHOT_ZONE_AREA']!='Left Side(L)')),'3 pointers','From Backcourt'
                                    )
                                )
                            )
                        )
                    )
                )
    # Group by the custom zone, select the attempt share and the FG percentage
    table = data.groupby('Zone').agg({
        'SHOT_ATTEMPTED_FLAG':'sum',
        'SHOT_MADE_FLAG':'mean'})
    table = table.rename(columns={
    'SHOT_ATTEMPTED_FLAG': 'FG Attempted',
    'SHOT_MADE_FLAG': 'FG%'
    })
    total_attempts = table['FG Attempted'].sum()
    table['% Attempted'] = (table['FG Attempted'] / total_attempts) * 100
    table['Field Goal %'] = table['FG%'] * 100
    table = table.sort_values(by='% Attempted', ascending=False)
    table = table.round(2).astype(str)
    table.drop(columns='FG Attempted',inplace=True)
    table.drop(columns='FG%',inplace=True)
    st.table(table)

## Function to get the min season for a team
def get_min_season(team_abbr) :
    teamyears_json = commonteamyears.CommonTeamYears(
    )
    teamyears_data = json.loads(teamyears_json.get_json())
    teamyears_relevant_data = teamyears_data['resultSets'][0]
    teamyears_headers = teamyears_relevant_data['headers']
    teamyears_rows = teamyears_relevant_data['rowSet']
    teamyears_data = pd.DataFrame(teamyears_rows)
    teamyears_data.columns = teamyears_headers
    teamyears_select = teamyears_data.loc[teamyears_data["ABBREVIATION"] == team_abbr]
    min_year = teamyears_select['MIN_YEAR'].iloc[0]
    min_year=int(min_year)
    if min_year < 1996 :
        min_year_ = 1996
    else :
        min_year_ = min_year

    return min_year_

## Function to get seasons from years
def list_seasons(min_year_,max_year):
    seasons = []
    for year in range(min_year_, max_year + 1):
        season = f"{year}-{str(year + 1)[-2:]}" 
        seasons.append(season)
    return seasons

## Function to get the max season for a team
def get_max_season(team_abbr) :
    teamyears_json = commonteamyears.CommonTeamYears(
    )
    teamyears_data = json.loads(teamyears_json.get_json())
    teamyears_relevant_data = teamyears_data['resultSets'][0]
    teamyears_headers = teamyears_relevant_data['headers']
    teamyears_rows = teamyears_relevant_data['rowSet']
    teamyears_data = pd.DataFrame(teamyears_rows)
    teamyears_data.columns = teamyears_headers
    teamyears_select = teamyears_data.loc[teamyears_data["ABBREVIATION"] == team_abbr]
    max_year = teamyears_select['MAX_YEAR'].iloc[0]
    max_year = int(max_year)
    return max_year

## Function to get the roster for a team and a season
def get_roster(team_abbr,season) :
    roster_json = commonteamroster.CommonTeamRoster(
        team_id = get_team_id(team_abbr),
        season = season,
    )
    roster_data = json.loads(roster_json.get_json())
    roster_relevant_data = roster_data['resultSets'][0]
    roster_headers = roster_relevant_data['headers']
    roster_rows = roster_relevant_data['rowSet']
    roster_data = pd.DataFrame(roster_rows)
    roster_data.columns = roster_headers
    return list(roster_data['PLAYER'])

# Function to find the last game for a given team
def lastg_find(team_abbr):
    game_json = leaguegamefinder.LeagueGameFinder(
        team_id_nullable = get_team_id(team_abbr)
        )
    game_data = json.loads(game_json.get_json())
    relevant_data = game_data['resultSets'][0]
    headers = relevant_data['headers']
    rows = relevant_data['rowSet']
    data = pd.DataFrame(rows)
    data.columns = headers
    max_date=data['GAME_DATE'].max()
    data=data[data['GAME_DATE']==max_date]
    game_id=data['GAME_ID'][0]
    return game_id

## Function to get matchups between two tems for a given season
def get_matchups(team1_abbr,team2_abbr,season, season_type) :
    game_json = leaguegamefinder.LeagueGameFinder(
        team_id_nullable = get_team_id(team1_abbr),
        vs_team_id_nullable = get_team_id(team2_abbr),
        season_nullable = season,
        season_type_nullable = season_type
        )
    game_data = json.loads(game_json.get_json())
    relevant_data = game_data['resultSets'][0]
    headers = relevant_data['headers']
    rows = relevant_data['rowSet']
    data = pd.DataFrame(rows)
    data.columns = headers
    data['GAME_DATE ']=pd.to_datetime(data['GAME_DATE'])
    data['GAME_DATE']=data['GAME_DATE '].dt.strftime('%Y-%m-%d')
    data=data[['GAME_ID','GAME_DATE ','GAME_DATE', 'MATCHUP']]

    return data

def timecode(time):
    
    # Getting time in minutes and overtime in minutes (float) from total time in tenths
    time_m = time / 10 / 60
    time_m_ot = (time - 28800) / 10 / 60
    
    # Getting the period and the time remaining in minutes (float) whether it is in time periods or overtime
    if time == 0 :
        p = 1
        period = f"QT{p}"
        time_r = 12
    elif time <= 28800 :
        p = int(np.ceil(time_m / 12))
        period = f"QT{p}"
        time_n = 12 - (time_m) % 12
        if time_n == 12 :
            time_r = 0
        else :
            time_r = time_n
    else :
        p = int(np.ceil(time_m_ot / 5))
        period = f"OT{p}"
        time_n = 5 - (time_m_ot % 5)
        if time_n == 5 :
            time_r = 0
        else :
            time_r = time_n
    
    # Converting the time remaining (float) in 2 objects minutes and seconds
    min = int(time_r)
    sec = int((time_r - min) * 60)
    
    # Formatting
    return f"{period} {min:02d}:{sec:02d}"

## Function to get rotation datas for a given game
def get_game_rota(game_id):    
    rota_json = gamerotation.GameRotation(
        game_id = game_id
        )
    rota_data = json.loads(rota_json.get_json())
    away_data = rota_data['resultSets'][0]
    home_data = rota_data['resultSets'][1]
    away_headers = away_data['headers']
    home_headers = home_data['headers']
    away_rows = away_data['rowSet']
    home_rows = home_data['rowSet']
    away_data = pd.DataFrame(away_rows)
    home_data = pd.DataFrame(home_rows)
    away_data.columns = away_headers
    home_data.columns = home_headers
    data_frames = [home_data, away_data]
    for df in data_frames:
        df['DURATION'] = df['OUT_TIME_REAL'] - df['IN_TIME_REAL']
        df['Player'] = df.apply(lambda row: row['PLAYER_FIRST'] + ' ' + row['PLAYER_LAST'], axis=1)
        df['Team_Name'] = df.apply(lambda row: row['TEAM_CITY'] + ' ' + row['TEAM_NAME'], axis=1)
        df['In Time'] = df['IN_TIME_REAL'].apply(timecode)
        df['Out Time'] = df['OUT_TIME_REAL'].apply(timecode)
        starters = df.groupby('PERSON_ID')['IN_TIME_REAL'].min() == 0
        df['starter'] = df['PERSON_ID'].map(starters).astype(int)
    return home_data, away_data

## Function to get teams id from the rotation data
def get_teams_id(home_data,away_data) :
    home_team_id,away_team_id = home_data['TEAM_ID'].unique()[0],away_data['TEAM_ID'].unique()[0]
    return home_team_id,away_team_id

## Function to get teams colors from the rotation data et the colors excel files
def get_teams_colors(home_data,away_data) :
    home_team_id, away_team_id = get_teams_id(home_data,away_data)
    home_team_c1 = colors[colors['team_id']==home_team_id]['color_1'].iloc[0].strip().upper()
    home_team_c2 = colors[colors['team_id']==home_team_id]['color_2'].iloc[0].strip().upper()
    away_team_c1 = colors[colors['team_id']==away_team_id]['color_1'].iloc[0].strip().upper()
    away_team_c2 = colors[colors['team_id']==away_team_id]['color_2'].iloc[0].strip().upper()
    return home_team_c1, home_team_c2, away_team_c1, away_team_c2

## Function to convert clock values to time value in tenths
def convert_clock_to_seconds(clock, period):
    # Extract minutes and seconds using regex
    match = re.match(r'PT(\d+)M(\d+\.\d+)S', clock)
    if not match:
        raise ValueError(f"Invalid clock format: {clock}")
    
    # Creating minutes and seconds objects with the match groups
    minutes = float(match.group(1))
    seconds = float(match.group(2))
    
    # Converting in seconds and then in tenths
    if period < 5: # for a game without OT
        total_seconds = minutes * 60 + seconds
        total_seconds = (period - 1) * 12 * 60 + (12 * 60 - total_seconds)
    else : # for a game with OTs
        total_seconds = minutes * 60 + seconds
        total_seconds = 4 * 12 * 60 + (period - 5) * 5 * 60 + (5 * 60 - total_seconds)
                
    total_tenths = total_seconds * 10
    
    return total_tenths

## Function to get score diff during game from the playbyplay NBA api endpoint
def score_diff(game_id):
    
    # Getting the playbyplay data
    pbp_json = playbyplayv3.PlayByPlayV3(
        game_id = game_id
        )
    pbp_data = json.loads(pbp_json.get_json())
    relevant_data = pbp_data['game']['actions']
    data = pd.DataFrame(relevant_data)[['clock','scoreHome','scoreAway','period','actionType']]
    
    # Filtering df to get only the entries that match score change
    data_sc = data[(data['actionType']=='period') | (data['actionType']=='Made Shot')].copy()
    
    # Calculating scorediff, time and timecode columns
    data_sc.loc[:,'time']=data_sc.apply(lambda row: convert_clock_to_seconds(row['clock'], row['period']), axis=1)
    data_sc.loc[:,'scoreDiff']=data_sc['scoreHome'].astype(int)-data_sc['scoreAway'].astype(int)
    data_sc.loc[:,'timeCode'] = data_sc['time'].apply(timecode)
    
    return data_sc

## Function to get the Game History chart
def game_hist(game_id):

    # Getting rotation data, score_diff data, teams id, colors
    home_data, away_data = get_game_rota(game_id)
    home_team_id,away_team_id= get_teams_id(home_data,away_data)
    home_team_c1, home_team_c2, away_team_c1, away_team_c2 = get_teams_colors(home_data,away_data)
    data_sc=score_diff(game_id)
    
    # Sorting the rotation data to have starters on top
    home_data=home_data.sort_values(by='starter', ascending=True)
    away_data=away_data.sort_values(by='starter', ascending=True)

    # Creating a Plotly go figure with 3 rows
    fig=go.Figure()
    fig = make_subplots(rows=3, cols=1)

    # Top row : home team game rotation bars with home_data values
    fig.add_trace(go.Bar(
        y = home_data.Player,
        base = home_data.IN_TIME_REAL,
        x = home_data.DURATION,
        orientation='h',
        hovertext=home_data[['In Time', 'Out Time', 'PLAYER_PTS']].apply(
            lambda row: f'In: {row["In Time"]} - Out: {row["Out Time"]} - {row["PLAYER_PTS"]} PTS',
            axis=1
            ),
        hoverinfo='y+text',
        marker=dict(
            color=home_team_c1,
            line=dict(color=home_team_c2, width=0.6),
            pattern=dict(shape='/', size=3, solidity=0.5, fgcolor=home_team_c2)
            )
        ),
    1,1)

    # Middle row : score diff line with data_sc values
    fig.add_trace(go.Scatter(
        y=data_sc['scoreDiff'],
        x=data_sc['time'],
        name='Score Difference',
        mode='lines+markers',
        hovertext=data_sc[['timeCode','scoreHome','scoreAway']].apply(
            lambda row: f'{row["timeCode"]} - Score : {row["scoreHome"]} - {row["scoreAway"]}',
            axis=1
            ),
        hoverinfo='text',
        marker=dict(
            color='grey',
            size=3
            ),
        line=dict(
            color='grey',
            width=1.2
            )
        ),
    2,1)

    # Red line to highlight the  score diff
    fig.add_shape(
        type="line",
        x0=min(data_sc['time']),
        x1=max(data_sc['time']),
        y0=0,
        y1=0,
        line=dict(
            color="red",
            width=0.8
        ),
        row=2,
        col=1
    )

    # Bottom row : away team game rotation bars with away_data values
    fig.add_trace(go.Bar(
        y = away_data.Player,
        base = away_data.IN_TIME_REAL,
        x = away_data.DURATION,
        orientation='h',
        hovertext=away_data[['In Time', 'Out Time', 'PLAYER_PTS']].apply(
            lambda row: f'In: {row["In Time"]} - Out: {row["Out Time"]} - {row["PLAYER_PTS"]} PTS',
            axis=1
            ),
        hoverinfo='y+text',
            marker=dict(
            color=away_team_c1,
            line=dict(color=away_team_c2, width=0.6),
            pattern=dict(shape='/', size=3, solidity=0.5, fgcolor=away_team_c2)
            )
        ),
    3,1)
    
    # Updating the x axis to match a game lenght, setting ticks to match quarters, adding orange lines to hightlight the periods ends
    max_x = max(data_sc['time'])
    fig.update_xaxes(
        tickvals=[7200, 14400, 21600, 28800, 31800, 34800, 37800, 40800, 43800, 46800]
    )


    fig.update_xaxes(
        showgrid=True,
        gridwidth=2,
        gridcolor='orange',
        range=[0, max_x]
    )
    
    # Hiding ticks for the game rotation graphs
    fig.update_xaxes(showticklabels=False)

    # Updating y axis
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgb(220, 220, 220)',
        zeroline=True,
        showline=True,
        linewidth=2,
        linecolor='orange'
    )

    # Adding home logo
    fig.add_layout_image(
        dict(
            source=f"https://raw.githubusercontent.com/SimonMartinez4/NBA_streamlit_app/main/logos/{home_team_id}.png",
            xref="paper", yref="paper",
            x=1, y=0.75,
            sizex=0.3, sizey=0.3,
            xanchor="right", yanchor="bottom",
            opacity=0.2
        )
    )

    # Adding away logo
    fig.add_layout_image(
        dict(
            source=f"https://raw.githubusercontent.com/SimonMartinez4/NBA_streamlit_app/main/logos/{away_team_id}.png",
            xref="paper", yref="paper",
            x=1, y=0.0,
            sizex=0.3, sizey=0.3,
            xanchor="right", yanchor="bottom",
            opacity=0.2
        )
    )
    
    # Adding periods annotations
    fig.add_annotation(
        x=3600,
        y=-12.5,
        text="1st QT",
        showarrow=False,
        font=dict(
        size=36,
        color='rgba(128, 128, 128, 0.5)'
        ),
        row=2,
        col=1
    )
    
    fig.add_annotation(
        x=10800,
        y=-12.5,
        text="2nd QT",
        showarrow=False,
        font=dict(
        size=36,
        color='rgba(128, 128, 128, 0.5)'
        ),
        row=2,
        col=1
    )
    
    fig.add_annotation(
        x=18000,
        y=-12.5,
        text="3rd QT",
        showarrow=False,
        font=dict(
        size=36,
        color='rgba(128, 128, 128, 0.5)'
        ),
        row=2,
        col=1
    )
    
    fig.add_annotation(
        x=25200,
        y=-12.5,
        text="4th QT",
        showarrow=False,
        font=dict(
        size=36,
        color='rgba(128, 128, 128, 0.5)'
        ),
        row=2,
        col=1
    )
    
    fig.add_annotation(
        x=30300,
        y=-12.5,
        text="OT1",
        showarrow=False,
        font=dict(
        size=20,
        color='rgba(128, 128, 128, 0.5)'
        ),
        row=2,
        col=1
    )
    
    fig.add_annotation(
        x=33300,
        y=-12.5,
        text="OT2",
        showarrow=False,
        font=dict(
        size=20,
        color='rgba(128, 128, 128, 0.5)'
        ),
        row=2,
        col=1
    )
    
    fig.add_annotation(
        x=36300,
        y=-12.5,
        text="OT3",
        showarrow=False,
        font=dict(
        size=20, 
        color='rgba(128, 128, 128, 0.5)'
        ),
        row=2,
        col=1
    )
    
    fig.add_annotation(
        x=39300,
        y=-12.5,
        text="OT4", 
        showarrow=False,
        font=dict(
        size=20,
        color='rgba(128, 128, 128, 0.5)'
        ),
        row=2,
        col=1
    )
    
    fig.add_annotation(
        x=42300,
        y=-12.5,
        text="OT5",
        showarrow=False,
        font=dict(
        size=20,
        color='rgba(128, 128, 128, 0.5)' 
        ),
        row=2,
        col=1
    )
    
    fig.add_annotation(
        x=45300,
        y=-12.5,
        text="OT6",
        showarrow=False,
        font=dict(
        size=20,
        color='rgba(128, 128, 128, 0.5)'
        ),
        row=2,
        col=1
    )

    # Title, size, legend
    fig.update_layout(
        title="Game History",
        title_font=dict(
            family="Verdana",
            size=36,
            color="#5580A0",
        ),
        title_x=0.37,
        showlegend=False,
        width=1000,
        height=1000,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )

    return st.plotly_chart(fig, use_container_width=True)

## Function to get all games for a season
def get_season_games(season) :
    game_json = leaguegamefinder.LeagueGameFinder(
        season_nullable = season,
        season_type_nullable = ['Regular Season','Playoffs']
        )
    game_data = json.loads(game_json.get_json())
    relevant_data = game_data['resultSets'][0]
    headers = relevant_data['headers']
    rows = relevant_data['rowSet']
    data = pd.DataFrame(rows)
    data.columns = headers
    data['GAME_DATE ']=pd.to_datetime(data['GAME_DATE'])
    data['GAME_DATE']=data['GAME_DATE '].dt.strftime('%Y-%m-%d')
    data=data[['GAME_ID','GAME_DATE ','GAME_DATE', 'MATCHUP']]
    return data