# app/utils/email.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from app.core.config import settings  # Assuming settings come from pydantic BaseSettings
import logging


def send_email(member_name: str, from_email: str, to_email: str, subject: str, body: str, is_body_html: bool = True):
    try:
        # Get sender name and default email if not provided
        name = member_name or settings.APP_ADMIN
        from_email = settings.APP_FROM_EMAIL

        # Compose the email
        msg = MIMEMultipart()
        msg['From'] = formataddr((name, from_email))
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach HTML or plain body
        mime_type = 'html' if is_body_html else 'plain'
        msg.attach(MIMEText(body, mime_type))

        # SMTP configuration
        smtp_host = settings.APP_SMTP_HOST
        smtp_port = int(settings.APP_SMTP_PORT or 587)
        smtp_password = settings.APP_SMTP_PWD

        # Send the email
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(from_email, smtp_password)
            server.send_message(msg)

        logging.info(f"Email sent to {to_email}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")