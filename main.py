# -*- coding: utf-8 -*-
"""

@author: Simon Martinez
"""

# Import packages
import streamlit as st
import home
import shooting
import game_history

def basketball_theme():
    st.set_page_config(
        page_title="Basketball Analytics",
        page_icon=":basketball:",
        layout="centered",
    )

basketball_theme()

# Function to load or change style
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load local CSS file
local_css("style.css")

st.sidebar.markdown("NBA Insights")
pages = ["**Home**", "**Shooting analysis**", "**Game History**"]
page = st.sidebar.radio("Menu", pages)
if page == pages[0]:
    home.run()
elif page == pages[1]:
    shooting.run()
else :
    game_history.run()

st.sidebar.markdown("---")
st.sidebar.markdown("### Contact me")
st.sidebar.markdown('Simon Martinez &nbsp; <a href="https://www.linkedin.com/in/simon-martinez-da/" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Linkedin.svg/20px-Linkedin.svg.png"></a> &nbsp; <a href="https://github.com/SimonMartinez4" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Octicons-mark-github.svg/20px-Octicons-mark-github.svg.png"></a> &nbsp; ', unsafe_allow_html=True)
st.sidebar.markdown("Email : [simonmartinez4@gmail.com](mailto:simonmartinez4@gmail.com)")