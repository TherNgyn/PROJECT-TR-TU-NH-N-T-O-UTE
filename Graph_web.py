import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from tkinter import ttk
from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Polygon
from tkinter import messagebox
from logpy import run, fact, eq, Relation, var
from streamlit import components
from matplotlib.animation import FuncAnimation

THEMES = [
    "light",
    "dark",
    "green",
    "blue",
]
GITHUB_OWNER = "streamlit"
GITHUB_REPO = "theming-showcase"

adjacent = Relation()
coastal = Relation()

file_coastal = 'coastal_states.txt'
file_adjacent = 'adjacent_states.txt'

with open(file_coastal, 'r') as f:
    line = f.read()
    coastal_states = line.split(',')

for state in coastal_states:
    fact(coastal, state)

with open(file_adjacent, 'r') as f:
    adjlist = [line.strip().split(',') for line in f if line and line[0].isalpha()]

for L in adjlist:
    head, tail = L[0], L[1:]
    for state in tail:
        fact(adjacent, head, state)

x = var()

st.markdown('<h1 style="text-align:center; color:Violet;">Analyzing Geography</h1>', unsafe_allow_html=True)

st.lst_city = ["Alabama", "Arizona", "Arkansas",
    "California", "Colorado", "Connecticut", "Delaware",
    "Florida", "Georgia", "Idaho", "Illinois", "Indiana",
    "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts",
    "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska",
    "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina",
    "North Dakota", "Ohio", "Oklahoma", "Oregon",
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia",
    "Washington", "West Virginia", "Wisconsin", "Wyoming"]

def ve_ban_do(states_to_fill):
    state_coords = {
        'California': (-119.4179, 36.7783),
        'Texas': (-99.9018, 31.9686),
        'Florida': (-81.5158, 27.6648),
        'New York': (-75.3060, 42.7128),
        'Illinois': (-89.3985, 40.6331),
        'Pennsylvania': (-77.4945, 40.9033),
        'Ohio': (-82.9071, 40.4173),
        'Georgia': (-83.5389, 32.1656),
        'North Carolina': (-79.0193, 35.4596),
        'Michigan': (-84.5068, 43.1148),
        '6': (-74.4057, 40.0583),
        'Virginia': (-78.2494, 37.5407),
        'Washington': (-120.3321, 46.8062),
        'Arizona': (-111.2937, 34.4484),
        '3': (-71.4589, 42.3601),
        'Tennessee': (-86.7816, 35.8627),
        'Indiana': (-86.1349, 39.7684),
        'Missouri': (-92.3295, 38.5767),
        '8': (-76.7413, 39.0458),
        'Wisconsin': (-89.4012, 44.2731),
        'Colorado': (-105.9821, 39.2501),
        'Minnesota': (-94.4650, 46.0778),
        'South Carolina': (-81.1637, 33.8361),
        'Alabama': (-86.6023, 33.3182),
        'Louisiana': (-91.8749, 30.0843),
        'Kentucky': (-84.7700, 37.4393),
        'Oregon': (-120.6765, 43.8393),
        'Oklahoma': (-97.0929, 35.0078),
        '5': (-73.0877, 41.6032),
        'Iowa': (-93.6977, 41.8780),
        'Mississippi': (-89.4985, 32.3547),
        'Arkansas': (-92.3311, 34.7465),
        'Utah': (-111.8535, 39.5608),
        'Nevada': (-116.4398, 39.1699),
        'Kansas': (-98.4842, 38.4119),
        'New Mexico': (-105.6056, 34.5199),
        'Nebraska': (-99.9018, 41.4925),
        '9': (-80.7549, 38.3498),
        'Idaho': (-114.7420, 44.0682),
        'Maine': (-69.0455, 45.2538),
        '1': (-71.5724, 43.1939),
        '4': (-71.4828, 41.5801),
        'Montana': (-109.3626, 46.8797),
        '7': (-75.5277, 38.9108),
        'South Dakota': (-99.9018, 44.3683),
        'North Dakota': (-100.7837, 47.5515),
        '2': (-72.6778, 44.1588),
        'Wyoming': (-107.2903, 43.0760)
    }
    states_digit = {'1': 'New Hamsphire', '2': 'Vermont', '3': 'Massachusetts', '4': 'Rhode Island',
                    '5': 'Connecticut', '6': 'New Jersey', '7': 'Delaware', '8': 'Maryland', 
                        '9': 'West Virginia'}
    
    fig = plt.figure(figsize=(10,8))  
    ax = fig.add_subplot(1,1,1)

    m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
        projection='lcc',lat_1=33,lat_2=45,lon_0=-95, ax=ax)  # Tạo một bản đồ
    m.readshapefile('st99_d00', 'states')  #Đọc file shapefile và vẽ các state lên bản đồ
    for state, coords in state_coords.items():
        lon, lat = coords
        x, y = m(lon, lat)
        plt.text(x, y, state, fontsize=7, fontweight = 'bold', ha='center', va='center', color='red', fontname = 'Georgia')
    for info, shape in zip(m.states_info, m.states):
        if info['NAME'] in states_to_fill:
            poly = Polygon(shape, facecolor='yellow')
            plt.gca().add_patch(poly)
    for i, name in states_digit.items():
        lon, lat = state_coords[i]  
        x, y = m(lon, lat) 
        plt.scatter(x, y, label=f'{i}: {name}')
    fig.legend(title = 'Map Annotation' , loc='upper center', ncol=2, prop={'family': 'Georgia'})
    return fig

st.sidebar.markdown('Menu')

if "label" not in st.session_state:
    st.session_state["label"] = ''
if "flag_anima" not in st.session_state:
    st.session_state["flag_anima"] = False
if st.session_state["flag_anima"] == False:
    if "flag_ve_ban_do" not in st.session_state:
        st.session_state["flag_ve_ban_do"] = True
        fig = ve_ban_do([])
        st.session_state['fig'] = fig
        st.pyplot(fig)
        print (st.session_state["flag_ve_ban_do"])
        print ("Vẽ bản đồ lần đầu")
    else:
        if st.session_state["flag_ve_ban_do"] == False:
            st.session_state["flag_ve_ban_do"] = True
            fig = ve_ban_do([])
            st.session_state['fig'] = fig
            st.pyplot(fig)
        else:
            print("Đã ve bản đồ")
            st.pyplot(st.session_state['fig'])
    if st.sidebar.button('Coastal States'):
        state_to_fill = []
        output = run(0, x, coastal(x))
        for item in output:
            state_to_fill.append(item)
            states = ', '.join(state_to_fill)
        st.session_state['label'] = 'Coastal States: '
        st.session_state['label'] += states
        fig = ve_ban_do(state_to_fill)
        st.session_state['fig'] = fig
        st.rerun()  
    #select_states = st.selectbox('Select States', st.lst_city)
    select_states = st.sidebar.selectbox('Select States', st.lst_city)
    if st.sidebar.button('Adjacent States'):
        state_to_fill = []
        output = run(0, x, adjacent(select_states, x))
        for item in output:
            state_to_fill.append(item)
            states = ', '.join(state_to_fill)
        st.session_state['label'] = 'Adjacent States: '
        st.session_state['label'] += states
        fig = ve_ban_do(state_to_fill)
        st.session_state['fig'] = fig
        st.rerun()
    if st.sidebar.button('Coastal States Adjacent'):
        state_to_fill = []
        states = ''
        output = run(0, x, adjacent(select_states, x), coastal(x))
        for item in output:
            state_to_fill.append(item)
            states = ', '.join(state_to_fill)
        st.session_state['label'] = 'Coastal States Adjacent: ' 
        st.session_state['label'] += states
        if len(state_to_fill) == 0:
            st.session_state['label'] = 'There are no states adjacent to ' + select_states + ' that are also coastal'
        fig = ve_ban_do(state_to_fill)
        st.session_state['fig'] = fig
        st.rerun()
    select_2_states = st.sidebar.selectbox('Select The Second State', st.lst_city)
    if st.sidebar.button('States that border the two chosen states'):
        state_to_fill = []
        states = ''
        output = run(0,x,adjacent(select_states, x), adjacent(select_2_states, x))
        for item in output:
            state_to_fill.append(item)
            states = ', '.join(state_to_fill)
        st.session_state['label'] = 'States that border the two chosen states: '
        st.session_state['label'] += states
        if len(state_to_fill) == 0:
            st.session_state['label'] = 'There are no states that are adjacent to ' + select_states + ' and ' + select_2_states
        fig = ve_ban_do(state_to_fill)
        st.session_state['fig'] = fig
        st.rerun()
    if st.session_state["label"] != '':
        st.write(st.session_state["label"])
        
else:
    if st.session_state["flag_anim"] == True:
        components.html(st.session_state["anim"].to_jshtml(), height=550)
        _, _, col3, _, _ = st.columns(5)
        with col3:
            if col3.button('Reset'):
                st.session_state["flag_anim"] = False
                st.session_state["flag_ve_ban_do"] = False
                st.rerun()

