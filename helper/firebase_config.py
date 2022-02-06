# https://console.cloud.google.com/firestore/data/{collection_name}/{document_name}?project={project_id}
# https://console.developers.google.com/apis/api/firestore.googleapis.com/metrics?project={project_id}&authuser=1
from typing import Callable, Dict, Any
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
from pathlib import Path
import datetime
import class_enumerators as class_enumerators


class Database():
  db: Callable

  def __init__(self, key: str):
    self.key = key
    self.db_client()

  def db_client(self) -> None:
    # Use a service account with Firebase DB
    cred = credentials.Certificate(self.key)
    firebase_admin.initialize_app(cred)
    self.db = firestore.client()


class Member(object):

  def __init__(
    self,
    id: int,
    name: str,
    facture: int,
    saison: str,
    date=datetime.datetime.now()
  ):
    self.id = id
    self.name = name
    self.facture = facture
    self.saison = saison
    self.date = date.strftime(class_enumerators.FireBase.DATETIME_FORMAT)

  def to_dict(self) -> Dict[str, Any]:
    return self.__dict__
  
  def __repr__(self):
      return(
          f'Member(\
              id={self.id}, \
              name={self.name}, \
              facture N°={self.facture}, \
              saison={self.saison}, \
              date={self.date}\
          )'
      )


p = Path('.')
matches = p.glob(f'{class_enumerators.FireBase.PROJECT_ID}*.json')
for i, match in enumerate(matches):
  if i > 0:
    raise(ValueError(f"Too many json files matching name of Firebase key for project {class_enumerators.FireBase.PROJECT_ID}"))
  key = match

db = Database(key).db

# INSERT #
reminder_sent = db.collection(u'sent')
reminder_sent.document(u'1').set(
    Member(u'0001', u'Richard Blanc', u'1234', u'2021-2022').to_dict()
)
reminder_sent.document(u'2').set(
    Member(u'0002', u'Robert Noir', u'1235', u'2020-2021').to_dict()
)
reminder_sent.document(u'3').set(
    Member(u'0002', u'Robert Noir', u'1236', u'2021-2022').to_dict()
)

# COLLECT #
# Note: Use of CollectionRef stream() is prefered to get()
docs = reminder_sent.where(u'id', u'==', '0002').stream()
for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')