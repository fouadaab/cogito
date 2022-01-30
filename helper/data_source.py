import os
import datetime
import pandas as pd
from .class_imports import *


class Data():
    """
    TODO: Add Dodstring
    """
    def __init__(self, cwd: str):
        data_file = f"{PathNames.FACTURES}.xls"
        self.xls_path = os.path.abspath(
            os.path.join(
                cwd,
                PathNames.DATA_FOLDER,
                data_file,
            )
        )
        self.column_types = {
            col.value.column: col.value.dtype for col in GetColumnToType
        }
        self.parse_dates = [
            ColumnNames.DATE_VALEUR,
            ColumnNames.DATE_ECHEANCE,
            ColumnNames.PROCHAINE_ECHEANCE,
            ColumnNames.PAYE_LE,
        ]
        self.date_parser = lambda x: pd.to_datetime(x, format='%d.%m.%Y')
        self.date_diff = lambda x: (datetime.datetime.today() - x).days

    def read_data(self) -> pd.DataFrame:
        """
        TODO: Add Docstring
        """
        df = pd.read_excel(
                self.xls_path,
                dtype=self.column_types,
                parse_dates=self.parse_dates,
                date_parser=self.date_parser
            )
        df[ColumnNames.OVERDUE] = df[ColumnNames.DATE_ECHEANCE].apply(self.date_diff)

        return df