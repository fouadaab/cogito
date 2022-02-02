import os
from helper import data_source, pdf_splitter, class_enumerators, email_api

cwd = os.path.abspath(os.path.dirname(__file__))

if __name__ == "__main__":

    # Collect input data and write in Pandas DataFrame
    data_object = data_source.Data(cwd)
    df = data_object.read_data()

    # Split invoices and write in PDF output folder
    write_pdfs = pdf_splitter.PdfWriter(
        cwd=cwd,
        names=df[class_enumerators.ColumnNames.MEMBRE],
        ids=df[class_enumerators.ColumnNames.NUMERO],
    )
    print(f"Members for which we could not generate a PDF invoice: {write_pdfs.not_found}")

    # Send out emails to each overdue member
    """
    TODO: Only send based on OVERDUE column (conditional)
    """
    email_object = email_api.Email(cwd)
    df = df.apply(lambda x: email_object.send_email(x), axis=1)

    print("Successfully Completed Automation Script")
