"""Main module to send email with HTML template and logo image."""

import smtplib
from email.message import EmailMessage
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from loguru import logger

from settings import settings


def main() -> None:
    """Send email with HTML template and logo image.

    Raises
    ------
        e: Exception raised when sending email fails.

    """
    try:
        msg = EmailMessage()
        msg["Subject"] = "Hello, this is COOL email!"
        msg["From"] = settings.smtp.user
        msg["To"] = settings.smtp.user

        env = Environment(loader=FileSystemLoader("."), autoescape=True)
        template = env.get_template("index.html")

        with Path("./images/logo1.svg").open("rb") as file:
            logo = file.read()

        variables = {
            "to_name": "John Doe",
            "subject_info": "This is a test email",
            "body": "This is a test email body.",
            "phone": "+1234567890",
            "email": settings.smtp.user,
            "logo": logo,
        }

        html = template.render(variables)

        msg.add_alternative(html, subtype="html")

        with smtplib.SMTP_SSL(settings.smtp.server, settings.smtp.port) as smtp:
            smtp.login(settings.smtp.user, settings.smtp.password.get_secret_value())
            smtp.send_message(msg)
    except Exception as e:
        logger.exception(e)
        raise


if __name__ == "__main__":
    logger.info("Sending email...")
    try:
        main()
    except Exception:
        logger.error("Failed to send email")
    else:
        logger.info("Email sent successfully")
