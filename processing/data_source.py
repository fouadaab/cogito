import os
import datetime
import pandas as pd
import enums.class_enumerators as class_enumerators


class Data():
    """
    Data class object (store client's data from Excel in a pandas DatFrame)
    """

    def __init__(self, cwd: str):
        """
        Args:
            cwd (str): current working directory's location (full path)
        """
        data_file = f"{class_enumerators.PathNames.EXCEL_FILE}.xls"
        self.xls_path = os.path.abspath(
            os.path.join(
                cwd,
                class_enumerators.PathNames.DATA_FOLDER,
                data_file,
            )
        )
        self.column_types = {
            col.value.column: col.value.dtype for col in class_enumerators.GetColumnToType
        }
        self.parse_dates = [
            class_enumerators.ColumnNames.DATE_VALEUR,
            class_enumerators.ColumnNames.DATE_ECHEANCE,
            class_enumerators.ColumnNames.PROCHAINE_ECHEANCE,
            class_enumerators.ColumnNames.PAYE_LE,
        ]
        
    def date_parser(self, x: str) -> datetime.datetime:
        return pd.to_datetime(x, format='%d.%m.%Y')
    
    def date_diff(self, x: datetime.datetime) -> int:
         return (datetime.datetime.today() - x).days

    def read_data(self) -> pd.DataFrame:
        """
        Read data using pandas method read_excel()
        Data types are defined in class_enumerators.GetColumnToType
        We define the columns that will be parsed as dates -> parse_dates object
        A custom method date_parser() is used to employ the desired format
        Data attribute OVERDUE is generated based on the time difference (days) between today and DATE_ECHEANCE

        Args:
            [None]
        Returns:
            [None]
        """
        df = pd.read_excel(
                self.xls_path,
                dtype=self.column_types,
                parse_dates=self.parse_dates,
                date_parser=self.date_parser
            )
        df[class_enumerators.ColumnNames.OVERDUE] = df[class_enumerators.ColumnNames.DATE_ECHEANCE].apply(self.date_diff)
        return df