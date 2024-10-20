import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gdp
import mapclassify
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import plotly.figure_factory as ff


st.set_page_config(layout="wide")

data = gdp.read_file('/home/angel/Documents/galois/EnergyStreamlit/data/data.shp')

# side bar ===========================================

markdown = """info"""
st.sidebar.title("About")
st.sidebar.info(markdown)
st.sidebar.image("https://i.imgur.com/UbOXYAU.png")

# BODY =============================================

st.title("Marker Cluster")

col1, col2,col3 = st.columns([1, 1, 1]) 
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
# Define layout using st.columns
col1, col2 = st.columns([2, 1])  # Ratio of space for map and plot (2:1)

# Column 1: Display the map
with col1:
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
    m.to_streamlit(height=600, width=900)

# Column 2: Display the histogram
with col2:
    st.markdown('''Leafmap is a Python package for interactive mapping and geospatial 
                analysis with minimal coding in a Jupyter environment. It is a spin-off 
                project of the geemap Python package, which was designed specifically to 
                work with Google Earth Engine (GEE). However, not everyone in the geospatial 
                community has access to the GEE cloud computing platform. Leafmap is designed 
                 fill this gap for non-GEE users.''')


    if select_schema == "Quantiles":
        classes = mapclassify.Quantiles(data[select_column], number_classes)
    elif select_schema == "EqualInterval":
        classes = mapclassify.EqualInterval(data[select_column], number_classes)
    elif select_schema == "FisherJenks":
        classes = mapclassify.FisherJenks(data[select_column], number_classes)
    else:
        classes = mapclassify.NaturalBreaks(data[select_column], number_classes)

    # Convert plot size from pixels to inches
    px = 1 / plt.rcParams['figure.dpi']  # Pixel in inches
    group_labels = ['distplot']
    fig = ff.create_distplot([data[select_column].values], 
                             group_labels,
                             bin_size=(data[select_column].max()-data[select_column].min())/int(np.log2(data.shape[0]+1)))
    for q in classes.bins:
        fig.add_vline(x=q, line_width=3, line_dash="dash", line_color="green")


    st.plotly_chart(fig, use_container_width=True)



with st.expander("See source code"):
    with st.echo():
        #code that I want to show
        print('code that I want to show to user')
