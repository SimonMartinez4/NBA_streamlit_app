# -*- coding: utf-8 -*-
"""

@author: Simon Martinez
"""

# Import packages
import streamlit as st
#from main import custom_css

#custom_css()

def run() :

    # Title of the page
    st.title("Welcome to NBA Insights")

    # About Me section
    st.header("About Me")
    st.write("""
    Hello, my name is **Simon Martinez**. I am a data analyst with a lifelong passion for basketball, having been a player and an avid fan since the age of six.
    Combining my professional expertise in data analysis with my love for the game, I created this streamlit app to share my unique perspective on basketball.
    """)

    st.image("img/michael-jordan---nba.jpg", use_column_width=True)

    st.write("""
    What interests me is identifying the elements that had the most influence during a game.
    Utilizing Python libraries and the NBA API, we aim to answer intriguing questions that arise during the excitement of a match, representing and synthesizing facts that are too numerous to narrate.
    """)

    # What You Will Find Here section
    st.header("What You Will Find Here")

    st.write("""
    - **Player Shooting Metrics**: Detailed analysis of shooting performances for individual players, including shooting percentages, shot locations, and efficiency.
    """)

    st.write("""
    - **Match Dynamics**: Specific game reports that trace the ebb and flow of each match, capturing pivotal moments and shifts in momentum.
    """)

    st.write("""
    - **In-depth Studies**: Comprehensive analyses on long-term trends and specific questions that have left a mark on the league. These studies provide deeper insights into historical and contemporary issues within the NBA.
    """)

    # Get in Touch section
    st.header("Get in Touch")
    st.write("""
    I am always eager to connect with other basketball fans and data enthusiasts. If you have any questions or would like to discuss any aspect of the game, feel free to reach out. 
    Whether you're a basketball fan, a fellow analyst, or simply curious, I'm here to explore the fascinating world of NBA data with you.
    """)