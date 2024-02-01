import streamlit as st
from streamlit_folium import st_folium
import folium
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import pyvista as pv
from PIL import Image
import numpy as np

# Define the buildingStandard dictionary here, so it's accessible in the main() function
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

# Function to generate and display a 3D cube
def generate_3d_cube():
    plotter = pv.Plotter(off_screen=True)
    cube = pv.Cube(center=(0, 0, 0), x_length=4, y_length=4, z_length=4)
    plotter.add_mesh(cube, color='cyan', show_edges=True)
    plotter.set_background('white')
    plotter.camera_position = 'xy'
    img = plotter.screenshot()
    return img

# Main app
def main():
    # Display logo and app title
    st.sidebar.image('https://www.bim4energy.eu/wp-content/uploads/2024/02/Geometric-Logo-3_Colors-1.png', width=300)
    st.title('BIM4ENERGY Assessment')
    # Your existing setup code for user inputs...

    # Layout for 3D visualization and text results
    col1, col2 = st.columns([3, 2])

    with col1:
        st.header("3D Building Visualization")
        # Display the 3D Cube
        cube_image = generate_3d_cube()
        st.image(cube_image, caption='3D Cube Visualization', use_column_width=True)

    with col2:
        # Your existing code to display project information and energy consumption...

if __name__ == "__main__":
    main()
