from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from django.utils import timezone
from .models import Wifi
import os
from django.conf import settings
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image as ReportlabImage

def generate_wifi_report():
    # Get today's date
    today = timezone.now().date()
    entries = Wifi.objects.filter(submitted_at__date=today)

    # Create a PDF file if there are entries
    if entries.exists():
        # Define the output directory for the report
        report_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
        os.makedirs(report_dir, exist_ok=True)  # Create directory if it doesn't exist

        # Define the PDF filename
        pdf_filename = os.path.join(report_dir, f'wifi_report_{today}.pdf')

        # Create a PDF document
        pdf = SimpleDocTemplate(pdf_filename, pagesize=letter)
        elements = []

        # Prepare data for the table
        data = [['Roll No', 'MAC Address', 'Submitted At', 'Screenshot']]
        
        for entry in entries:
            # Prepare the image path
            img_path = entry.screenshot.path if entry.screenshot else None
            
            # Check if the image file exists
            if img_path and os.path.isfile(img_path):  # Ensure the file exists
                img = ReportlabImage(img_path, width=1.5 * inch, height=1.5 * inch)  # Resize image
                img.hAlign = 'CENTER'  # Center the image in the cell
                data.append([
                    entry.roll_no.roll_no,
                    entry.mac_address,
                    entry.submitted_at.strftime('%Y-%m-%d %H:%M:%S'),
                    img  # Embed the image directly
                ])
            else:
                data.append([
                    entry.roll_no.roll_no,
                    entry.mac_address,
                    entry.submitted_at.strftime('%Y-%m-%d %H:%M:%S'),
                    "No Screenshot"  # Placeholder for no screenshot
                ])

        # Create a Table
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Add the table to the elements
        elements.append(table)

        # Build the PDF
        pdf.build(elements)

        print(f"PDF report generated: {pdf_filename}")
        return pdf_filename
    else:
        print("No entries for today to generate a report.")
        return None
