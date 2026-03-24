from datetime import datetime
from geopy.timezone import TimezoneFinder
import pytz


def check_gps(metadata):
    if metadata["gps_latitude"] and metadata["gps_longitude"]:
        return "GPS Present"
    else:
        return "GPS Missing"


def check_timestamp(metadata):
    if metadata["timestamp"] != "Not Available":
        return "Timestamp Present"
    else:
        return "Timestamp Missing"


def check_software(metadata):
    software = metadata.get("software", "").lower()

    editing_software = ["photoshop", "gimp", "lightroom", "snapseed", "canva"]

    for software_name in editing_software:
        if software_name in software:
            return f"Edited using {software}"

    if software == "not available":
        return "Software Tag Missing"

    return "No Editing Software Detected"


def check_timezone_consistency(metadata):
    try:
        if metadata["gps_latitude"] and metadata["gps_longitude"] and metadata["timestamp"] != "Not Available":
            tf = TimezoneFinder()
            timezone_str = tf.timezone_at(
                lat=metadata["gps_latitude"],
                lng=metadata["gps_longitude"]
            )

            if timezone_str is None:
                return "Timezone could not be determined"

            timezone = pytz.timezone(timezone_str)

            image_time = datetime.strptime(metadata["timestamp"], "%Y:%m:%d %H:%M:%S")
            localized_time = timezone.localize(image_time)

            return f"Timezone Match: {timezone_str}"

        else:
            return "Insufficient Data for Timezone Check"

    except Exception as e:
        return f"Timezone Check Error: {str(e)}"


def check_image_dimensions(metadata):
    width = metadata.get("image_width")
    height = metadata.get("image_height")

    if width and height:
        if width < 500 or height < 500:
            return "Low Resolution Image (Suspicious)"
        else:
            return "Resolution Normal"
    else:
        return "Image Dimensions Unknown"


def run_consistency_checks(metadata):
    """
    Main function that runs all checks
    """
    results = {
        "gps_check": check_gps(metadata),
        "timestamp_check": check_timestamp(metadata),
        "software_check": check_software(metadata),
        "timezone_check": check_timezone_consistency(metadata),
        "resolution_check": check_image_dimensions(metadata)
    }

    return results