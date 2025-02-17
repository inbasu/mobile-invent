import base64
import time
from abc import ABC, abstractmethod
from logging import getLogger
from typing import Any

from mobile_invent.views import INTERFACE
from services.atlassian_adapters.insight.unit import InsightMetroUnit
from services.atlassian_adapters.jira.unit import JiraMetroUnit
from services.atlassian_adapters.unit_factory import Formatter, Insight, Interface


class InsightError(Exception):
    pass


class JiraError(Exception):
    pass


class Handler(ABC):
    logger = getLogger("mobile")
    action: str

    def __init__(self, operation_id, item, user, store, file, code) -> None:
        self.operation_id = operation_id
        self.store = store
        self.user = user
        """  """
        self.item = item
        self.file = file
        self.code = code

    @abstractmethod
    async def handle(self) -> dict:
        """Самый глваный метод =)"""

    @staticmethod
    def get_field_by_name(fields: list[dict], name: str):
        for field in fields:
            if field["name"] == name:
                return field
        return {}

    @staticmethod
    def get_label_of_field(field: dict) -> Any:
        return field.get("values", [{}])[0].get("label")

    @staticmethod
    def hw_user_update(func):
        async def wrapper(self, *args, **kwargs):
            if user_id := self.hw_user_id:
                Handler.logger.info(f"{self.operation_id}: {self.action} {self.item['label']} {self.user['email']}")
                update = func(self, *args, **kwargs)
                if not update.get("error", False):
                    time.sleep(3)
                    client = Insight.create(interface=INTERFACE, scheme=1, formatter=Formatter.ATTRS_IN_LIST)
                    await client.update_object(type_id=8, object_id=self.item["id"], attrs={2427: [user_id]})
                return update
            return {}

        return wrapper

    @classmethod
    def zip_it(cls, main: list[dict], joined: list[dict], on: str) -> list:
        if main and joined:
            for obj in main:
                obj["joined"] = []
                for rel in joined:
                    is_main = {r["id"] for r in cls.get_field_by_name(rel["attrs"], on).get("values", [])}
                    if obj["id"] in is_main:
                        obj["joined"].append(rel)
        return main

    """ полделить нижнюю логику на 2 класса """


class InsightHandler(Handler):
    def __init__(self, *args, **kwargs) -> None:
        self._insight_inv_client = Insight.create(interface=INTERFACE, scheme=1, formatter=Formatter.ATTRS_IN_LIST)
        self._insight_auth_client = Insight.create(interface=INTERFACE, scheme=2, formatter=Formatter.ATTRS_IN_LIST)
        super().__init__(self, *args, **kwargs)

    @abstractmethod
    async def _change_erequest(self) -> None:
        """how to update ereq"""

    @property
    async def hw_user_id(self) -> str:
        return await self.get_user(self.user.get("email"))

    async def get_user(self, user_email) -> str:
        try:
            return (
                await self._insight_auth_client.get_objects(
                    iql=f"objectTypeId = 57 AND Email = {user_email}", results=1
                )
            )[0]["id"]
        except (IndexError, KeyError):
            raise InsightError("Проблема с пользователем.")

    async def insight_add_attachment(self):
        self.logger.info(f"{self.operation_id}: К Erequest`у добавлен файл")

    def obj_link(self, obj) -> str:
        return f"https://jirainvent.metro-cc.ru/secure/insight/assets/IN-{obj.get('id')}"


class JiraHandler(Handler):
    _jira_client: JiraMetroUnit

    async def jira_create_req(self, component):
        jreq = await self._jira_client.create_issue(
            summary=f"{self.action} мобильного оборудования ТЦ",
            description="f'пользователь {self.user.get('email')} создал задачу по сдаче оборудования\n{self.obj_link(self.item)}\nБланк {self.obj_link(self.ereq)}'",
            fields={"mteam": "FLS", "components": component},
        )
        if jreq.startswith("IT-"):
            self.logger.info(f"{self.operation_id}: Заявка https://jira.metro-cc.ru/browse/{123} создана")
            return jreq
        self.logger.error(f"{self.operation_id}: Произошла ошибка при создании заявки в Jira")
        raise JiraError("Произошла ошибка при создании заявки в Jira")

    async def jira_add_attachment(self, itreq):
        if self.file is None:
            self.logger.error(f"{self.operation_id}: Пейн я файла не чувствую, потому что его нет Буба!")
        source = base64.b64encode(self.file.read()).decode("utf-8")
        if await self._jira_client.upload_attachment(issue=itreq, file_name=self.file.name, file=source):
            self.logger.info(f"{self.operation_id}: Файл {self.file.name} добавлен к заявке")
            return None
        self.logger.error(f"{self.operation_id}: Ошибка добавления файла к заявке")
        raise JiraError("{self.operation_id}: Проблема при добавлении к Jira реквесту файла")

    def _get_component(self, component):
        """Сделать enum"""
        {
            "ipad": "iPad",
            "laptop": "Laptop",
        }.get(component, "")
