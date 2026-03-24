import exifread
from PIL import Image
import hashlib


def get_decimal_from_dms(dms, ref):
    """
    Convert GPS coordinates from Degrees, Minutes, Seconds to Decimal format
    """
    degrees = float(dms[0].num) / float(dms[0].den)
    minutes = float(dms[1].num) / float(dms[1].den)
    seconds = float(dms[2].num) / float(dms[2].den)

    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)

    if ref in ['S', 'W']:
        decimal = -decimal

    return decimal


def extract_gps(tags):
    """
    Extract GPS Latitude and Longitude
    """
    gps_latitude = None
    gps_longitude = None

    try:
        if 'GPS GPSLatitude' in tags and 'GPS GPSLatitudeRef' in tags:
            lat = tags['GPS GPSLatitude'].values
            lat_ref = tags['GPS GPSLatitudeRef'].values
            gps_latitude = get_decimal_from_dms(lat, lat_ref)

        if 'GPS GPSLongitude' in tags and 'GPS GPSLongitudeRef' in tags:
            lon = tags['GPS GPSLongitude'].values
            lon_ref = tags['GPS GPSLongitudeRef'].values
            gps_longitude = get_decimal_from_dms(lon, lon_ref)

    except Exception as e:
        print("GPS Extraction Error:", e)

    return gps_latitude, gps_longitude


def generate_image_hash(image_path):
    """
    Generate SHA256 hash of image for duplicate detection
    """
    hasher = hashlib.sha256()
    with open(image_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()


def extract_metadata(image_path):
    """
    Main function to extract metadata
    """
    metadata = {}

    # Image hash
    metadata["image_hash"] = generate_image_hash(image_path)

    # Open image for EXIF
    with open(image_path, 'rb') as f:
        tags = exifread.process_file(f)

    # GPS
    gps_lat, gps_lon = extract_gps(tags)
    metadata["gps_latitude"] = gps_lat
    metadata["gps_longitude"] = gps_lon

    # Timestamp
    metadata["timestamp"] = str(tags.get("EXIF DateTimeOriginal", "Not Available"))

    # Camera Info
    metadata["camera_make"] = str(tags.get("Image Make", "Not Available"))
    metadata["camera_model"] = str(tags.get("Image Model", "Not Available"))

    # Orientation
    metadata["orientation"] = str(tags.get("Image Orientation", "Not Available"))

    # Software (important for detecting editing)
    metadata["software"] = str(tags.get("Image Software", "Not Available"))

    # Image size
    image = Image.open(image_path)
    metadata["image_width"], metadata["image_height"] = image.size

    return metadata