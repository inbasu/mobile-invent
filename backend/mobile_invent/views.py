import json
import re
from logging import getLogger
from uuid import uuid4

import requests
from django.http import HttpResponse, JsonResponse
from django.views import View

from mobile_invent.services.handler import Handler

from .services.blanks.worddocument import WordDocument

logger = getLogger("mobile")


USER = {
        "username": "ivan.fisenko",
        "email": "ivan.fisenko@metro-cc.ru",
        "roles": ["MCC_RU_INSIGHT_IT_ROLE"],
        "store_role": ["1065"]
        }

def get_reqs():
    with open('./itreqs.json', 'r') as f:
        data = json.load(f)
    return data


# Create your views here.
class GetStoresListView(View):
    def post(self, request):
        return JsonResponse(requests.post('http://127.0.0.1:8000/iql', 
                                          json={"scheme": 1, "iql": 'objectTypeId = 16 AND "УНАДРТЦ" IS NOT EMPTY AND "Jira issue location" IS NOT EMPTY'}).json(),
                            safe=False)


class GetDeviceListView(View):
    def post(self, request) -> JsonResponse:
        store =  json.loads(json.loads(request.body.decode("utf-8")).get('store', ''))
        jira_issue_location = Handler.get_field_by_name(store["attrs"], "Jira issue location").get("values", [{}])[0].get("label", '')
        if store and jira_issue_location:
            insight_data = requests.post('http://127.0.0.1:8000/iql/join', 
                            json={
                                "scheme":1, 
                                "iql": f'objectTypeId=8 AND Type IN ("LAPTOP", "WIRELESS HANDHELD") AND Store in ({store["label"]}) AND State IN ("Free", "ApprovedToBeSent", "Working", "Stock OK", "Reserved")', 
                                'joined_iql': 'objectTypeId=78', 
                                'on':'Инв No и модель',
                                })
            jira_data = requests.post("http://127.0.0.1:8000/jql",
                                      json={"jql": f'project = "IT Requests" AND type = "HW/SW Request" AND Hardware in (Laptop, iPad, "Mobile Phone") AND inv. is not EMPTY AND "For user" is not EMPTY AND labels != hwr_done AND status in ("SSS To Do", "Wait Delivery" ) AND "Issue Location" = {jira_issue_location}'})
            if insight_data.status_code == 200:
                return JsonResponse(self.zip_it(insight_data.json(), []), safe=False)
        return JsonResponse([], safe=False)


    def zip_it(self, insight_data: list[dict], jira_data: list[dict]) -> list:
        for item in insight_data:
            numbers = [attr["values"][0]["label"] for attr in item["attrs"] if attr["name"] in {"Serial No", "INV No"}]
            for idx, req in enumerate(jira_data):
                item_no = self.get_item_number(req.get('fields', {}).get('customfield_13400', '')) # 13400 поле inv.
                if item_no in numbers:
                    try:
                        item["itreq"] = {
                            "Key": req.get('key',''),
                            "For user": req.get('fields', {}).get('customfield_13004', {}).get("displayName", ''),
                            "Issue Location" : req.get('fields', {}).get('customfield_10702', {})[0].get("value", ''),
                            "inv.": req.get('fields', {}).get('customfield_13400', ''),
                            }
                        jira_data.pop(idx)
                    finally:
                        break

        
        return insight_data + [{
            "id": 0,
            "label": '',
            "attrs": [],
            "joined": [],
            "itreq": {
                            "Key": req.get('key',''),
                            "For user": req.get('fields', {}).get('customfield_13004', {}).get("displayName", ''),
                            "Issue Location" : req.get('fields', {}).get('customfield_10702', {})[0].get("value", ''),
                            "inv.": req.get('fields', {}).get('customfield_13400', ''),
                            }

            } for req in jira_data]
    
    def get_item_number(self, number: str) -> str:
        if re.findall(r"^\d{6}$|^MCC\d{6}$|^MCC.\d{6}$" ,number.strip().upper()):
            return number.strip()[-6:]
        return number



class DownloadBlank(View):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        action = data.get('action', '')
        hardware = data.get('item', {})
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        if action and hardware:
            item_type = self.check_type(hardware)
            path = f'./mobile_invent/services/blanks/source/{action}/{item_type}.docx'
            data = {
                    "$DEVICE":  Handler.get_field_by_name(hardware['attrs'], "Model").get("values", [])[0].get('label', ''),
                    "$NUMBER": f"{Handler.get_field_by_name(hardware['attrs'], 'Serial No').get("values", [])[0].get('label', '')} / {Handler.get_field_by_name(hardware['attrs'], 'INV No').get("values", [])[0].get('label', '')}",
                    }
            WordDocument(path).change_table(data=data).save(response)
            response["Content-Dispostal"] = 'attachment; filename=document.docx'
        return response


    def check_type(self, item) -> str:
        item_type = Handler.get_field_by_name(item['attrs'], "Model").get("values", [])[0].get('label','').lower()
        if "nokia" in item_type:
            return "nokia"
        elif "ipad" in item_type:
            return "ipad"
        else:
            return Handler.get_field_by_name(item['attrs'], "Type").get("values", [])[0].get("label", '').lower()


class HandleActionView(View):
    http_method_names = ['post']

    def post(self, request):
        data = self.form_data(request)
        operation_id = str(uuid4())[-12:]
        match data["action"]:
            case "takeback":
                # result = TakebackHandler.handle(operation_id=operation_id, **data)
                pass
            case "giveaway":
                result = {1, 2}
            case "send":
                result = {1, 2}
        return JsonResponse(result)



    def form_data(self, request) -> dict:
        action = request.POST.get('action', '')
        item = json.loads(request.POST.get("item", '{}'))
        file = request.FILES.get("blank", '')
        user = request.session.get('user', USER)
        store = request.POST.get('store', '')
        return {'action': action, "item": item, "file": file, "user": user, "store": store}

        


