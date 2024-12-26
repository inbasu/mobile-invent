from .handler import Handler, JiraError


class SendHandler(Handler):
    action = "Пересылка"

    def __init__(self, item, store, code: str, operation_id: str, user, **kwargs) -> None:
        self.operation_id = operation_id
        self.item = item
        self.store = store
        self.code = code

    @Handler.hw_user_update
    def handle(self) -> dict:
        try:
            self.jira_create_req('')
            self.logger.info('')
            self.insight_update_hardware()
            self.logger.info("")
        except JiraError:
            pass
        return {}         

    def insight_update_hardware(self):
        pass



            

