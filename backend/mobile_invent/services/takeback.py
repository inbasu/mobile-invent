import datetime

import requests

from mobile_invent.services.handler import Handler


class EreqChangeError(Exception):
    pass

class TakebackHandler(Handler):

    @classmethod
    @Handler.hw_user_update
    def handle(cls, item, user: int, file, **kwargs) -> dict[str, str|dict]:
        ereqs = item.get('joined', False)
        if not ereqs or not ereqs[0].get("id"):
            # logger.error() 
            return {}
        ereq_id = ereqs[0].get("id")
        try:
            cls.jira_req('', file)
            ereq = cls.change_erequest(user, ereq_id)
            cls.add_attachment(ereq_id, file)
            #logger.info()
            return {"result": ereq, "error": ""}
        except EreqChangeError:
            #logger.error('')
            return {}


    @classmethod
    def change_erequest(cls, ereq_id, user):
        cur_date = datetime.date.today()
        try:
            ereq_change_response = requests.post('/update', {'scheme': 1, "object_type_id": 8, "object_id": {},
                                  "attributes":{
                                        0: f'{1}',                                                       # pass   
                                        1: f'{cur_date.day}/{cur_date.month}/{str(cur_date.year)[-2:]}', # Дата сдачи
                                        2: user,                                                         #Кто принял,
                                      }})
            return ereq_change_response.json()
        except:
            raise EreqChangeError('')


        
    @classmethod
    def jira_req(cls, data, file) -> str:
        # create jira requests
        #logging.info('')
        #add.attachment
        #logging.
        return ''


    @classmethod
    def add_attachment(cls, ereq_id, file):
        pass
