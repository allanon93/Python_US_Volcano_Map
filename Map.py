# US Volcano Map
# Cyris Zeiders
# 03/23/2023

# --- MODULES ---
# folium: Makes it easy to vizualize data;
# pandas: Software library used to manipulate and analyze data;
import folium
import pandas

# --- Creating Volcanoes Data ---
# Create variable "volcanoes_data" to hold Volcanoes.csv;
# Pull CSV column information and transpose into variables;

volcanoes_data = pandas.read_csv("Data Sources\Volcanoes.csv")
volcanoes_latitude = list(volcanoes_data["LAT"])
volcanoes_longitude = list(volcanoes_data["LON"])
volcanoes_name = list(volcanoes_data["NAME"])
volcanoes_elevation = list(volcanoes_data["ELEV"])
volcanoes_location = list(volcanoes_data["LOCATION"])
volcanoes_type = list(volcanoes_data["TYPE"])

# --- Functions ---
# Create function to define marker color according to elevation;
def marker_color_coder(elevation):
    if elevation < 1500:
        return "green"
    elif 1500 <= elevation < 3000:
        return "orange"
    else: 
        return "red"

# --- Creating Map ---
# Create "map" variable with start location, zoom, and type of tile;
map = folium.Map(location = [40.254442393789965, -96.94174713363157], zoom_start = 5, tiles = "OpenStreetMap")

# --- Map Border ---
# Create folium Feature Group "fg_population" to hold Population feature;
# Adding child containing folium.GeoJson("json source") to Feature Group "fg_map";
    # Added style_function lambda for coloration according to population of 2005;

fg_population = folium.FeatureGroup(name = "World Population")

fg_population.add_child(folium.GeoJson(data=open("Data Sources\world.json", "r", encoding="utf-8-sig").read(),
    style_function=lambda x: {'color': 'black', 'fillOpacity': .2, 'fillColor': 'green' 
        if x['properties']['POP2005'] < 10000000 else 'orange' if 10000000 <= x['properties']['POP2005'] < 50000000 
        else 'red'}))

# --- Marker Creation ---
# Create folium Feature Group "fg_markers" to hold Markers;
# Creation of for loop that complies information from various volcanoes_variables;
    # Create "html" variable to hold HTML code design for pop up;
    # Reformat "v_loc" from (US - "") to ("" - US);
    # Else return as CSV suggests, but titlized; 
    # Build "iframe" variable containing IFrame callable with previous "html" variable and assigned inputs;
    # Add child to map that creates CircleMarker with set parameters;

fg_markers = folium.FeatureGroup(name = "US Volcanoes")

for v_la, v_lo, v_name, v_el, v_loc, v_type, in zip(volcanoes_latitude, volcanoes_longitude,
    volcanoes_name, volcanoes_elevation, volcanoes_location, volcanoes_type):

    html = """<h3>%s Information</h3>
        <h4>Height:</h4> %sm
        <h4>Type:</h4> <a href="https://www.google.com/search?q=%s+Volcano+Type" target="_blank">%s</a>
        <h4>Location:</h4> %s
        <a href="https://www.google.com/search?q=%s+%s" target="_blank">
            <h4>Click here for related search results.</h4></a>
        """

    if v_loc[:3] == "US-":
        v_loc_reformatted = " - ".join([v_loc[3:].title(), v_loc[:2].upper()])
    else:
        v_loc_reformatted = v_loc.title()     

    iframe = folium.IFrame(html = html % (v_name.title(), str(v_el), v_type.title(), v_type.title(),
        v_loc_reformatted, v_name + " Volcano", v_loc_reformatted), width=200, height=250)

    fg_markers.add_child(folium.CircleMarker(location=[v_la, v_lo], radius=7, popup=folium.Popup(iframe), 
        tooltip=v_name, color = "black", fillColor=marker_color_coder(v_el), fillOpacity=.7))

# --- Children and Layer Control ---
# Add child "fg_markers" to "map";
# Add child "fg_population" to "map";
# Add child Layer Control to turn on/off Feature Groups/Layers;
map.add_child(fg_population)
map.add_child(fg_markers)
map.add_child(folium.LayerControl())


# --- Save and HTML Creation ---
# Save map as HTML document;
map.save("US Volcano Map.html")