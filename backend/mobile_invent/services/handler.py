import time
from abc import ABC, abstractmethod

import requests


class Handler(ABC):
    logger = ''

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
                cls.logger.info('{operation_id} user: user['email']')
                update = func(cls, item, *args, **kwargs)
                if not update.get("error", False):
                    time.sleep(3)
                    # requests.post('', json={"HWUserUpdate": user_id})  
                return update
            return {}
        return wrapper


    @abstractmethod
    @classmethod
    def handle(cls, item, user, **kwargs) -> dict:
        pass
