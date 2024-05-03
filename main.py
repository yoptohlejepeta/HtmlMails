import smtplib
from email.message import EmailMessage
from loguru import logger
from jinja2 import Environment, FileSystemLoader

from settings import settings


def main():
    try:
        msg = EmailMessage()
        msg["Subject"] = "Hello, this is COOL email!"
        msg["From"] = settings.smtp.user
        msg["To"] = settings.smtp.user

        env = Environment(loader=FileSystemLoader("."))
        template = env.get_template("index.html")
        
        with open('./images/logo2.svg', 'r') as file:
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
        raise e


if __name__ == "__main__":
    logger.info("Sending email...")
    try:
        main()
    except Exception as e:
        logger.error("Failed to send email")
    else:
        logger.info("Email sent successfully")
