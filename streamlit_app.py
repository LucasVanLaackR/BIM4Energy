import streamlit as st
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import folium

# Function to perform reverse geocoding
def reverse_geocode(lat, lon):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse([lat, lon], exactly_one=True)
    if location:
        return location.address
    else:
        return "", ""

st.title('BIM4ENERGY Assessment')

# Sidebar for map and user inputs
with st.sidebar:
    st.header('Select Your Location on the Map')
    default_location = [59.9139, 10.7522]  # Center of Norway
    m = folium.Map(location=default_location, zoom_start=5)

    # Folium map in Streamlit
    map_response = st_folium(m, width=725, height=500)

    # If a location is selected, get the country and coordinates
    if map_response['last_clicked']:
        lat, lon = map_response['last_clicked']['lat'], map_response['last_clicked']['lng']
        address = reverse_geocode(lat, lon)
        country = address.split(',')[-1].strip() if address else ""
        coordinates = f"{lat}, {lon}"
    else:
        country = "Norway"  # Default
        coordinates = "59.9077106, 10.6785692"  # Default

    st.header('Project Information')
    projectName = st.text_input('Project Name', 'My Project 1')
    country = st.text_input('Country', country)
    coordinates = st.text_input('Coordinates', coordinates)
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

# Calculations based on inputs
areaGrossFloorAboveGround = areaGrossFloor
areaGrossFloorBelowGround = 0
areaFootPrint = areaGrossFloor / (numberFloorsAboveGround + numberFloorsBelowGround)
heightFloorToFloor = heightFloorToCeiling + 0.4  # Assuming thicknessFloor is 0.4

buildingHeight = 3 * numberFloorsAboveGround
buildingDepth = st.number_input('Building Depth', value=14)  # User input
buildingWidth = st.number_input('Building Width', value=14)  # User input
areaGroundSlab = areaFootPrint
areaUpperSlabs = areaFootPrint * numberFloorsAboveGround
lengthFootPrint = buildingDepth * 2 + buildingWidth * 2
areaExternalFacade = lengthFootPrint * buildingHeight
windowRatio = 0.4
areaExternalWindow = areaExternalFacade * windowRatio
areaExternalWall = areaExternalFacade - areaExternalWindow
areaRoof = areaFootPrint

# Building standards dictionary
buildingStandard = {
    "Norway": {
        "TEK87": {
            "Single Family": {
                "Space Heating": 100,
                "Service Water Heating": 20,
                "Fans and Pumps": 6,
                "Internal Lighting": 24,
                "Miscellaneous": 25
            }
        },
        "TEK97": {
            "Single Family": {
                "Space Heating": 93,
                "Service Water Heating": 31,
                "Fans and Pumps": 8,
                "Internal Lighting": 18,
                "Miscellaneous": 24
            }
        },
    }
}

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
