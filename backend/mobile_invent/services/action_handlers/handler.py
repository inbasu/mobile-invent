import base64
import time
from abc import ABC, abstractmethod
from logging import getLogger
from typing import Any

import requests


class InsightError(Exception):
    pass

class JiraError(Exception):
    pass

class Handler(ABC):
    logger = getLogger("mobile")
    action: str

    def __init__(self, operation_id, item, user, store) -> None:
        self.operation_id = operation_id
        self.item = item
        self.user = user
        self.hw_user_id = self.get_user()
        self.store = store

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
    
    def obj_link(self, obj) -> str:
        return f'https://jirainvent.metro-cc.ru/secure/insight/assets/IN-{obj.get('id')}'



    @staticmethod
    def hw_user_update(func):
        def wrapper(self, *args, **kwargs):
            if user_id := self.hw_user_id:
                Handler.logger.info(f'{self.operation_id}: {self.action} {self.item["label"]} {self.user['email']}')
                update = func(self, *args, **kwargs)
                if not update.get("error", False):
                    time.sleep(3)
                    requests.post('http://127.0.0.1:8000/update', json={"scheme": 1, "object_type_id": 8, "object_id": self.item["id"],
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


    def jira_create_req(self, description: str):
        jreq = requests.post('', json={
            "summary": f"{self.action} мобильного оборудования ТЦ",
            "description": description,
            "Metro Team": 'Support Remote',
            "Issue Location": self.get_field_by_name(self.store["attrs"], "Jira Issue Location").get("values", [{}])[0].get('label', ''),
            "component": self.get_component(),
            })
        if jreq.status_code == 200:
            return jreq.json()
        raise ITREQError('Проблема при создании заявки в Jira')



#  ,
