# main app
# >>> streamlit run app.py

import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import altair as alt
import networkx as nx
from pyvis.network import Network

from param import col_dict, snames, max_node_map, def_node_map
from util import parse_data, clock, rc


#####################
### INITIAL SETUP ###
#####################

# styling
st.set_page_config(page_title='ShakespeareCA', page_icon=f"data/shakespeare.png")

st.markdown(""" <style> 
        #MainMenu {visibility: hidden;} 
        footer {visibility: hidden;} 
        </style> """, unsafe_allow_html=True)

padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)


st.sidebar.markdown('# Shakespeare Character Interactions')

# for selecting series
series_pick = st.sidebar.selectbox('Shakespeare Werk wählen:',
                                   list(snames.values()),
                                   key='series', index=0)
snames_r = {v: k for k, v in snames.items()}
series_code = snames_r[series_pick]  # for later use

# initial parse data
df, chars, relationships = parse_data(series_code)
chars_sorted = np.sort(chars)  # for ordered dropbox

###########################
#### INTERACTIONS CHART ###
###########################

# define options in sidebar
st.sidebar.markdown('## Netzwerk Optionen')
physics_bool = st.sidebar.checkbox(
    'Physik-Engine hinzufügen', key='phys', value=False)
box_bool = st.sidebar.checkbox('Knotenboxen', key='boxb', value=False)
col_bool = st.sidebar.checkbox('Zufällige Farben', key='colb', value=False)

max_node = max_node_map[series_code]
default_node = def_node_map[series_code]


interactions = st.sidebar.slider(
    label="Anzahl der Charactere",
    min_value=4,
    max_value=23,
    step=1,
    value=default_node)


st.markdown(
    '''#### INTERACTION NETWORK
Dickere Linien = Mehr Interaktion. \n
Klicke und ziehe an den Knoten, um die Interaktionen der einzelnen Charaktere sichtbarer zu machen. 
''')

nx_graph = nx.empty_graph(interactions)  # create initial dummy graph
chars_subset = chars[:interactions]  # select characer subset

#  positions depend on number of interactions
clockface = clock[interactions]
pos_dict = {chars[i]: clockface[i]
            for i in range(interactions)}  # positions for character
name2node = {}  # for mapping from node idx to character name


# add each character node
for idx, c in enumerate(chars_subset):

    name2node[c] = idx
    for k, v in {'label': c,
                 'mass': 10,
                 'physics': physics_bool,
                 'x': (pos_dict[c][0]) * 1.6 * 500,
                 'y': (pos_dict[c][1]) * 1.1 * 500,
                 'size': 20,
                 'shape': 'box' if box_bool else 'dot',
                 'color': f'rgb({rc()},{rc()},{rc()})' if col_bool
                 else col_dict[series_code][c]
                 }.items():

        nx_graph.nodes[idx][k] = v


# add each interaction edge
for wt, fr, to in relationships.values:
    if (to in chars_subset) & (fr in chars_subset) & (fr != to):
        if wt > 0:
            nx_graph.add_edge(name2node[fr], name2node[to],
                              width=wt/4.5,
                              color='#094230')


# translate to pyvis network
h, w = 500, 750
nt = Network(f'{h}px', f'{w}px',
             font_color='white' if box_bool else 'black')
nt.from_nx(nx_graph)
path = f'network.html'
nt.show(path)
HtmlFile = open(path, 'r')  # , encoding='utf-8')
source_code = HtmlFile.read()
components.html(source_code, height=h * 1.1, width=w * 1.1)



###############
#### ABOUT ####
###############

st.sidebar.markdown('''
## ABOUT
Code: https://github.com/isabelhansen\n
Code Inspiration Credits: https://github.com/gmorinan/trekviz\n 
Digitale Sammlung: https://shakespeare.folger.edu/ \n
Tools: [Streamlit](https://streamlit.io/), [Altair](https://altair-viz.github.io/), [Networkx](https://networkx.org/) & [Pyvis](https://pyvis.readthedocs.io/en/latest/)
''')