import streamlit as st
import requests
import json
import pandas as pd
import pydeck as pdk


def get_astronauts():
    url = "http://api.open-notify.org/astros.json"
    
    try:
        response = requests.get(url)
        data = json.loads(response.text)
    except:
        st.exception("There has been an error with retrieving the information")

    # Get names of astronauts
    names = []
    for astronaut in data["people"]:
        names.append(astronaut["name"])

    # Get amount of people in Space
    total_amount = len(data["people"])

    return names,total_amount

def get_current_iss_location():
    url = "http://api.open-notify.org/iss-now.json"

    try:
        response = requests.get(url)
        data = json.loads(response.text)
        longitude = float(data["iss_position"]["longitude"])
        latitude = float(data["iss_position"]["latitude"])
    except:
        st.exception("There has been an error with retrieving the information")


    return longitude,latitude

    

# Set title and description for page
st.title('Astronaut information')
st.caption("Below you can see all the astronauts who are currently in space and also the amount of astronauts in total, so you don't need to count them")

st.image("https://i.pinimg.com/originals/9a/7c/12/9a7c12b1e9488b9122883a5a504df8bc.gif")

# Get names of all astronauts & totalNumber
names_of_astronauts,total_astronauts = get_astronauts()
st.header("Astronauts currently in space:")
names_of_astronauts
st.write(f"Total number of astronauts in space: {total_astronauts}")


longitude,latitude = get_current_iss_location()

# Display longitude and latitude
st.header(f"The following map shows the current location of the ISS") 
st.caption(f"long:{longitude}    |    lat: {latitude})")

# Create a DataFrame
data = pd.DataFrame({
    'lat': [latitude],
    'lon': [longitude]
})


# Define the layer for the map
layer = pdk.Layer(
    'ScatterplotLayer',
    data,
    get_position='[lon, lat]',
    get_color='[231, 13, 13, 160]',
    get_radius=100000,  # Radius in meters
)

# Define the view state
view_state = pdk.ViewState(
    latitude=latitude,
    longitude=longitude,
    zoom=1,
    pitch=0,
)

# Render the map
import time
import streamlit as st

with st.spinner('Wait for it...'):
    time.sleep(5)
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
st.success('Done!')

