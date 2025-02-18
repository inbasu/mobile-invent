import asyncio
import datetime

from django.core.exceptions import ValidationError

from .handler import Handler, InsightError, InsightHandler, JiraError, JiraHandler


class TakebackHandler(JiraHandler, InsightHandler):
    action = "Сдача оборудования"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def handle(self) -> dict:
        """да функция асинхроннаяно выполняется последовательно"""
        try:
            # Start
            await self._validate()
            self.logger.info(f"{self.operation_id}: {self.action} {self.item['label']} {self.user['email']}")
            await self._change_erequest()
            await self.upload_attachment()
            await self.jira_create_req(
                desc=f"Пользователь {self.user.get('email')} создал задачу по сдаче оборудования\\n{self.obj_link(self.item)}\\nБланк {self.obj_link(self.ereq)}",
                component="iPad",
            )
            await self.jira_add_attachment()
            await self.hw_user_update()
            # End!
            self.logger.info(f"{self.operation_id}: Оборудование успешно сдано {self.obj_link(self.item)}")
            return {"result": "ok", "error": ""}
        except (JiraError, InsightError) as e:
            self.logger.error(f"{self.operation_id}: {e}")
            return {"result": "", "error": str(e)}

    async def _validate(self) -> None:
        self._check_ereq()
        await self._check_user()

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
            await self._insight_inv_client.update_object(
                type_id=78,
                object_id=self.ereq.get("id"),
                attrs={
                    819: f"[{itreq}][{inv}] {self.item['label']}",  # name
                    827: f"{cur_date.day}/{cur_date.month}/{str(cur_date.year)[-2:]}",  # Дата сдачи
                    831: await self.hw_user_id(),  # Кто принял,
                },
            )
            self.logger.info(f"{self.operation_id}: Erequest {self.obj_link(self.ereq)} отредактирован")
        except Exception as e:
            raise InsightError(e)
