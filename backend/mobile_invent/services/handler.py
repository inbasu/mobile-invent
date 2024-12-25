import base64
import time
from abc import ABC, abstractmethod
from logging import getLogger
from typing import Any

import requests


class EreqChangeError(Exception):
    pass

class ITREQError(Exception):
    pass

class Handler(ABC):
    logger = getLogger("mobile")
    user: dict

    @staticmethod
    def get_field_by_name(fields: list[dict], name: str):
        for field in fields:
            if field["name"] == name:
                return field
        return {}

    @staticmethod
    def get_label_of_field(field: dict) -> Any:
        return field.get("values", [{}])[0].get("label")


    def get_user(self) -> int:
        resp = requests.post('http://127.0.0.1:8000/iql', json={"scheme": 2, "iql":f"objectTypeId = 57 AND Email = {self.user.get('email')}"}).json()
        try:
            return resp[0].get('id', 0)
        except IndexError:
            return 0
    
    def obj_link(self, id: int) -> str:
        return f'https://jirainvent.metro-cc.ru/secure/insight/assets/IN-{id}'



    @staticmethod
    def hw_user_update(func):
        def wrapper(cls, operation_id: str, user, item, action, *args, **kwargs):
            if user_id := cls.get_user(user['email']):
                cls.logger.info(f'{operation_id}: {user['email']} {action.upper()} {item["label"]}')
                update = func(cls, item=item, hws_user_id=user_id, operation_id=operation_id ,*args, **kwargs)
                if not update.get("error", False):
                    time.sleep(3)
                    requests.post('http://127.0.0.1:8000/update', json={"scheme": 1, "object_type_id": 8, "object_id": item["id"],
                                                                        "attrs":{2427: [user_id]}})  
                return update
            return {}
        return wrapper


    @abstractmethod
    def handle(self) -> dict:
        pass

    def jira_add_attachment(self, itreq: str, file):
        source = base64.b64encode(file.read()).decode("utf-8")
        res = requests.post('http://127.0.0.1:8000/add_attachment', json={"project": "it", "issue": itreq, "name": file.name, "source": source})
        if res.status_code == 200:
            return None
        raise ITREQError("Проблема при добавлении к Jira реквесту файла")


    def get_component(self):
        components = {"ipad": "iPad",
                      "laptop": "Laptop",
                     }
        return ''



    def insight_add_attachment(self, id, file):
        pass
