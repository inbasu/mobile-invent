import datetime
from typing import Any

import requests

from mobile_invent.services.handler import Handler


class EreqChangeError(Exception):
    pass

class ITREQError(Exception):
    pass

class TakebackHandler(Handler):

    @classmethod
    @Handler.hw_user_update
    def handle(cls, item: dict[str, Any], user: int, operation_id: str, file=None, **kwargs) -> dict[str, str|dict]:
        ereqs = item.get('joined', False)
        if not ereqs or not ereqs[0].get("id", False) or ereqs[0].get("Дата сдачи", False):
            msg = f"{operation_id}: Нет открытого Erequest'а для {item["label"]}"
            cls.logger.error(msg) 
            return {"result": "", "error": msg}
        ereq_id = ereqs[0].get("id")
        itreq = [path for path in cls.get_field_by_name(ereqs[0].get("attrs", {}), "Реквест").get("values", [{}])[0].get("label").split('/') if path][-1]
        inv = cls.get_field_by_name(item['attrs'], "INV No").get('values', [{}])[0].get("label")
        name = f'[{itreq}][{inv}] {item["label"]}'
        try:
            # jreq = cls.jira_create_req(file)
            ereq = cls.change_erequest(ereq_id, user, name)
            cls.logger.info(f'{operation_id}: Erequest {cls.obj_link(ereq_id)} отредактирован')
            # cls.add_attachment(ereq_id, file)
            return {"result": ereq, "error": ""}
        except EreqChangeError:
            cls.logger.error(f'{operation_id}: ')
            return {}


    @classmethod
    def change_erequest(cls, ereq_id, user_id, name: str):
        cur_date = datetime.date.today()
        ereq_change_response = requests.post('http://127.0.0.1:8000/update', json={'scheme': 1, "object_type_id": 78, "object_id": ereq_id,
                                  "attrs":{
                                        819: [name],                                                              # name
                                        827: [f'{cur_date.day}/{cur_date.month}/{str(cur_date.year)[-2:]}'],      # Дата сдачи
                                        831: [user_id],                                                           #Кто принял,
            }})
        if ereq_change_response.status_code == 200:
            return ereq_change_response.json()
        raise EreqChangeError('')


        
    @classmethod
    def jira_create_req(cls, file):
        jreq = requests.post('', json={
            "summary": '',
            "description": '',
            "Metro Team": '',
            "Issue Location": ''
            })
        if jreq.status_code == 200:
            return jreq.json()
        raise ITREQError('')

    @classmethod
    def add_attachment(cls, ereq_id, file):
        pass
