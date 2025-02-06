import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
import geopandas as gpd

st.set_page_config(
    page_title="World Geospatial Dashboard by Tommy"
)


@st.cache_data
def get_data():
    url = "https://raw.githubusercontent.com/tommyscodebase/12_Days_Geospatial_Python_Bootcamp/refs/heads/main/13_final_project_data/world_population.csv"

    geo_url = "https://raw.githubusercontent.com/tommyscodebase/12_Days_Geospatial_Python_Bootcamp/refs/heads/main/13_final_project_data/world.geojson"

    try:
        df = pd.read_csv(url)
        gdf = gpd.read_file(geo_url)
        return df, gdf
    except Exception as e:
        st.error(f"An error occured: {e}")
        return None, None
    

data, geodata = get_data()


def get_country_boundary(country):
    country_bounds = geodata[geodata['name'] == country]

    if country_bounds.empty:
        return None
    return country_bounds





# Header
st.title("World Population Dashboard")
st.write("Select a country to view its population data and geographical information")

# Country slection
country = st.selectbox(label="Select a country", options=[""] + list(data["Country/Territory"].unique()), key="selected_country")

country_boundary = get_country_boundary(country=country)

if country:
    country_data = data[data['Country/Territory'] == country].iloc[0]

    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("Population Over Selected Years")

        years = ["2022 Population", "2020 Population", "2015 Population", "2010 Population", "2000 Population", "1990 Population", "1980 Population", "1970 Population"]

        selected_years = st.multiselect(label="Select Population Years", options=years, default=years[:3])

        # Create a dataframe and pass it to plotly
        population_data = {
            "Year": [year.split()[0] for year in selected_years],
            "Population": [country_data[year] for year in selected_years]
        }

        population_df = pd.DataFrame(population_data)


        # Display the chart
        fig = px.bar(population_df, x="Year", y="Population", title=f"Population of {country} over Selected Years")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        if country_data is not None:
            # Country Statistics
            st.subheader("Country Statistics")
            st.write(f"**Area (km²):** {country_data['Area (km²)']} km²")
            st.write(f"**Density (per km²):** {country_data['Density (per km²)']} people/km²")
            st.write(f"**Growth Rate:** {country_data['Growth Rate']}%")
            st.write(f"**World Population Percentage:** {country_data['World Population Percentage']}%")

            # Map
            bounds = country_boundary.total_bounds
            st.subheader("Country Map")
            m = folium.Map()
            folium.GeoJson(data=country_boundary).add_to(m)
            m.fit_bounds([
                [bounds[1], bounds[0]],
                [bounds[3], bounds[2]],
            ])

            st_folium(m, width=300, height=300, use_container_width=True)
else:
    st.write("Select a country to view its data")
