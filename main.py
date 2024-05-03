import smtplib
from email.message import EmailMessage
from loguru import logger

from settings import settings


def main():
    msg = EmailMessage()
    msg['Subject'] = 'Check out Bronx as a puppy!'
    msg['From'] = settings.smtp.user
    msg['To'] = settings.smtp.user

    msg.add_alternative("""
    <!DOCTYPE html>
    <html>
        <body>
            <h1 style="color:SlateGray;">This is an HTML Email!</h1>
        </body>
    </html>
    """, subtype='html')


    with smtplib.SMTP_SSL(settings.smtp.server, settings.smtp.port) as smtp:
        smtp.login(settings.smtp.user, settings.smtp.password.get_secret_value())
        smtp.send_message(msg)

if __name__ == '__main__':
    logger.info("Sending email...")
    try:
        main()
    except Exception as e:
        logger.exception(e)
        logger.error("Failed to send email")
    else:
        logger.info("Email sent successfully")
    