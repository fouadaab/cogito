import os
from pathlib import Path
from helper import data_source, pdf_splitter, class_enumerators, email_api, firebase_config

cwd = os.path.abspath(os.path.dirname(__file__))

if __name__ == "__main__":

    # Initialize Firebase DB
    p = Path('.')
    matches = p.glob(f'{class_enumerators.FireBase.PROJECT_ID}*.json')
    for i, match in enumerate(matches):
        if i > 0:
            raise(ValueError(f"Too many json files matching name of Firebase key for project {class_enumerators.FireBase.PROJECT_ID}"))
        key = match
    db = firebase_config.Database(key).db

    # Initialize email object
    email_object = email_api.Email(cwd, db)

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

    # Filter out DF using DB collect -> collect past reminders
    already_sent = email_object.collect_from_db()
    df = df[~df[class_enumerators.ColumnNames.FACTURE].isin(already_sent)]
    
    # Send out emails to each overdue member
    df = df.apply(lambda x: email_object.check_condition(x), axis=1)
    
    # TODO: Add extract to output -> Updated status after script run

    print("Successfully Completed Automation Script")


# TODOS - Improvements:
# 0. method not lambda (not serializable) -> implemented
# 1. firebase (google) i.o sqlite (record tracking) -> Implemented
# 2. with context email class -> implemented
# 3. path lib (file/folder path)
# 4. string lib (message)