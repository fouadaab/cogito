from enums import class_enumerators
from typing import Dict, Any
import datetime


class Member(object):
  """
  Class object in which we write the client data that will be uploaded to Firebase DB
  """

  def __init__(
    self,
    id: int,
    name: str,
    season: str = class_enumerators.FireBase.CURRENT_SEASON,
    date: datetime.datetime = datetime.datetime.now(),
  ):
    self.id = id
    self.name = name
    self.season = season
    self.date = date.strftime(class_enumerators.FireBase.DATETIME_FORMAT)

  def to_dict(self) -> Dict[str, Any]:
    return self.__dict__
  
  def __repr__(self):
      return(
          f'Member(\
              {class_enumerators.FireBase.SENT_ID}={self.id}, \
              {class_enumerators.FireBase.SENT_NAME}={self.name}, \
              {class_enumerators.FireBase.SENT_SEASON}={self.season}, \
              {class_enumerators.FireBase.SENT_DATE}={self.date}\
          )'
      )