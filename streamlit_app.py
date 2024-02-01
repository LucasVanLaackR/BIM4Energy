import streamlit as st
from streamlit_folium import st_folium
import folium
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

# Function to perform reverse geocoding
def reverse_geocode(lat, lon):
    geolocator = Nominatim(user_agent="streamlit_geopy_user")
    try:
        location = geolocator.reverse((lat, lon), exactly_one=True)
        if location:
            return location.address
    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        st.error(f"Geocoding error: {e}")
    return None

# Display logo
logo_url = 'https://www.bim4energy.eu/wp-content/uploads/2024/02/Geometric-Logo-3_Colors-1.png'
st.sidebar.image(logo_url, width=300)  # Adjust the width as needed

# Streamlit app title
st.title('BIM4ENERGY Assessment')

# Define Building standards dictionary
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

# Sidebar for user inputs and map
with st.sidebar:
    # Initialize default coordinates
    DEFAULT_LATITUDE, DEFAULT_LONGITUDE = 59.9139, 10.7522

    st.header('Select Your Location on the Map')
    m = folium.Map(location=[DEFAULT_LATITUDE, DEFAULT_LONGITUDE], zoom_start=4)
    m.add_child(folium.LatLngPopup())

    f_map = st_folium(m, width=330, height=500)

    # Attempt to get last clicked position or use default
    country_name = "Norway"  # Default country
    selected_coordinates = f"{DEFAULT_LATITUDE}, {DEFAULT_LONGITUDE}"
    if f_map.get("last_clicked"):
        selected_latitude = f_map["last_clicked"]["lat"]
        selected_longitude = f_map["last_clicked"]["lng"]
        selected_coordinates = f"{selected_latitude}, {selected_longitude}"
        address = reverse_geocode(selected_latitude, selected_longitude)
        if address:
            country_name = address.split(',')[-1].strip()

    st.header('Project Information')
    projectName = st.text_input('Project Name', 'My Project 1')
    country = st.text_input('Country', country_name)
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

# Project information and calculations (mockup, replace with your logic)
energy_consumption = {
    "Space Heating": areaGrossFloor * buildingStandard["Norway"][selectBuildingStandard]["Single Family"]["Space Heating"],
    "Service Water Heating": areaGross
