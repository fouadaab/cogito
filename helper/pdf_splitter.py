from PyPDF2 import PdfFileWriter, PdfFileReader
from typing import List
import re

class PdfWriter():
    not_found: List[str]

    def __init__(
        self,
        file_name: str,
        names: List[str],
        ids: List[str],
    ):
        self.file_name = file_name
        self.names = names
        self.ids = ids
        self.getPagebreakList()

    def getPagebreakList(self) -> List[str]:

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
                with open(f"/home/johndoe/Documents/test codes/handball_accounting_automation/ouput/PDFs/Facture-{name}-{id}.pdf", "wb") as outputStream:
                    output.write(outputStream)
            else:
                not_found.append(f"{name}_{id}")
        
        self.not_found = not_found

        return None

if __name__ == '__main__':
    
    names = [
        "GRIBI Alain",
        "KUPFRSCHMID Sophie & Denis",
        "RAMEL Armand",
        "FREI Maurice",
        "DA SILVA André",
        "DUTASTA Fabien",
        "HARRINGTON Rodney",
        ]
    ids = [
        3234,
        3281,
        3222,
        3241,
        3583,
        3580,
        3582,
    ]
    write_pdfs = PdfWriter(
        "/home/johndoe/Documents/test codes/handball_accounting_automation/data/DOC4965810388239128821.pdf",
        names,
        ids,
    )
    print(write_pdfs.not_found)