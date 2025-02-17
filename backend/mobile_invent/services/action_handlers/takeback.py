import asyncio
import datetime

import requests

from services.atlassian_adapters.unit_factory import Formatter, Insight

from .handler import Handler, InsightError, InsightHandler, JiraError, JiraHandler


class TakebackHandler(JiraHandler, InsightHandler):
    action = "Сдача оборудования"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.ereq = self.item.get("joined", [{}])[0]

    async def handle(self) -> dict:
        """да функция асинхроннаяно выполняется последовательно"""
        if not self.ereq or self.ereq.get("Дата сдачи", False):
            msg = f"{self.operation_id}: Нет открытого Erequest'а для {self.item['label']}"
            self.logger.error(msg)
            return {"result": "", "error": msg}
        if not self.hw_user_id:
            msg = f"{self.operation_id}: Проблема со сдающим пользователем, очевидно же."
            self.logger.error(msg)
            return {"result": "", "error": msg}
        try:
            # Start
            self.logger.info(f"{self.operation_id}: {self.action} {self.item['label']} {self.user['email']}")
            await self._change_erequest()
            await self._insight_inv_client.upload_attachment()
            iterq = await self.jira_create_req(
                "ipad",
                desc=f"Пользователь {self.user.get('email')} создал задачу по сдаче оборудования\n{self.obj_link(self.item)}\nБланк {self.obj_link(self.ereq)}",
            )
            await asyncio.gather(self.jira_add_attachment(itreq=iterq), self.hw_user_update(), return_exceptions=True)
            # End!
            self.logger.info(f"{self.operation_id}: Оборудование успешно сдано {self.obj_link(self.item)}")
            return {"result": "ok", "error": ""}
        except (JiraError, InsightError) as e:
            self.logger.error(f"{self.operation_id}: {e}")
            return {"result": "", "error": str(e)}

    async def _change_erequest(self) -> None:
        cur_date = datetime.date.today()
        inv = Handler.get_field_by_name(self.item["attrs"], "INV No").get("values", [{}])[0].get("label")
        itreq = [
            path
            for path in Handler.get_field_by_name(self.ereq.get("attrs", {}), "Реквест")
            .get("values", [{}])[0]
            .get("label")
            .split("/")
            if path
        ][-1]
        try:
            ereq = await self._insight_inv_client.update_object(
                type_id=78,
                object_id=self.ereq.get("id"),
                attrs={
                    819: f"[{itreq}][{inv}] {self.item['label']}",  # name
                    827: f"{cur_date.day}/{cur_date.month}/{str(cur_date.year)[-2:]}",  # Дата сдачи
                    831: self.hw_user_id,  # Кто принял,
                },
            )
            self.logger.info(f"{self.operation_id}: Erequest {self.obj_link(self.ereq)} отредактирован")
        except Exception as e:
            raise InsightError(e)
