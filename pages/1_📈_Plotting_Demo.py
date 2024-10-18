import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gdp

st.set_page_config(layout="wide")
data = gdp.read_file('/home/angel/Documents/galois/EnergyUseStreamlit/data/data.shp')

# side bar -----------------------------------

markdown = """info"""
st.sidebar.title("About")
st.sidebar.info(markdown)
st.sidebar.image("https://i.imgur.com/UbOXYAU.png")

# body -------------------------------

st.title("Marker Cluster")

m = leafmap.Map(center=[40, -100], zoom=4)
m.add_xyz_service("xyz.Esri.WorldGrayCanvas")

m.add_data(
    data=data, 
    column="CONSUMO_KW", 
    scheme="NaturalBreaks", 
    cmap="Blues", 
    style={'stroke':False},
    legend_title="Population"
)
m.to_streamlit(height=700)



with st.expander("See source code"):
    with st.echo():
        #code that I want to show
        print('code that I want to show to user')
