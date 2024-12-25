import base64
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
    def handle(cls, item: dict[str, Any],user_email: str, user_id: int, operation_id: str, file, store, **kwargs) -> dict[str, str|dict]:
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
            ereq = cls.change_erequest(ereq_id, user_id, name)
            cls.logger.info(f'{operation_id}: Erequest {cls.obj_link(ereq_id)} отредактирован')
            cls.insight_add_attachment(ereq_id, file)
            cls.logger.info(f'{operation_id}: К Erequest`у добавлен файл')
            jreq = cls.jira_create_req(user_email, 
                                       cls.get_field_by_name(store['attrs'], "Jira Issue Location").get("values", [{}])[0].get('label', ''), 
                                       cls.obj_link(ereq_id), cls.obj_link(item['id']), cls.get_component(item))
            cls.logger.info(f'{operation_id}: Заявка https://jira.metro-cc.ru/browse/{123} создана')
            cls.jira_add_attachment(itreq=jreq, file=file)
            cls.logger.info(f'{operation_id}: Файл {file.name} добавлен к заявке')
            cls.logger.info(f'{operation_id}: Оборудование успешно сдано {cls.obj_link(item['id'])}')
            return {"result": ereq, "error": ""}
        except (ITREQError, EreqChangeError) as e:
            cls.logger.error(f'{operation_id}: {e}')
            return {"result": "", "error": str(e)}


    @classmethod
    def change_erequest(cls, ereq_id, user_id, name: str):
        cur_date = datetime.date.today()
        ereq_change_response = requests.post('http://127.0.0.1:8000/update', json={'scheme': 1, "object_type_id": 78, "object_id": ereq_id,
                                  "attrs":{
                                        819: [name],                                                              # name
                                        827: [f'{cur_date.day}/{cur_date.month}/{str(cur_date.year)[-2:]}'],      # Дата сдачи
                                        831: [user_id],                                                         #Кто принял,
            }})
        if ereq_change_response.status_code == 200:
            return ereq_change_response.json()
        raise EreqChangeError('')


        
    @classmethod
    def jira_create_req(cls, email, location, ereq, item, component):
        jreq = requests.post('', json={
            "summary": f"Сдача мобильного оборудования ТЦ {location.split()[0]}",
            "description": f'Пользователь {email} создал задачу по сдаче оборудования\n{item}\nБланк {ereq}',
            "Metro Team": 'Support Remote',
            "Issue Location": location,
            "component": component,
            })
        if jreq.status_code == 200:
            return jreq.json()
        raise ITREQError('Проблема при создании заявки в Jira')

    @classmethod
    def jira_add_attachment(cls, itreq: str, file):
        source = base64.b64encode(file.read()).decode("utf-8")
        res = requests.post('http://127.0.0.1:8000/add_attachment', json={"project": "it", "issue": itreq, "name": file.name, "source": source})
        if res.status_code == 200:
            return None
        raise ITREQError("Проблема при добавлении к Jira реквесту файла")

    @classmethod
    def insight_add_attachment(cls, ereq_id, file):
        pass


    @classmethod
    def get_component(cls, item):
        components = {"ipad": "iPad",
                      "laptop": "Laptop",
                     }
        return ''
