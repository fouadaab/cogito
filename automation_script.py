"""
TODOS - Improvements:
1. path lib (file/folder path)
2. string lib (message)
"""

import os
from processing import data_source, pdf_splitter
from enums import class_enumerators
from emails import email_api
from firebase import firebase_config , write_out

cwd = os.path.abspath(os.path.dirname(__file__))

if __name__ == "__main__":

    # Initialize Firebase DB
    firebase = firebase_config.initialize_firebase()
    
    # Initialize email object
    email_object = email_api.Email(cwd, firebase)

    # Collect input data and write in Pandas DataFrame
    data_object = data_source.Data(cwd)
    df = data_object.read_data()

    # Split invoices and write in PDF output folder
    write_pdfs = pdf_splitter.PdfWriter(
        cwd=cwd,
        firebase=firebase,
        ids=df[class_enumerators.ColumnNames.NUMERO],
        names=df[class_enumerators.ColumnNames.MEMBRE],
        invoice_ids=df[class_enumerators.ColumnNames.FACTURE],
    )

    # Get filter list of members to exclude from reminders
    pdfs_not_found = write_pdfs.not_found
    already_sent = list(firebase.collect_from_db().keys())
    filter_out = set(pdfs_not_found + already_sent)

    # Filter out DF using DB collect -> collect past reminders + Missing Invoice
    df = df[~df[class_enumerators.ColumnNames.FACTURE].isin(filter_out)]
    
    # Send out emails to each overdue member
    df = df.apply(lambda x: email_object.check_condition(x), axis=1)
    
    # Add extract to output -> Updated status after script run
    status = firebase.collect_from_db()
    write_out.CurrentStatus(cwd, status)

    print("Successfully Completed Automation Script")