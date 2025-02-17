import asyncio

from .handler import InsightHandler, JiraError, JiraHandler


class SendHandler(InsightHandler, JiraHandler):
    action = "Пересылка"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(self, *args, **kwargs)

    async def handle(self) -> dict:
        try:
            self.logger.info(f"{self.operation_id}: начат процесс отправки оборудования {self.obj_link(self.item)}")
            await asyncio.gather(
                self.jira_create_req(
                    "ipad",
                    desc=f"Пользователь {self.user.get('email')} создал задачу по сдаче пересылке\n{self.obj_link(self.item)}\nТрек номер: {self.code}",
                ),
                self.update_hardware(),
            )

        except JiraError:
            pass
        return {}

    async def update_hardware(self) -> None:
        if await self._insight_inv_client.update_object(
            type_id=8, object_id=self.item["id"], attrs={214: "Store", 661: 126836, 217: self.code}
        ):
            self.logger.info(f"{self.operation_id}: Оборудование успешно отправленно {self.obj_link(self.item)}")
            return None
        self.logger.error(f"{self.operation_id}: Произошла ошибка в потправке оборудования {self.obj_link(self.item)}")

    async def _change_erequest(self) -> None:
        raise NotImplementedError()
