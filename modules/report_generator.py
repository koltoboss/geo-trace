from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import os
from datetime import datetime


def create_table(data_dict):
    """
    Convert dictionary to table format
    """
    table_data = [["Field", "Value"]]

    for key, value in data_dict.items():
        table_data.append([str(key), str(value)])

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
    ]))

    return table


def generate_pdf_report(image_path, metadata, consistency_results, score, label,
                        location_info=None, osm_data=None, map_path=None):
    """
    Generate OSINT Investigation PDF Report
    """

    if not os.path.exists("reports"):
        os.makedirs("reports")

    report_path = f"reports/GeoTrace_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(report_path, pagesize=A4)

    elements = []

    # Title
    title = Paragraph("GeoTrace OSINT Investigation Report", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 20))

    # Case Info
    elements.append(Paragraph("Case Information", styles['Heading2']))
    case_info = {
        "Report Generated On": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Investigative Tool": "GeoTrace OSINT Framework",
        "Analysis Type": "Geospatial OSINT Profiling"
    }
    elements.append(create_table(case_info))
    elements.append(Spacer(1, 20))

    # Image
    elements.append(Paragraph("Analyzed Image", styles['Heading2']))
    elements.append(Image(image_path, width=400, height=300))
    elements.append(Spacer(1, 20))

    # Metadata
    elements.append(Paragraph("Extracted Metadata", styles['Heading2']))
    elements.append(create_table(metadata))
    elements.append(Spacer(1, 20))

    # Location Info
    if location_info:
        elements.append(Paragraph("Location Information", styles['Heading2']))
        elements.append(create_table(location_info))
        elements.append(Spacer(1, 20))

    # OSM Intelligence
    if osm_data:
        elements.append(Paragraph("Open Source Map Intelligence", styles['Heading2']))
        elements.append(create_table(osm_data))
        elements.append(Spacer(1, 20))

    # Consistency Results
    elements.append(Paragraph("Consistency Analysis", styles['Heading2']))
    elements.append(create_table(consistency_results))
    elements.append(Spacer(1, 20))

    # Credibility Score
    elements.append(Paragraph("Credibility Assessment", styles['Heading2']))
    credibility_data = {
        "Credibility Score": score,
        "Credibility Level": label
    }
    elements.append(create_table(credibility_data))
    elements.append(Spacer(1, 20))

    # Final Conclusion
    elements.append(Paragraph("Final Conclusion", styles['Heading2']))

    if label == "High Credibility":
        conclusion_text = "The image metadata and geospatial information are consistent. The image is likely authentic and location claim appears credible."
    elif label == "Medium Credibility":
        conclusion_text = "Some inconsistencies were detected. The image location claim requires further verification."
    else:
        conclusion_text = "Multiple inconsistencies detected. The image location claim is likely not credible."

    elements.append(Paragraph(conclusion_text, styles['Normal']))

    # Build PDF
    doc.build(elements)

    return report_path