# https://console.cloud.google.com/firestore/data/{collection_name}/{document_name}?project={project_id}
# https://console.developers.google.com/apis/api/firestore.googleapis.com/metrics?project={project_id}&authuser=1
from typing import Callable, Dict, Any
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
import helper.class_enumerators as class_enumerators

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
    saison: str,
    date=datetime.datetime.now(),
  ):
    self.id = id
    self.name = name
    self.saison = saison
    self.date = date.strftime(class_enumerators.FireBase.DATETIME_FORMAT)

  def to_dict(self) -> Dict[str, Any]:
    return self.__dict__
  
  def __repr__(self):
      return(
          f'Member(\
              {class_enumerators.FireBase.SENT_ID}={self.id}, \
              {class_enumerators.FireBase.SENT_NAME}={self.name}, \
              {class_enumerators.FireBase.SENT_SAISON}={self.saison}, \
              {class_enumerators.FireBase.SENT_DATE}={self.date}\
          )'
      )

