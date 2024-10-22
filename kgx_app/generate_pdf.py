from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import datetime

def generate_pdf(data):
    filename = f"Work_on_holiday{datetime.date.today()}.pdf"
    document = SimpleDocTemplate(filename, pagesize=letter)
    
    elements = []

    # Title
    title = f"Work on holidays list"
    date_str = f"Date: {datetime.date.today()}"
    title_data = [[title], [date_str]]
    title_table = Table(title_data)
    title_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12)
    ]))
    elements.append(title_table)
    
    # Table data
    table_data = [['Name', 'Department / year', 'Purpose', 'Entry Time', 'Exit Time']]
    
    styles = getSampleStyleSheet()
    for entry in data:
        row = [
            entry.name,
            entry.department,
            Paragraph(entry.purpose, styles['Normal']),  # Wrap text in 'Purpose' column
            entry.entry_time,
            entry.exit_time
        ]
        table_data.append(row)
    
    # Create table
    attendance_table = Table(table_data, colWidths=[100, 100, 200, 100, 100])  # Adjust column widths as needed
    attendance_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(attendance_table)
    
    # Build PDF
    document.build(elements)
    
    return filename
