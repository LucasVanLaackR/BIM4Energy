import streamlit as st
from streamlit_folium import st_folium
import folium
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import pyvista as pv

# Define the buildingStandard dictionary here, so it's accessible in the main() function
buildingStandard = {
        "Norway": 
            { 
            "TEK87" : 
                {    
                "Single Family" : 
                    {
                    "Space Heating": 100,
                    "Space Cooling": 0,
                    "Service Water Heating": 20,
                    "Fans and Pumps": 6,
                    "Internal Lighting": 24,
                    "Miscellaneous": 25                    
                    },
                "Apartment" : 
                    {
                    "Space Heating": 97,
                    "Space Cooling": 0,
                    "Service Water Heating": 30,
                    "Fans and Pumps": 7,
                    "Internal Lighting": 24,
                    "Miscellaneous": 27                    
                    },  
                "Office" : 
                    {
                    "Space Heating": 96,
                    "Space Cooling": 21,
                    "Service Water Heating": 5,
                    "Fans and Pumps": 46,
                    "Internal Lighting": 47,
                    "Miscellaneous": 34                    
                    }            
                },
            "TEK97" : 
                {    
                "Single Family" : 
                    {
                    "Space Heating": 93,
                    "Space Cooling": 0,
                    "Service Water Heating": 31,
                    "Fans and Pumps": 8,
                    "Internal Lighting": 18,
                    "Miscellaneous": 24                    
                    },
                "Apartment" : 
                    {
                    "Space Heating": 81,
                    "Space Cooling": 0,
                    "Service Water Heating": 26,
                    "Fans and Pumps": 9,
                    "Internal Lighting": 15,
                    "Miscellaneous": 20                    
                    },  
                "Office" : 
                    {
                    "Space Heating": 117,
                    "Space Cooling": 19,
                    "Service Water Heating": 4,
                    "Fans and Pumps": 17,
                    "Internal Lighting": 19,
                    "Miscellaneous": 26                    
                    } 
                },                    
            "TEK07" : 
                {    
                "Single Family" : 
                    {
                    "Space Heating": 57,
                    "Space Cooling": 0,
                    "Service Water Heating": 30,
                    "Fans and Pumps": 8,
                    "Internal Lighting": 17,
                    "Miscellaneous": 23                    
                    },
                "Apartment" : 
                    {
                    "Space Heating": 37,
                    "Space Cooling": 0,
                    "Service Water Heating": 30,
                    "Fans and Pumps": 10,
                    "Internal Lighting": 17,
                    "Miscellaneous": 23                    
                    },  
                "Office" : 
                    {
                    "Space Heating": 54,
                    "Space Cooling": 24,
                    "Service Water Heating": 5,
                    "Fans and Pumps": 22,
                    "Internal Lighting": 25,
                    "Miscellaneous": 34                    
                    } 
                }, 
            "TEK10" : 
                {    
                "Single Family" : 
                    {
                    "Space Heating": 52,
                    "Space Cooling": 0,
                    "Service Water Heating": 30,
                    "Fans and Pumps": 8,
                    "Internal Lighting": 17,
                    "Miscellaneous": 23                    
                    },
                "Apartment" : 
                    {
                    "Space Heating": 32,
                    "Space Cooling": 0,
                    "Service Water Heating": 30,
                    "Fans and Pumps": 10,
                    "Internal Lighting": 17,
                    "Miscellaneous": 23                    
                    },  
                "Office" : 
                    {
                    "Space Heating": 39,
                    "Space Cooling": 24,
                    "Service Water Heating": 5,
                    "Fans and Pumps": 22,
                    "Internal Lighting": 25,
                    "Miscellaneous": 34                    
                    } 
                },  
            "TEK17" : 
                {    
                "Single Family" : 
                    {
                    "Space Heating": 48,
                    "Space Cooling": 0,
                    "Service Water Heating": 30,
                    "Fans and Pumps": 8,
                    "Internal Lighting": 14,
                    "Miscellaneous": 19                    
                    },
                "Apartment" : 
                    {
                    "Space Heating": 30,
                    "Space Cooling": 0,
                    "Service Water Heating": 30,
                    "Fans and Pumps": 8,
                    "Internal Lighting": 14,
                    "Miscellaneous": 20                    
                    },  
                "Office" : 
                    {
                    "Space Heating": 31,
                    "Space Cooling": 19,
                    "Service Water Heating": 5,
                    "Fans and Pumps": 17,
                    "Internal Lighting": 19,
                    "Miscellaneous": 26                    
                    } 
                }                    
            }
        }



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

# Function to create a PDF report
def create_pdf(project_info, energy_consumption):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 800, "BIM4ENERGY Assessment Report")
    c.drawString(100, 780, f"Project Name: {project_info['projectName']}")
    c.drawString(100, 760, f"Country: {project_info['country']}")
    c.drawString(100, 740, f"Coordinates: {project_info['coordinates']}")
    y_position = 720
    for key, value in energy_consumption.items():
        c.drawString(100, y_position, f"{key}: {value} kWh")
        y_position -= 20
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

# Main app
def main():
    # Display logo and app title
    st.sidebar.image('https://www.bim4energy.eu/wp-content/uploads/2024/02/Geometric-Logo-3_Colors-1.png', width=300)
    st.title('BIM4ENERGY Assessment')

    # User input for project information
    with st.sidebar:
        st.header('Select Your Location on the Map')
        # Map setup
        DEFAULT_LATITUDE, DEFAULT_LONGITUDE = 59.9139, 10.7522
        m = folium.Map(location=[DEFAULT_LATITUDE, DEFAULT_LONGITUDE], zoom_start=4)
        m.add_child(folium.LatLngPopup())
        f_map = st_folium(m, width=330, height=500)
        country_name, selected_coordinates = "Norway", f"{DEFAULT_LATITUDE}, {DEFAULT_LONGITUDE}"
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

    # Project information and calculations
    project_info = {
        'projectName': projectName,
        'country': country,
        'coordinates': coordinates,
    }
    energy_consumption = {
        "Space Heating": areaGrossFloor * buildingStandard["Norway"][selectBuildingStandard]["Single Family"]["Space Heating"],
        "Service Water Heating": areaGrossFloor * buildingStandard["Norway"][selectBuildingStandard]["Single Family"]["Service Water Heating"],
        "Fans and Pumps": areaGrossFloor * buildingStandard["Norway"][selectBuildingStandard]["Single Family"]["Fans and Pumps"],
        "Internal Lighting": areaGrossFloor * buildingStandard["Norway"][selectBuildingStandard]["Single Family"]["Internal Lighting"],
        "Miscellaneous": areaGrossFloor * buildingStandard["Norway"][selectBuildingStandard]["Single Family"]["Miscellaneous"]
    }

    # Layout for 3D visualization and text results
    col1, col2 = st.columns([3, 2])
    """
    with col1:
        st.header("3D Building Visualization")
        # PyVista plot setup
        plotter = pv.Plotter(off_screen=True)
        cube = pv.Cube(center=(0, 0, 0), x_length=4, y_length=4, z_length=4)
        plotter.add_mesh(cube, color='cyan', show_edges=True)
        plotter.set_background('white')
        plotter.camera_position = 'iso'
        
        # Generate screenshot of the plot
        img = plotter.screenshot()
        
        # Display the screenshot in Streamlit
        st.image(img, caption='3D Cube Visualization', use_column_width=True)
    """
    with col2:
        # Display Project Information
        st.subheader('Project Information')
        st.write(f"Project Name: {projectName}")
        st.write(f"Country: {country}")
        st.write(f"Coordinates: {coordinates}")
        st.write(f"Building Type: {buildingType}")
        st.write(f"Year of Construction Completion: {yearConstructionCompletion}")
        st.write(f"Number of Building Users: {numberBuildingUsers}")
        # Display Calculated Energy Consumption
        st.subheader('Energy Consumption')
        for key, value in energy_consumption.items():
            st.write(f"{key}: {value} kWh")
        # Generate and download PDF report button
        if st.button('Generate PDF Report'):
            pdf_bytes = create_pdf(project_info, energy_consumption)
            st.download_button(label="Download PDF Report",
                               data=pdf_bytes,
                               file_name="BIM4ENERGY_Report.pdf",
                               mime="application/pdf")

if __name__ == "__main__":
    main()
