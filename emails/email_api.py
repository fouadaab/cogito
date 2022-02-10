import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from enums.class_enumerators import EmailAttributes, ColumnNames, LibelleToStr, PathNames, FireBase, OverdueInvoice
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

    def __init__(
        self,
        cwd: str,
        firebase: Callable,
    ):
        """
        Args:
            cwd (str): current working directory's location (full path)
            firebase (class instance / Callable): Firebase DB client
        """
        self.cwd = cwd
        self.firebase = firebase

    def check_condition(self, record: pandas.Series) -> Callable:
        """
        Condition to check whether to send an email or skip to next client
        Depends on "OVERDUE" attribute in the input variable
        Args:
            record (pandas.Series): Input row containing current client's data
        Returns:
            [Callable]: Method send_email() if invoice is overdue, otherwise no_email() 
        """
        self.record = record
        if self.record[ColumnNames.OVERDUE] > OverdueInvoice.LIMIT:
            return self.send_email()
        else:
            return self.no_email()

    def regex_match(self, x: str) -> str:
        """
        Column LIBELLE in client's data defines the choice of words to include in the message
            - If LIBELLE is a yearly membership/subscription: return "la cotisation annuelle {year_of_season}"
            - If LIBELLE is a partial membership/subscription: return "la {N-ème} tranche de cotisations {year_of_season}"
            - If LIBELLE is an item invoice: return "votre achat"
        Args:
            x (str): LIBELLE attribute of input row containing current client's data
        Returns:
            [str]: piece of sentence conditioned by the value of attribute self.record[ColumnNames.LIBELLE]
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
        Place an additional message in the body of the email depending on the LIBELLE
            - If the nature of the invoice does NOT refer to a purchase (item): return the complementary body text
            - Otherwise: return a line break
        Args:
            x (str): LIBELLE attribute of input row containing current client's data
        Returns:
            [str]: Additional piece of sentence to attach to the email
        """
        complement = '\n'
        if self.regex_match(x) != LibelleToStr.ARTICLE:
            complement += "\nSi jamais vous deviez faire face à des difficultés financières, je vous remercie de bien vouloir prendre contact, en toute confidentialité, avec moi ou l'un des membres du comité et nous vous orienterons alors vers une association à même de vous aider financièrement.\n"
        return complement

    def get_message(self) -> str:
        """
        Main body of the email, fill with client data stored in Email class object self.record
        Args:
            [None]
        Returns:
            [None]
        """
        message = f'''
        Bonjour, 

        Je me permets de vous contacter car le HBC Nyon est toujours en attente du paiement de la facture N° {self.record[ColumnNames.FACTURE]} d'un montant de CHF {self.record[ColumnNames.MONTANT_A_PAYER]}-- (dont vous trouverez une copie en pièce jointe) et relative à {self.regex_match(self.record[ColumnNames.LIBELLE])}. {self.conditional_complement(self.record[ColumnNames.LIBELLE])}
        Vous remerciant par avance de votre compréhension et de votre intervention et restant bien évidemment à votre disposition, je vous prie de bien vouloir agréer l'expression de mes sincères salutations. \n

        {EmailAttributes.SENDER} - {EmailAttributes.ROLE}'''
        return message

    def send_email(self) -> None:
        """
        Send an email to the current client (data stored in Email class object self.record)
        Get the attachment - associated PDF invoice for the current client -
        Write into Firebase DB with timestamp to keep track, with invoice N° as primary key
        Args:
            [None]
        Returns:
            [None]
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
                    PathNames.OUTPUT_FOLDER,
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

            self.firebase.insert_db(
                FireBase.SCHEMA_SENT,
                self.record[ColumnNames.FACTURE],
                self.record[ColumnNames.NUMERO],
                self.record[ColumnNames.MEMBRE],
            )

            print(f"Reminder sent to {self.record[ColumnNames.MEMBRE]}: Invoice N°{self.record[ColumnNames.FACTURE]}")

    def no_email(self):
        print(
            f"No reminder needed for {self.record[ColumnNames.MEMBRE]} - Skipping"
        )