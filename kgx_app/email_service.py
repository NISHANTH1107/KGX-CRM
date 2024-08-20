import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_email(pdf_filename):
    sender_email = "nagaroshan09@gmail.com"
    receiver_email = "nagaroshan09@gmail.com"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # SSL port for Gmail
    smtp_password = "awljxpnvolvrkzku"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "KGX Public Holiday Attendance Report"

    body = "Please find attached the attendance report for the upcoming public holiday."
    msg.attach(MIMEText(body, 'plain'))

    with open(pdf_filename, "rb") as attachment:
        part = MIMEApplication(attachment.read(), _subtype="pdf")
        part.add_header('Content-Disposition', 'attachment', filename=pdf_filename)
        msg.attach(part)

    server = None

    try:
       
        # Establish a secure session with Gmail's outgoing SMTP server using SMTP_SSL
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
        server.ehlo()
       
        
        # Login using your Gmail account
        server.login(sender_email, smtp_password)
        

        
        # Send email
        server.sendmail(sender_email, receiver_email, msg.as_string())
        

        
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        if server is not None:
            server.quit()

