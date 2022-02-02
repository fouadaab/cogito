from PyPDF2 import PdfFileWriter, PdfFileReader
from typing import List
import helper.class_enumerators as class_enumerators
import pandas
import re
import os

class PdfWriter():
    """
    TODO: update not_found after inital DEV phase
    """
    not_found: List[str]

    def __init__(
        self,
        cwd: str,
        names: pandas.Series,
        ids: pandas.Series,
    ):
        self.cwd = cwd
        self.file_name = os.path.abspath(
            os.path.join(
                self.cwd,
                class_enumerators.PathNames.DATA_FOLDER,
                f"{class_enumerators.PathNames.PDF_FILE}.pdf",
            )
        )
        self.names = names
        self.ids = ids
        self.getPagebreakList()

    def getPagebreakList(self) -> None:

        not_found = list()
        pdf_file = PdfFileReader(self.file_name)
        num_pages = pdf_file.getNumPages()
        if num_pages != len(self.names):
            raise ValueError(f"{num_pages} pages found when passing list of {len(self.names)} members")

        for i, (name, id) in enumerate(zip(self.names, self.ids)):
            output = PdfFileWriter()
            pageobj = pdf_file.getPage(i)
            output.addPage(pageobj)
            
            Text = pageobj.extractText()
            pattern = rf"(?:{name} \({id}\))"

            if re.findall(pattern, Text):
                with open(
                    os.path.join(
                        self.cwd,
                        class_enumerators.PathNames.PDF_FOLDER,
                        f"Facture-{name}-{id}.pdf"
                    ),
                    "wb") as outputStream:
                    output.write(outputStream)
            else:
                not_found.append(f"{name}_{id}")
        
        self.not_found = not_found

        return None
