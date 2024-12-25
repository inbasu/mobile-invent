import datetime

import requests

from mobile_invent.services.handler import EreqChangeError, Handler, ITREQError


class TakebackHandler(Handler):

    def __init__(self, item, user, hw_user_id, store, operation_id, file) -> None:
        self.item = item
        self.ereq = item.get('joined', [{}])[0]
        self.ereq_id = self.ereq.get('id')
        self.user = user
        self.hw_user_id = hw_user_id
        self.store = store
        self.file = file
        self.operation_id = operation_id
        


    @Handler.hw_user_update
    def handle(self) -> dict[str, str|dict]:
        if not self.ereq or self.ereq.get("Дата сдачи", False):
            msg = f"{self.operation_id}: Нет открытого Erequest'а для {self.item["label"]}"
            self.logger.error(msg) 
            return {"result": "", "error": msg}
        itreq = [path for path in Handler.get_field_by_name(self.ereq.get("attrs", {}), "Реквест").get("values", [{}])[0].get("label").split('/') if path][-1]
        inv = Handler.get_field_by_name(self.item['attrs'], "INV No").get('values', [{}])[0].get("label")
        ereq_id = self.ereq[0].get('id'),
        try:
            ereq = self.change_erequest(name=f'[{itreq}][{inv}] {self.item["label"]}')
            self.logger.info(f'{self.operation_id}: Erequest {self.obj_link(self.ereq_id)} отредактирован')
            self.insight_add_attachment(ereq_id, self.file)
            self.logger.info(f'{self.operation_id}: К Erequest`у добавлен файл')
            jreq = self.jira_create_req(self.user.get("email"), 
                                       Handler.get_field_by_name(self.store['attrs'], "Jira Issue Location").get("values", [{}])[0].get('label', ''), 
                                       self.obj_link(self.ereq_id), self.obj_link(self.item['id']), self.get_component())
            self.logger.info(f'{self.operation_id}: Заявка https://jira.metro-cc.ru/browse/{123} создана')
            self.jira_add_attachment(itreq=jreq, file=self.file)
            self.logger.info(f'{self.operation_id}: Файл {self.file.name} добавлен к заявке')
            self.logger.info(f'{self.operation_id}: Оборудование успешно сдано {self.obj_link(self.item['id'])}')
            return {"result": ereq, "error": ""}
        except (ITREQError, EreqChangeError) as e:
            self.logger.error(f'{self.operation_id}: {e}')
            return {"result": "", "error": str(e)}


    def change_erequest(self, name: str):
        cur_date = datetime.date.today()
        ereq_change_response = requests.post('http://127.0.0.1:8000/update', json={'scheme': 1, "object_type_id": 78, "object_id": self.ereq_id,
                                  "attrs":{
                                        819: [name],                                                              # name
                                        827: [f'{cur_date.day}/{cur_date.month}/{str(cur_date.year)[-2:]}'],      # Дата сдачи
                                        831: [self.hw_user_id],                                                         #Кто принял,
            }})
        if ereq_change_response.status_code == 200:
            return ereq_change_response.json()
        raise EreqChangeError('')


        
    def jira_create_req(self, email, location, ereq, item, component):
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






