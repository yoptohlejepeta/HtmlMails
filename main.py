import smtplib
from email.message import EmailMessage
from email.mime.image import MIMEImage
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

        variables = {
            "to_name": "John Doe",
            "subject_info": "This is a test email",
            "body": "This is a test email body.",
            "phone": "+1234567890",
            "email": settings.smtp.user,
        }

        html = template.render(variables)

        msg.add_alternative(html, subtype="html")
        
        # with open('./images/ujep_logo.png', 'rb') as file:
        #     img_data = file.read()

        # img = MIMEImage(img_data)
        # img.add_header('Content-ID', '<logo_cid>')
        # msg.attach(img)

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
