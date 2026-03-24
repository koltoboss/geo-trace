import requests


OVERPASS_URL = "http://overpass-api.de/api/interpreter"


def query_overpass(query):
    """
    Send query to Overpass API
    """
    try:
        response = requests.get(OVERPASS_URL, params={'data': query})
        data = response.json()
        return data['elements']
    except Exception as e:
        return {"error": str(e)}


def get_nearby_roads(lat, lon):
    """
    Get nearby roads
    """
    query = f"""
    [out:json];
    way
      (around:500,{lat},{lon})
      ["highway"];
    out tags;
    """

    elements = query_overpass(query)

    roads = []
    for el in elements:
        if 'tags' in el:
            roads.append(el['tags'].get('name', 'Unnamed Road'))

    return list(set(roads))[:10]


def get_nearby_buildings(lat, lon):
    """
    Get nearby buildings
    """
    query = f"""
    [out:json];
    way
      (around:300,{lat},{lon})
      ["building"];
    out tags;
    """

    elements = query_overpass(query)

    buildings = []
    for el in elements:
        if 'tags' in el:
            buildings.append(el['tags'].get('name', 'Unnamed Building'))

    return list(set(buildings))[:10]


def get_nearby_amenities(lat, lon):
    """
    Get nearby amenities like hospitals, cafes, banks, etc.
    """
    query = f"""
    [out:json];
    node
      (around:500,{lat},{lon})
      ["amenity"];
    out tags;
    """

    elements = query_overpass(query)

    amenities = []
    for el in elements:
        if 'tags' in el:
            amenities.append({
                "name": el['tags'].get('name', 'Unknown'),
                "type": el['tags'].get('amenity', 'Unknown')
            })

    return amenities[:10]


def get_landuse_info(lat, lon):
    """
    Determine land use type (residential, commercial, industrial, etc.)
    """
    query = f"""
    [out:json];
    way
      (around:500,{lat},{lon})
      ["landuse"];
    out tags;
    """

    elements = query_overpass(query)

    landuse = []
    for el in elements:
        if 'tags' in el:
            landuse.append(el['tags'].get('landuse', 'Unknown'))

    return list(set(landuse))


def gather_osm_intelligence(lat, lon):
    """
    Main function to gather all OSM intelligence
    """
    osm_data = {
        "nearby_roads": get_nearby_roads(lat, lon),
        "nearby_buildings": get_nearby_buildings(lat, lon),
        "nearby_amenities": get_nearby_amenities(lat, lon),
        "landuse": get_landuse_info(lat, lon)
    }

    return osm_data