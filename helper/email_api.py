import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from helper.class_enumerators import EmailAttributes, ColumnNames, LibelleToStr, PathNames, FireBase
from helper.firebase_config import Member
from typing import Callable, Dict, Any
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
        firebase: Callable,
    ):
        """
        TODO: Initialize class with name, id
        """
        self.cwd = cwd
        self.firebase = firebase

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

    def get_message(self) -> str:
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

            self.write_to_db(schema=FireBase.SCHEMA_SENT)

    def no_email(self):
        print(
            f"No reminder needed for {self.record[ColumnNames.MEMBRE]} - Skipping"
        )

    def collect_from_db(self, schema: str = FireBase.SCHEMA_SENT) -> Dict[int, Dict[str, Any]]:
        """
        TODO: Add Docstring
        """
        # COLLECT FROM FIREBASE DB #
        # Note: Use of CollectionRef stream() is prefered to get()
        _collection = self.firebase.collection(f'{schema}')
        past_reminders = dict() 
        docs = _collection.where(f'{FireBase.SENT_SAISON}', u'==', f'{FireBase.SAISON_21_22}').stream()
        for doc in docs:
            past_reminders[int(doc.id)] = doc.to_dict()
        
        return past_reminders

    def write_to_db(self, schema: str) -> None:
        """
        TODO: Add Docstring
        """
        # INSERT INTO FIREBASE DB: SENT #
        _collection = self.firebase.collection(f'{schema}')
        _collection.document(f'{self.record[ColumnNames.FACTURE]}').set(
            Member(
                f'{self.record[ColumnNames.NUMERO]}',
                f'{self.record[ColumnNames.MEMBRE]}',
                f'{self.record[ColumnNames.SAISON]}',
            ).to_dict()
        )