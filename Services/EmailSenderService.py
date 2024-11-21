from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl


def sendEmail(data):

    sender_email = "lunabistrobizzchatbot1@gmail.com"
    receiver_email = data["email"]
    password = "rkfs bzmp cayq rvnd"

    message = MIMEMultipart("alternative")
    message["Subject"] = data["titlu"]
    message["From"] = sender_email
    message["To"] = receiver_email

    part1 = MIMEText(data["text"], "plain")

    message.attach(part1)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
