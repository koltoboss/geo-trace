# geo-trace
GeoTrace: A Geospatial OSINT Profiling and Location Verification Framework
Project Overview

GeoTrace is a rule-based Open Source Intelligence (OSINT) framework developed in Python that performs geospatial profiling and location verification of digital images using publicly available data sources.

The system extracts metadata from images, performs geolocation analysis, gathers environmental intelligence from OpenStreetMap, conducts consistency checks, and generates a credibility score along with an automated investigation report.

This project demonstrates the application of OSINT, GEOINT, and Digital Forensics techniques in a structured investigation framework.

Features
Extract EXIF metadata from images
Extract GPS coordinates and timestamp
Reverse geocoding (GPS → City, Country)
Map visualization using Folium
OpenStreetMap intelligence (roads, buildings, amenities, land use)
Metadata consistency and forensic checks
Rule-based credibility scoring engine
Automated PDF investigation report generation
Streamlit-based user interface
Technology Stack
Category	Tools Used
Programming Language	Python
UI Framework	Streamlit
Image Processing	Pillow
Metadata Extraction	exifread
Geolocation	geopy
Map Visualization	folium
OSINT Data Source	OpenStreetMap
Timezone Analysis	timezonefinder, pytz
Hashing	hashlib
Report Generation	reportlab
Project Structure
GeoTrace/
│
├── app.py
├── modules/
│   ├── metadata_extractor.py
│   ├── geolocation.py
│   ├── osm_intelligence.py
│   ├── consistency_checker.py
│   ├── scoring_engine.py
│   └── report_generator.py
│
├── uploads/
├── reports/
├── maps/
├── requirements.txt
└── README.md
System Workflow
User Upload Image
        ↓
Metadata Extraction
        ↓
GPS Coordinate Extraction
        ↓
Reverse Geocoding
        ↓
OpenStreetMap Intelligence Collection
        ↓
Consistency & Forensic Checks
        ↓
Rule-Based Credibility Scoring
        ↓
Map Visualization
        ↓
Automated PDF Investigation Report
Credibility Scoring Model

The system uses a rule-based scoring mechanism:

Condition	Score
GPS metadata present	+2
Timestamp present	+1
No editing software detected	+1
Timezone matches GPS location	+2
High resolution image	+1
OSM environmental data available	+2
Metadata missing	-2
Editing software detected	-2
Credibility Levels
Score Range	Credibility
6 and above	High Credibility
3 – 5	Medium Credibility
0 – 2	Low Credibility
Below 0	Very Low Credibility
How to Run the Project Locally
1. Install Dependencies

Open terminal in project folder and run:

pip install -r requirements.txt
2. Run the Application
streamlit run app.py

The application will open in your browser at:

http://localhost:8501
Test Dataset

The system was tested using:

Original images with GPS metadata
Images with stripped metadata (e.g., social media images)
Screenshots
Edited images

These test cases were used to evaluate the credibility scoring system.

Output Generated

The system generates an automated OSINT Investigation Report containing:

Case Information
Image Evidence
Extracted Metadata
Location Information
Open-Source Map Intelligence
Consistency Analysis
Credibility Score
Final Investigation Conclusion
Applications
Digital Forensics
OSINT Investigations
Cybercrime Investigations
Journalism Verification
Location Verification of Images
Threat Intelligence
Future Enhancements
Sun position analysis for time verification
Weather verification using historical weather APIs
Multi-image case analysis
Facial recognition for suspect identification
Web-based dashboard deployment
Integration with OSINT tools

OSINT  Project


This project is developed for academic and educational purposes.
