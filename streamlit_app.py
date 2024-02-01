import streamlit as st
from streamlit_folium import st_folium
import folium
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

# Streamlit app title
st.title('BIM4ENERGY Assessment')

# Sidebar for user inputs and map
with st.sidebar:
    # Initialize default coordinates
    DEFAULT_LATITUDE = 59.9139
    DEFAULT_LONGITUDE = 10.7522

    st.header('Select Your Location on the Map')
    m = folium.Map(location=[DEFAULT_LATITUDE, DEFAULT_LONGITUDE], zoom_start=10)
    m.add_child(folium.LatLngPopup())

    f_map = st_folium(m, width=330, height=500)  # Adjust the width and height if needed

    # Attempt to get last clicked position or use default
    if f_map.get("last_clicked"):
        selected_latitude = f_map["last_clicked"]["lat"]
        selected_longitude = f_map["last_clicked"]["lng"]
        selected_coordinates = f"{selected_latitude}, {selected_longitude}"
    else:
        selected_coordinates = f"{DEFAULT_LATITUDE}, {DEFAULT_LONGITUDE}"

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

# Create a PDF 
def create_pdf(project_info, energy_consumption):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Add your PDF content here
    c.drawString(100, 800, "BIM4ENERGY Assessment Report")
    c.drawString(100, 780, f"Project Name: {project_info['projectName']}")
    c.drawString(100, 760, f"Country: {project_info['country']}")
    c.drawString(100, 740, f"Coordinates: {project_info['coordinates']}")

    # Energy Consumption
    y_position = 720
    for key, value in energy_consumption.items():
        c.drawString(100, y_position, f"{key}: {value} kWh")
        y_position -= 20

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

# Assuming you have gathered project_info and energy_consumption in the right format
project_info = {
    'projectName': projectName,
    'country': country,
    'coordinates': coordinates,
    # Add other project details as necessary
}

# Assuming energy_consumption is a dictionary with your calculated values
energy_consumption = {
    # Your calculated energy consumption data here...
}

# Place to add the PDF generation button
if st.button('Generate PDF Report'):
    pdf_bytes = create_pdf(project_info, energy_consumption)
    st.download_button(label='Download PDF Report',
                       data=pdf_bytes,
                       file_name='bim4energy_report.pdf',
                       mime='application/pdf')
