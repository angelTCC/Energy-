import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gdp
import mapclassify
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import plotly.express as px
import mapclassify

st.set_page_config(layout="wide")

data = gdp.read_file('/home/angel/Documents/galois/EnergyStreamlit/data/data.shp')

# SIDE BAR ===========================================

markdown = """info"""
st.sidebar.title("About")
st.sidebar.info(markdown)
st.sidebar.image("https://i.imgur.com/UbOXYAU.png")

# INTRODUCTION =============================================

st.title("Choropleth map")
st.markdown('''
            On this page, I will show the energy characteristics such as consumption, 
            generation potential, and the amount of money spent using a choropleth map. 
            You can select the number of classes and the scheme to categorize the groups. 
            Additionally, you can visualize the selected data with a histogram. 
            You can remove outliers to improve the visualization; however, the removed data 
            will be displayed.
            ''')


## SELECTBOX ========================================================

col1, col2,col3, col4 = st.columns([1, 1, 1, 1]) 
with col3:

    select_schema = st.selectbox(
        "Select the Schema.",
        ("Quantiles", "EqualInterval", "FisherJenks", "NaturalBreaks"),
        index=0,
    )

with col1:
    select_column = st.selectbox(
        "Select the Column.",
        ("CONSUMO_KW", "MONTO_SOLE", "POTENCIA_C"),
        index=0,
    )
with col2:
    number_classes = st.selectbox(
        "Number of classes.",
        (2, 3, 4,5 ,6),
        index=0,
    )
with col4:
    max_value = st.slider(
    "Take values up to",
    value=data[select_column].max(),
    )

    agree = st.checkbox(label="Show data don't selected",
                        value=True)
    
# HISTOGRAM AND DATAFRAME  ====================================================

col1, col2 = st.columns([1, 1])  # Ratio of space for map and plot (2:1)

dummi = data.loc[data[select_column] <= max_value, select_column]
dummi2 = data.loc[data[select_column] > max_value, :]#data.columns.difference([select_column])]

# HISTROGRAM

with col1:

    if select_schema == "Quantiles":
        classes = mapclassify.Quantiles(dummi, number_classes)
    elif select_schema == "EqualInterval":
        classes = mapclassify.EqualInterval(dummi, number_classes)
    elif select_schema == "FisherJenks":
        classes = mapclassify.FisherJenks(dummi, number_classes)
    elif select_schema == "NaturalBreaks":
        classes = mapclassify.NaturalBreaks(dummi, number_classes)

    fig = px.histogram(dummi, 
                    x=select_column,
                    marginal="box", # or violin, rug
                    nbins=int((dummi.max()-dummi.min())/int(np.log2(data.shape[0]+1)))
                    )

    for q in classes.bins:
        fig.add_vline(x=q, line_width=3, line_dash="dash", line_color="green")

    st.plotly_chart(fig, use_container_width=True)

# DATAFRAME

with col2:
    if agree:
        if dummi2.shape[0]!=0:
            st.dataframe(dummi2.drop(columns=['geometry']))
        else:
            st.markdown('''Here the dataframe will be showed''')


## MAP ===================================================

m = leafmap.Map(center=[40, -100], zoom=4)
m.add_xyz_service("xyz.Esri.WorldGrayCanvas")
m.add_data(
    data=data, 
    column=select_column, 
    scheme=select_schema, 
    k=number_classes,
    cmap="Blues", 
    style={'stroke': False},
    legend_title="Population"
)
m.to_streamlit()#height=600, width=900)

with st.expander("See source code"):
    with st.echo():
        #code that I want to show
        print('code that I want to show to user')
