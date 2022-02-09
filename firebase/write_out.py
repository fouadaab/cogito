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
        self.cwd = cwd
        self.status = [
            self.new_dict(key, val) for key, val in status.items() 
        ]
        self.write_excel()

    def new_dict(self, key: int, val: Dict[str, Any]) -> Dict[str, Any]:
        _dict = {class_enumerators.ColumnNames.FACTURE: key}
        _dict.update(val)
        return _dict

    def write_excel(self) -> None:
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