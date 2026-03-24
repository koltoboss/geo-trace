import streamlit as st
from PIL import Image
import os

# Create required directories
for folder in ["uploads", "reports", "maps"]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Import project modules
from modules.metadata_extractor import extract_metadata
from modules.geolocation import get_location_info, generate_map
from modules.osm_intelligence import gather_osm_intelligence
from modules.consistency_checker import run_consistency_checks
from modules.scoring_engine import calculate_credibility_score
from modules.report_generator import generate_pdf_report

st.set_page_config(page_title="GeoTrace OSINT", layout="wide")

st.title("GeoTrace: Geospatial OSINT Profiling Framework")
st.write("Upload an image to perform geospatial OSINT analysis and location verification.")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Save uploaded file
    upload_path = os.path.join("uploads", uploaded_file.name)
    with open(upload_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Display image
    image = Image.open(upload_path)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Metadata Extraction
    st.subheader("Metadata Extraction")
    metadata = extract_metadata(upload_path)
    st.json(metadata)

    # Initialize variables to avoid errors
    location_info = {}
    osm_data = {}
    map_file = None

    # Geolocation Mapping
    if metadata.get("gps_latitude") and metadata.get("gps_longitude"):
        st.subheader("Geolocation Mapping")
        location_info = get_location_info(metadata["gps_latitude"], metadata["gps_longitude"])
        st.write(location_info)

        map_file = generate_map(metadata["gps_latitude"], metadata["gps_longitude"])
        with open(map_file, 'r', encoding='utf-8') as f:
            map_html = f.read()
        st.components.v1.html(map_html, height=500)

        # OSM Intelligence
        st.subheader("Open-Source Map Intelligence (OSM)")
        osm_data = gather_osm_intelligence(metadata["gps_latitude"], metadata["gps_longitude"])
        st.write(osm_data)

    else:
        st.info("GPS coordinates not found in metadata; skipping geolocation and OSM intelligence.")

    # Consistency Analysis
    st.subheader("Consistency Analysis")
    consistency_results = run_consistency_checks(metadata)
    st.write(consistency_results)

    # Credibility Score
    st.subheader("Credibility Score")
    score, label = calculate_credibility_score(metadata, consistency_results, osm_data)
    st.write(f"Score: {score}")
    st.write(f"Credibility Level: {label}")

    # Generate Report
    st.subheader("Generate Investigation Report")
    if st.button("Generate PDF Report"):
        report_path = generate_pdf_report(
            upload_path,
            metadata,
            consistency_results,
            score,
            label,
            location_info,
            osm_data,
            map_file
        )

        with open(report_path, "rb") as f:
            st.download_button("Download Report", f, file_name="GeoTrace_Report.pdf")
