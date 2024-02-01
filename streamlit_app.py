import streamlit as st
from streamlit_folium import st_folium
import folium

# Initialize default coordinates
DEFAULT_LATITUDE = 59.9139
DEFAULT_LONGITUDE = 10.7522

# Streamlit app title
st.title('BIM4ENERGY Assessment')

# Map setup to select location
st.header('Select a Location on the Map')
m = folium.Map(location=[DEFAULT_LATITUDE, DEFAULT_LONGITUDE], zoom_start=10)
m.add_child(folium.LatLngPopup())

f_map = st_folium(m, width=725)

# Attempt to get last clicked position or use default
selected_latitude = DEFAULT_LATITUDE
selected_longitude = DEFAULT_LONGITUDE

if f_map.get("last_clicked"):
    selected_latitude = f_map["last_clicked"]["lat"]
    selected_longitude = f_map["last_clicked"]["lng"]

# Convert selected coordinates into string format for the input field
selected_coordinates = f"{selected_latitude}, {selected_longitude}"

# Sidebar for user inputs
with st.sidebar:
    st.header('Project Information')
    projectName = st.text_input('Project Name', 'My Project 1')
    country = st.text_input('Country', 'Norway')
    # Coordinates input field now uses the map-selected coordinates
    coordinates = st.text_input('Coordinates', value=selected_coordinates)
    buildingType = st.selectbox('Building Type', ['Residential', 'Commercial', 'Industrial'])
    yearConstructionCompletion = st.text_input('Year of Construction Completion', '1950')
    numberBuildingUsers = st.number_input('Number of Building Users', min_value=1, value=4, step=1)

    st.header('Building Information')
    areaGrossFloor = st.number_input('Gross Floor Area', value=200)
    conditionedArea = st.number_input('Conditioned Area', value=150)
    numberFloorsAboveGround = st.number_input('Number of Floors Above Ground', value=2, min_value=0)
    numberFloorsBelowGround = st.number_input('Number of Floors Below Ground', value=0, min_value=0)
    heightFloorToCeiling = st.number_input('Height from Floor to Ceiling', value=3.0)
    
    st.header('Assessment Information')
    selectBuildingStandard = st.selectbox('Building Standard', ['TEK87', 'TEK97'])

# Building standards and energy consumption calculations remain unchanged

# Display Project Information
st.subheader('Project Information')
st.write(f"Project Name: {projectName}")
st.write(f"Country: {country}")
st.write(f"Coordinates: {coordinates}")
st.write(f"Building Type: {buildingType}")
st.write(f"Year of Construction Completion: {yearConstructionCompletion}")
st.write(f"Number of Building Users: {numberBuildingUsers}")

# Energy Consumption Calculation
energy_consumption = {
    "Space Heating": areaGrossFloor * buildingStandard["Norway"][selectBuildingStandard]["Single Family"]["Space Heating"],
    "Service Water Heating": areaGrossFloor * buildingStandard["Norway"][selectBuildingStandard]["Single Family"]["Service Water Heating"],
    "Fans and Pumps": areaGrossFloor * buildingStandard["Norway"][selectBuildingStandard]["Single Family"]["Fans and Pumps"],
    "Internal Lighting": areaGrossFloor * buildingStandard["Norway"][selectBuildingStandard]["Single Family"]["Internal Lighting"],
    "Miscellaneous": areaGrossFloor * buildingStandard["Norway"][selectBuildingStandard]["Single Family"]["Miscellaneous"]
}

# Display Calculated Energy Consumption
st.subheader('Energy Consumption')
for key, value in energy_consumption.items():
    st.write(f"{key}: {value} kWh")
