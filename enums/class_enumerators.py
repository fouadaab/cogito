import enum
from typing import NamedTuple
import configparser

config = configparser.ConfigParser()
config.read('conf.ini')


class PathNames(str, enum.Enum):
    DATA_FOLDER = config['PATHNAMES']['DATA_FOLDER']
    OUTPUT_FOLDER = config['PATHNAMES']['OUTPUT_FOLDER']
    PDF_FOLDER = config['PATHNAMES']['PDF_FOLDER']
    FIREBASE_FOLDER = config['PATHNAMES']['FIREBASE_FOLDER']
    STATUS_FOLDER = config['PATHNAMES']['STATUS_FOLDER']
    EXCEL_FILE = config['PATHNAMES']['EXCEL_FILE']
    PDF_FILE = config['PATHNAMES']['PDF_FILE']

class ColumnNames(str, enum.Enum):
    SAISON = "Saison"
    DATE_VALEUR = "Date valeur"
    FACTURE = "Fact."
    STATUT_FACTURE = "Statut facture"
    COMPTA = "Compta"
    LIBELLE = "Libellé"
    NUMERO = "N°"
    MEMBRE = "Membre"
    ACTIF = "Actif"
    CAT = "Cat."
    DATE_ECHEANCE = "Date éch."
    PROCHAINE_ECHEANCE = "Proch. éch."
    PAYE_LE = "Payé le"
    MONTANT_TOTAL = "Mont. total"
    SOLDE = "Solde"
    MONTANT_A_PAYER = "Montant à payer"
    PAYE = "Payé"
    MONTANT_SOLDE = "Montant soldé"
    EXPEDITION_FACT = "Expédition des factures"
    LICENSIE = "Licencié"
    EMAIL = "Email 1"
    ECHELONNEMENT = "Echelonnement"
    ENVOI_ERREUR = "Envoi en erreur"
    SUIVI = "Suivi"
    OVERDUE = "Overdue"

class ColumnTypes(str, enum.Enum):
    STRING = "str"
    FLOAT = "float64"
    INT = "int64"
    BOOLEAN = "bool"


class ColumnToTypeWrapper(NamedTuple):
    column: str
    dtype: str

class GetColumnToType(enum.Enum):
    SAISON = ColumnToTypeWrapper(ColumnNames.SAISON, ColumnTypes.STRING)
    DATE_VALEUR = ColumnToTypeWrapper(ColumnNames.DATE_VALEUR, ColumnTypes.STRING)
    FACTURE = ColumnToTypeWrapper(ColumnNames.FACTURE, ColumnTypes.INT)
    STATUT_FACTURE = ColumnToTypeWrapper(ColumnNames.STATUT_FACTURE, ColumnTypes.STRING)
    COMPTA = ColumnToTypeWrapper(ColumnNames.COMPTA, ColumnTypes.BOOLEAN)
    LIBELLE = ColumnToTypeWrapper(ColumnNames.LIBELLE, ColumnTypes.STRING)
    NUMERO = ColumnToTypeWrapper(ColumnNames.NUMERO, ColumnTypes.INT)
    MEMBRE = ColumnToTypeWrapper(ColumnNames.MEMBRE, ColumnTypes.STRING)
    ACTIF = ColumnToTypeWrapper(ColumnNames.ACTIF, ColumnTypes.BOOLEAN)
    CAT = ColumnToTypeWrapper(ColumnNames.CAT, ColumnTypes.STRING)
    DATE_ECHEANCE = ColumnToTypeWrapper(ColumnNames.DATE_ECHEANCE, ColumnTypes.STRING)
    PROCHAINE_ECHEANCE = ColumnToTypeWrapper(ColumnNames.PROCHAINE_ECHEANCE, ColumnTypes.STRING)
    PAYE_LE = ColumnToTypeWrapper(ColumnNames.PAYE_LE, ColumnTypes.STRING)
    MONTANT_TOTAL = ColumnToTypeWrapper(ColumnNames.MONTANT_TOTAL, ColumnTypes.FLOAT)
    SOLDE = ColumnToTypeWrapper(ColumnNames.SOLDE, ColumnTypes.FLOAT)
    MONTANT_A_PAYER = ColumnToTypeWrapper(ColumnNames.MONTANT_A_PAYER, ColumnTypes.FLOAT)
    PAYE = ColumnToTypeWrapper(ColumnNames.PAYE, ColumnTypes.FLOAT)
    MONTANT_SOLDE = ColumnToTypeWrapper(ColumnNames.MONTANT_SOLDE, ColumnTypes.FLOAT)
    EXPEDITION_FACT = ColumnToTypeWrapper(ColumnNames.EXPEDITION_FACT, ColumnTypes.STRING)
    LICENSIE = ColumnToTypeWrapper(ColumnNames.LICENSIE, ColumnTypes.BOOLEAN)
    EMAIL = ColumnToTypeWrapper(ColumnNames.EMAIL, ColumnTypes.STRING)
    ECHELONNEMENT = ColumnToTypeWrapper(ColumnNames.ECHELONNEMENT, ColumnTypes.STRING)
    ENVOI_ERREUR = ColumnToTypeWrapper(ColumnNames.ENVOI_ERREUR, ColumnTypes.BOOLEAN)
    SUIVI = ColumnToTypeWrapper(ColumnNames.SUIVI, ColumnTypes.STRING)

class EmailAttributes(str, enum.Enum):
    NAMESPACE = config['EMAILATTRIBUTES']['NAMESPACE']
    ENTRY = config['EMAILATTRIBUTES']['ENTRY']
    SENDER = config['EMAILATTRIBUTES']['SENDER']
    CC = config['EMAILATTRIBUTES']['CC']
    ROLE = config['EMAILATTRIBUTES']['ROLE']

class LibelleToStr(str, enum.Enum):
    TRANCHE = "tranche"
    TRANCHE_DE = TRANCHE + " " + "de"
    COTISATION = "la cotisation annuelle"
    ARTICLE = "votre achat"

class FireBase(str, enum.Enum):
    PROJECT_ID = config['FIREBASE']['PROJECT_ID']
    SCHEMA_INVOICE = config['FIREBASE']['SCHEMA_INVOICE']
    SCHEMA_SENT = config['FIREBASE']['SCHEMA_SENT']
    CURRENT_SEASON = config['FIREBASE']['CURRENT_SEASON']
    DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"
    SENT_ID = "id"
    SENT_NAME = "name"
    SENT_SEASON = "season"
    SENT_DATE = "date"

class OverdueInvoice(enum.IntEnum):
    LIMIT = config['OVERDUE']['LIMIT']