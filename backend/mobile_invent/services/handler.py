import time
from abc import ABC, abstractmethod
from logging import getLogger

import requests


class Handler(ABC):
    logger = getLogger("mobile")

    @classmethod
    def get_field_by_name(cls, fields: list[dict], name: str):
        for field in fields:
            if field["name"] == name:
                return field
        return {}

    @classmethod
    def get_user(cls, email: str) -> int:
        resp = requests.post('http://127.0.0.1:8000/iql', json={"scheme": 2, "iql":f"objectTypeId = 57 AND Email = {email}"}).json()
        try:
            return resp[0].get('id', 0)
        except IndexError:
            return 0
    
    @classmethod
    def obj_link(cls, id: int) -> str:
        return f'https://jirainvent.metro-cc.ru/secure/insight/assets/IN-{id}'


    @staticmethod
    def hw_user_update(func):
        def wrapper(cls, operation_id: str, user, item, action, *args, **kwargs):
            if user_id := cls.get_user(user['email']):
                cls.logger.info(f'{operation_id}: {user['email']} {action.upper()} {item["label"]}')
                update = func(cls, item=item, user=user_id, operation_id=operation_id ,*args, **kwargs)
                if not update.get("error", False):
                    time.sleep(3)
                    requests.post('http://127.0.0.1:8000/update', json={"scheme": 1, "object_type_id": 8, "object_id": item["id"],
                                                                        "attrs":{2427: [user_id]}})  
                return update
            return {}
        return wrapper


    @classmethod
    @abstractmethod
    def handle(cls, item, user, **kwargs) -> dict:
        pass
