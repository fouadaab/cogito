import os
from pathlib import Path
from helper import data_source, pdf_splitter, class_enumerators, email_api, firebase_config, write_out

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
        firebase=db,
        ids=df[class_enumerators.ColumnNames.NUMERO],
        names=df[class_enumerators.ColumnNames.MEMBRE],
        invoice_ids=df[class_enumerators.ColumnNames.FACTURE],
    )

    # Get filter list of members to exclude from reminders
    pdfs_not_found = write_pdfs.not_found
    already_sent = list(email_object.collect_from_db().keys())
    filter_out = set(pdfs_not_found + already_sent)

    # Filter out DF using DB collect -> collect past reminders + Missing Invoice
    df = df[~df[class_enumerators.ColumnNames.FACTURE].isin(filter_out)]
    
    # Send out emails to each overdue member
    df = df.apply(lambda x: email_object.check_condition(x), axis=1)
    
    # Add extract to output -> Updated status after script run
    status = email_object.collect_from_db(schema=class_enumerators.FireBase.SCHEMA_SENT)
    write_out.CurrentStatus(cwd, status)

    print("Successfully Completed Automation Script")


# TODOS - Improvements:
# 0. method not lambda (not serializable) -> implemented
# 1. firebase (google) i.o sqlite (record tracking) -> Implemented
# 2. with context email class -> implemented
# 3. path lib (file/folder path)
# 4. string lib (message)