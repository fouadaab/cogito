import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from helper.class_enumerators import EmailAttributes, ColumnNames, LibelleToStr, PathNames
from typing import Callable
import keyring
import pandas
import re
import os


cred = keyring.get_credential(
    EmailAttributes.NAMESPACE,
    EmailAttributes.ENTRY
)

class Email():
    """
    TODO: Add Docstring
    """
    def __init__(
        self,
        cwd: str,
    ):
        """
        TODO: Initialize class with name, id
        """
        self.cwd = cwd

    def check_condition(self, record: pandas.Series) -> Callable:
        """
        TODO: Add Docstring
        """
        self.record = record

        if self.record[ColumnNames.OVERDUE] >= 30:
            return self.send_email()
        else:
            return self.no_email()

    def regex_match(self, x: str) -> str:
        """
        TODO: Add docstring
        """
        if re.match(r'^Cotisations.*', x):
            return LibelleToStr.COTISATION + " " + self.record[ColumnNames.SAISON]
        elif re.match(r'[A-a+Z-z+è+ ]+Cotisations.*', x):
            return "la " + self.record[ColumnNames.LIBELLE].replace(LibelleToStr.TRANCHE, LibelleToStr.TRANCHE_DE).lower()
        elif re.match(r'.*article$', x):
            return LibelleToStr.ARTICLE
        
        raise ValueError(f"Unexpected value {x} in Column {ColumnNames.LIBELLE}")

    def conditional_complement(self, x: str) -> str:
        """
        TODO: Add docstring
        """
        complement = '\n'
    
        if self.regex_match(x) != LibelleToStr.ARTICLE:
            complement += "\nSi jamais vous deviez faire face à des difficultés financières, je vous remercie de bien vouloir prendre contact, en toute confidentialité, avec moi ou l'un des membres du comité et nous vous orienterons alors vers une association à même de vous aider financièrement.\n"
        
        return complement

    def get_message(self):
        message = f'''
        Bonjour, 

        Je me permets de vous contacter car le HBC Nyon est toujours en attente du paiement de la facture N° {self.record[ColumnNames.FACTURE]} d'un montant de CHF {self.record[ColumnNames.MONTANT_A_PAYER]}-- (dont vous trouverez une copie en pièce jointe) et relative à {self.regex_match(self.record[ColumnNames.LIBELLE])}. {self.conditional_complement(self.record[ColumnNames.LIBELLE])}
        Vous remerciant par avance de votre compréhension et de votre intervention et restant bien évidemment à votre disposition, je vous prie de bien vouloir agréer l'expression de mes sincères salutations. \n

        {EmailAttributes.SENDER} - {EmailAttributes.ROLE}
        '''
        return message

    def send_email(self) -> None:
        """
        TODO: Add Docstring
        """

        with smtplib.SMTP("smtp.outlook.com", 587) as s:  # Change smtp for Outlook
            s.starttls()
            s.login(cred.username, cred.password)

            msg = MIMEMultipart() # create a message

            # add in the actual person name to the message template
            message = self.get_message()

            # setup the parameters of the message
            msg['From']=cred.username
            msg['To']=self.record[ColumnNames.EMAIL]
            msg['Subject']=f"HBC Nyon - Retard de paiement {self.record[ColumnNames.MEMBRE]}"

            # Set up attachment folder
            attachment = os.path.abspath(
                os.path.join(
                    self.cwd,
                    PathNames.PDF_FOLDER,
                    f"Facture-{self.record[ColumnNames.MEMBRE]}-{self.record[ColumnNames.NUMERO]}.pdf",
                )
            )

            # add in the message body
            msg.attach(MIMEText(message, 'plain'))

            # attach pdf to email
            with open(attachment, "rb") as f:
                attach = MIMEApplication(f.read(),_subtype="pdf")
            attach.add_header('Content-Disposition', 'attachment', filename=attachment.split('/')[-1])
            msg.attach(attach)

            # send the message via the server set up earlier.
            s.send_message(msg)

            print(f"Reminder sent to {self.record[ColumnNames.MEMBRE]}")

        return None

    def no_email(self):
        print(
            f"No reminder needed for {self.record[ColumnNames.MEMBRE]} - Skipping"
        )