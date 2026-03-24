def score_gps(consistency_results):
    if consistency_results["gps_check"] == "GPS Present":
        return 2
    else:
        return -2


def score_timestamp(consistency_results):
    if consistency_results["timestamp_check"] == "Timestamp Present":
        return 1
    else:
        return -1


def score_software(consistency_results):
    result = consistency_results["software_check"].lower()

    if "edited using" in result:
        return -2
    elif "no editing software detected" in result:
        return 1
    else:
        return 0


def score_timezone(consistency_results):
    result = consistency_results["timezone_check"]

    if "match" in result.lower():
        return 2
    elif "insufficient" in result.lower():
        return 0
    else:
        return -1


def score_resolution(consistency_results):
    if "suspicious" in consistency_results["resolution_check"].lower():
        return -1
    else:
        return 1


def score_osm(osm_data):
    """
    Score based on environment richness
    More landmarks/amenities = more believable location context
    """
    score = 0

    if len(osm_data.get("nearby_amenities", [])) > 3:
        score += 2
    elif len(osm_data.get("nearby_amenities", [])) > 0:
        score += 1

    if len(osm_data.get("nearby_roads", [])) > 0:
        score += 1

    if len(osm_data.get("landuse", [])) > 0:
        score += 1

    return score


def calculate_credibility_score(metadata, consistency_results, osm_data=None):
    """
    Main scoring function
    """
    total_score = 0

    total_score += score_gps(consistency_results)
    total_score += score_timestamp(consistency_results)
    total_score += score_software(consistency_results)
    total_score += score_timezone(consistency_results)
    total_score += score_resolution(consistency_results)

    if osm_data:
        total_score += score_osm(osm_data)

    # Classification
    if total_score >= 6:
        credibility = "High Credibility"
    elif total_score >= 3:
        credibility = "Medium Credibility"
    else:
        credibility = "Low Credibility"

    return total_score, credibility