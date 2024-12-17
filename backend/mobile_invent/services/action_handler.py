import datetime
import time

import requests


class EreqChangeError(Exception):
    pass

class ActionHandler:


    @classmethod
    def get_user(cls, email: str) -> int:
        resp = requests.post('http://127.0.0.1:8000/iql', json={"scheme": 2, "iql":f"objectTypeId = 57 AND Email = {email}"}).json()
        try:
            return resp[0].get('id', 0)
        except IndexError:
            return 0
    
    @staticmethod
    def hw_user_update(func):
        def wrapper(cls, operation_id: str, user, item, *args, **kwargs):
            if user_id := cls.get_user(user['email']):
                # logger.info('{operation_id} user: user['email']')
                update = func(cls, item, *args, **kwargs)
                if not update.get("error", False):
                    time.sleep(3)
                    # requests.post('', json={"HWUserUpdate": user_id})  
                return update
            return {}
        return wrapper


    
    @classmethod
    @hw_user_update
    def takeback(cls, item, user: int, **kwargs) -> dict[str, str]:
        ereqs = item.get('joined', False)
        if not ereqs or not ereqs[0].get("id"):
            # logger.error() 
            return {}
        ereq_id = ereqs[0].get("id")
        try:
            issue = cls.jira_req()
            ereq = cls.change_erequest(user, ereq_id)
            # add attachment
            #logger.info()
            return {"result": "Оборудование успешно сдано", "error": ""}
        except EreqChangeError:
            #logger.error('')
            return {}




    @classmethod
    def change_erequest(cls, ereq_id, user):
        cur_date = datetime.date.today()
        try:
            ereq_change_response = requests.post('/update', {'scheme': 1, "object_type_id": 8, "object_id": {},
                                  "attributes":{
                                        0: f'{1}',
                                        1: f'{cur_date.day}/{cur_date.month}/{str(cur_date.year)[-2:]}', # Дата сдачи
                                        2: user,    #Кто принял,
                                      }})
        except:
            raise EreqChangeError('')


        
    @classmethod
    def jira_req(cls,data, file) -> str:
        # create jira requests
        #logging.info('')
        #add.attachment
        #logging.
        return ''
