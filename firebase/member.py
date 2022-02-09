from enums import class_enumerators
from typing import Dict, Any
import datetime


class Member(object):

  def __init__(
    self,
    id: int,
    name: str,
    saison: str = class_enumerators.FireBase.SAISON_21_22,
    date: datetime.datetime = datetime.datetime.now(),
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