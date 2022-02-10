import os
import csv
from typing import Dict, Any
from datetime import date
import enums.class_enumerators as class_enumerators


class CurrentStatus(object):

    def __init__(
        self,
        cwd: str,
        status: Dict[int, Dict[str, Any]],
    ):
        """
        Args:
            cwd (str): current working directory's location (full path)
            status (Dict[int, Dict[str, Any]]): Firebase DB extract of (already) sent reminders 
        """
        self.cwd = cwd
        self.status = [
            self.new_dict(key, val) for key, val in status.items() 
        ]
        self.write_excel()

    def new_dict(self, key: int, val: Dict[str, Any]) -> Dict[str, Any]:
        """
        Function to re-shape the extract from the Firebase DB
        For every item in the Dict:
            - The key is the invoice N° (serving in DB as PK)
            - The value is a Dict containing the client details and timestamp
        For each item, include the key in the values and refer it as the invoice number

        Args:
            key (int): The invoice N° (serving in DB as PK)
            val (Dict[str, Any]): Contains the client details and timestamp of the last reminder
        Returns:
            [Dict[str, Any]]: Dictionary combining invoice number and client details to write into local csv file
        """
        _dict = {class_enumerators.ColumnNames.FACTURE: key}
        _dict.update(val)
        return _dict

    def write_excel(self) -> None:
        """
        Write all invoice reminders sent to clients currently sitting in Firebase DB for the on-going season
        Write in csv file at specific location defined in class_enumerators.py / conf.ini

        Args:
            [None]
        Returns:
            [None]
        """
        with open(
            os.path.join(
                self.cwd,
                class_enumerators.PathNames.OUTPUT_FOLDER,
                class_enumerators.PathNames.STATUS_FOLDER,
                f"{date.today()}.csv",
            ),
            "w") as outputStream:
            
            writer = csv.DictWriter(outputStream, fieldnames=self.status[0].keys())
            writer.writeheader()
            for row in self.status:
                writer.writerow(row)