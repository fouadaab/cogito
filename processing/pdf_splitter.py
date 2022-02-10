from PyPDF2 import PdfFileWriter, PdfFileReader
from typing import Callable, List
import enums.class_enumerators as class_enumerators
import pandas
import re
import os

class PdfWriter():
    not_found: List[int]

    def __init__(
        self,
        cwd: str,
        firebase: Callable,
        ids: pandas.Series,
        names: pandas.Series,
        invoice_ids: pandas.Series,
    ):
        """
        Args:
            cwd (str): current working directory's location (full path)
            firebase (class instance / Callable): Firebase DB client
            ids (pandas.Series): Column of client ids from client DF
            names (pandas.Series): Column of client names from client DF
            invoice_ids (pandas.Series): Column of invoice ids from client DF
        """
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
        self.page_break()

    def page_break(self) -> None:
        """
        Break the PDF containing all clients' invoices into singular invoices (1 for each customer)
        Write the resulting PDFs in the appropriate folder (output defined in class_enumerators.py)
        Write the data for clients that could not be matched into the invoice table in Firebase DB
        Populate the object not_found to be used in main script as a filter criteria: filter out unmatched clients
        Args:
            [None]
        Returns:
            [None]
        """
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

                self.firebase.insert_db(
                    class_enumerators.FireBase.SCHEMA_INVOICE,
                    invoice_id,
                    id,
                    name,
                )
        
        self.not_found = not_found
        return None
