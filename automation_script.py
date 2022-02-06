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
    email_object = email_api.Email(cwd)
    df = df.apply(lambda x: email_object.check_condition(x), axis=1)

    print("Successfully Completed Automation Script")


# TODOS - Improvements:
# 0. method not lambda (not serializable) -> implemented
# 1. firebase (google) i.o sqlite (record tracking) -> Implementing on 06/02/2022
# 2. with context email class -> implemented
# 3. path lib (file/folder path)
# 4. string lib (message)