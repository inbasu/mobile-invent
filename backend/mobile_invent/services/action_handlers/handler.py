import base64
import time
from abc import ABC, abstractmethod
from logging import getLogger
from typing import Any

from django.core.exceptions import ValidationError
from django.utils.regex_helper import NonCapture

from services.atlassian_adapters.unit_factory import Formatter, Insight, Interface, Jira, Project

INSIGHT_INTERFACE = Interface.MARS_INSIGHT
JIRA_INTERFACE = Interface.MARS_JIRA


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

    @abstractmethod
    async def _validate(self) -> None:
        """ """

    @staticmethod
    def get_field_by_name(fields: list[dict], name: str):
        for field in fields:
            if field["name"] == name:
                return field
        return {}

    @staticmethod
    def get_label_of_field(field: dict) -> Any:
        return field.get("values", [{}])[0].get("label")

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
        super().__init__(*args, **kwargs)
        self._hw_user_id = None
        self.ereq = self.item.get("joined", [{}])[0]
        self._insight_inv_client = Insight.create(
            interface=INSIGHT_INTERFACE,
            scheme=1,
            formatter=Formatter.ATTRS_IN_LIST,
        )
        self._insight_auth_client = Insight.create(
            interface=INSIGHT_INTERFACE,
            scheme=2,
            formatter=Formatter.ATTRS_IN_LIST,
        )

    async def hw_user_id(self):
        if self._hw_user_id is not None:
            return self._hw_user_id
        return await self._get_user(self.user.get("email"))

    @abstractmethod
    async def _change_erequest(self) -> None:
        """how to update ereq"""

    async def _get_user(self, user_email) -> str | bool:
        try:
            return (
                await self._insight_auth_client.get_objects(
                    iql=f"objectTypeId = 57 AND Email = {user_email}", results=1
                )
            )[0]["id"]
        except (IndexError, KeyError):
            return False

    async def upload_attachment(self):
        self.logger.info(f"{self.operation_id}: К Erequest`у добавлен файл")

    def obj_link(self, obj) -> str:
        return f"https://jirainvent.metro-cc.ru/secure/insight/assets/IN-{obj.get('id')}"

    async def hw_user_update(self) -> None:
        time.sleep(3)
        if await self._insight_auth_client.update_object(
            type_id=8, object_id=self.item["id"], attrs={2427: self.hw_user_id}
        ):
            self.logger.info(f"{self.operation_id}: HWUserUpdate изменено.")
            return None
        self.logger.error(f"{self.operation_id}: HWUserUpdate НЕ изменено.")

    """ Validations """

    async def _check_user(self) -> None:
        if not await self.hw_user_id():
            msg = f"{self.operation_id}: Проблема со сдающим пользователем, очевидно же."
            raise ValidationError(msg)

    def _check_ereq(self) -> None:
        if not self.ereq or self.ereq.get("Дата сдачи", False):
            msg = f"{self.operation_id}: Нет открытого Erequest'а для {self.item['label']}"
            raise ValidationError(msg)


class JiraHandler(Handler):
    metro_team: str = "FLS"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._jira_client = Jira.create(interface=JIRA_INTERFACE, project=Project.ITREQ)
        self._issue = ""

    @property
    def issue(self):
        if not self._issue:
            raise ValueError("Нет реквеста в Jira")
        return self._issue

    @issue.setter
    def issue(self, issue):
        if issue:
            self.issue = issue

    async def jira_create_req(self, component, desc) -> None:
        jreq = await self._jira_client.create_issue(
            summary=f"{self.action} мобильного оборудования ТЦ",
            description=desc,
            fields={"mteam": self.metro_team, "components": component},
        )
        if not jreq.startswith("IT-"):
            self.logger.error(f"{self.operation_id}: Произошла ошибка при создании заявки в Jira")
            raise JiraError("Произошла ошибка при создании заявки в Jira")
        self.issue = jreq
        self.logger.info(f"{self.operation_id}: Заявка https://jira.metro-cc.ru/browse/{jreq} создана")

    async def jira_comment(self, comment: str) -> None:
        if not await self._jira_client.comment_issue(issue=self.issue, comment=comment):
            self.logger.error(f"{self.operation_id}: Ошибка комментирования заявки.")
            raise JiraError("{self.operation_id}: Проблема коментировании реквеста в Jira")
        self.logger.warning(f"{self.operation_id}: Заявка {self.issue} прокоментрованна.")

    async def jira_add_attachment(self) -> None:
        if self.file is None and self._issue:
            self.logger.error(f"{self.operation_id}: Пейн я файла не чувствую, потому что его нет Буба!")
        source = base64.b64encode(self.file.read()).decode("utf-8")
        if not await self._jira_client.upload_attachment(issue=self.issue, file_name=self.file.name, file=source):
            self.logger.error(f"{self.operation_id}: Ошибка добавления файла к заявке")
            raise JiraError("{self.operation_id}: Проблема при добавлении к Jira реквесту файла")
        self.logger.info(f"{self.operation_id}: Файл {self.file.name} добавлен к заявке")

    def _get_component(self, component):
        """Сделать enum"""
        {
            "ipad": "iPad",
            "laptop": "Laptop",
        }.get(component, "")

    """ Validations """

    def _issue_validation(self) -> None:
        pass
