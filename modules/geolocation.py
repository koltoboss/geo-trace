from geopy.geocoders import Nominatim
import folium
import requests
import os

geolocator = Nominatim(user_agent="geotrace_osint")


def get_location_info(latitude, longitude):
    """
    Reverse geocoding to get address details
    """
    try:
        location = geolocator.reverse((latitude, longitude), language='en')
        address = location.raw.get('address', {})

        location_info = {
            "full_address": location.address,
            "city": address.get('city', ''),
            "state": address.get('state', ''),
            "country": address.get('country', ''),
            "postcode": address.get('postcode', '')
        }

        return location_info

    except Exception as e:
        return {"error": str(e)}


def generate_map(latitude, longitude):
    """
    Generate folium map and save as HTML
    """
    map_obj = folium.Map(location=[latitude, longitude], zoom_start=15)

    folium.Marker(
        [latitude, longitude],
        tooltip="Image Location",
        popup="Extracted GPS Location",
        icon=folium.Icon(color="red")
    ).add_to(map_obj)

    # Save map
    if not os.path.exists("maps"):
        os.makedirs("maps")

    map_path = "maps/location_map.html"
    map_obj.save(map_path)

    return map_path


def get_nearby_landmarks(latitude, longitude):
    """
    Fetch nearby landmarks using OpenStreetMap Overpass API
    """
    overpass_url = "http://overpass-api.de/api/interpreter"

    query = f"""
    [out:json];
    node
      (around:500,{latitude},{longitude})
      ["amenity"];
    out;
    """

    try:
        response = requests.get(overpass_url, params={'data': query})
        data = response.json()

        landmarks = []

        for element in data['elements']:
            name = element['tags'].get('name', 'Unknown')
            amenity = element['tags'].get('amenity', 'Unknown')

            landmarks.append({
                "name": name,
                "type": amenity
            })

        return landmarks[:10]  # return top 10 nearby places

    except Exception as e:
        return {"error": str(e)}