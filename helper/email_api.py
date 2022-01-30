import smtplib
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# pip install keyring
# pip install --upgrade --force-reinstall cffi
import keyring
from class_imports import EmailAttributes


cred = keyring.get_credential(
    EmailAttributes.NAMESPACE,
    EmailAttributes.ENTRY
)

class Email():
    """
    TODO: Add Docstring
    """

    def __init__(self):
        """
        TODO: Initialize class with name, id
        """
        self.send_email()

    def send_email(self, recipient: str = EmailAttributes.DEV_RECIPIENT) -> None:
        """
        TODO: Add Docstring
        """
        s = smtplib.SMTP("smtp.outlook.com", 587) # Change smtp for Outlook
        s.starttls()
        s.login(cred.username, cred.password)

        msg = MIMEMultipart()       # create a message

        # add in the actual person name to the message template
        message = f'''
            Dear {recipient}
            You did it!

            BR,
            FN.
        '''

        # setup the parameters of the message
        msg['From']=cred.username
        msg['To']=recipient
        msg['Subject']="Marketplace order Accepted!"

        # add in the message body
        msg.attach(MIMEText(message, 'plain'))

        # attach pdf to email
        with open(EmailAttributes.PATH_TO_PDF, "rb") as f:
            attach = MIMEApplication(f.read(),_subtype="pdf")
        attach.add_header('Content-Disposition', 'attachment', filename=EmailAttributes.PATH_TO_PDF.split('/')[-1])
        msg.attach(attach)

        # send the message via the server set up earlier.
        s.send_message(msg)

        # Terminate the SMTP session and close the connection
        s.quit()

        return None


if __name__ == "__main__":
    Email()