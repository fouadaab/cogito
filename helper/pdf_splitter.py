from PyPDF2 import PdfFileWriter, PdfFileReader
from typing import Callable, List
import helper.class_enumerators as class_enumerators
from helper.firebase_config import Member
import pandas
import re
import os

class PdfWriter():
    """
    TODO: update not_found after inital DEV phase
    """
    not_found: List[int]

    def __init__(
        self,
        cwd: str,
        firebase: Callable,
        ids: pandas.Series,
        names: pandas.Series,
        invoice_ids: pandas.Series,
    ):
        self.cwd = cwd
        self.firebase = firebase
        self.file_name = os.path.abspath(
            os.path.join(
                self.cwd,
                class_enumerators.PathNames.DATA_FOLDER,
                f"{class_enumerators.PathNames.PDF_FILE}.pdf",
            )
        )
        self.ids = ids
        self.names = names
        self.invoice_ids = invoice_ids
        self.getPagebreakList()

    def getPagebreakList(self) -> None:

        not_found = list()
        pdf_file = PdfFileReader(self.file_name)
        num_pages = pdf_file.getNumPages()
        if num_pages != len(self.names):
            raise ValueError(f"{num_pages} pages found when passing list of {len(self.names)} members")

        for i, (id, name, invoice_id) in enumerate(zip(self.ids, self.names, self.invoice_ids)):
            output = PdfFileWriter()
            pageobj = pdf_file.getPage(i)
            output.addPage(pageobj)
            
            Text = pageobj.extractText()
            pattern = rf"(?:{name} \({id}\))"

            if re.findall(pattern, Text):
                with open(
                    os.path.join(
                        self.cwd,
                        class_enumerators.PathNames.OUTPUT_FOLDER,
                        class_enumerators.PathNames.PDF_FOLDER,
                        f"Facture-{name}-{id}.pdf"
                    ),
                    "wb") as outputStream:
                    output.write(outputStream)
            else:
                not_found.append(invoice_id)

                # INSERT INTO FIREBASE DB: INVOICE #
                _collection = self.firebase.collection(f'{class_enumerators.FireBase.SCHEMA_INVOICE}')
                _collection.document(f'{invoice_id}').set(
                    Member(
                        f'{id}',
                        f'{name}',
                    ).to_dict()
                )
        
        self.not_found = not_found

        return None
