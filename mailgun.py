import requests
from receipt_statments import PdfStatement
import os
from dotenv import load_dotenv
from framework_utils import config

root_path = config.get_root_path()
logger = config.configure_logging(log_file_name="mailgun.log", logger_name=__name__)


wifi_credentials_statement = PdfStatement().wifi_credentials(username="Pero PEric 123", password="ma nema")


class Mailgun:
    def __init__(self, sender=(), domain=None):
        dotenv_path = (root_path + ".env")
        load_dotenv(dotenv_path=dotenv_path)
        self.domain = domain or os.getenv("mailgun_domain")
        self.key = os.getenv("mailgun_api_key")
        self.sender_name, self.sender_username = sender

    def send_mail(self, recipient_email, subject, attachment_bytes, message=None, html=None):
        url = f"https://api.mailgun.net/v3/{self.domain}/messages"

        data = {"from": f"{self.sender_name} <{self.sender_username}@{self.domain}>",
                "to": recipient_email,
                "subject": subject,
                **({"text": message} if message is not None else {"html": html}),
                'h:Reply-To': 'reply_to_email@example.com'
                }

        files = [("attachment", ("document.pdf", attachment_bytes))]

        response = requests.post(
            url=url,
            auth=("api", self.key),
            files=files,
            data=data
        )

        if response.status_code == 200:
            logger.info("Email sent successfully!")
        else:
            logger.warning(f"Email could not be sent. Status code: {response.status_code}")
            logger.error(response.text)


if __name__ == "__main__":
    my_mailgun = Mailgun(sender=("Sender Ime", "Senderusername"))
    my_mailgun.send_mail(recipient_email="dpustahija@gmail.com", subject="naslov", message="porukica", attachment_bytes=wifi_credentials_statement)
