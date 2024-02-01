import streamlit as st

# Streamlit app title
st.title('BIM4ENERGY Assessment')

# Sidebar for user inputs
with st.sidebar:
    st.header('Project Information')
    projectName = st.text_input('Project Name', 'My Project 1')
    country = st.text_input('Country', 'Norway')
    coordinates = st.text_input('Coordinates', '59.9077106, 10.6785692')
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

# Instructions for running the app will be provided in the text after the code.
