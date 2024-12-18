import json
import re
from uuid import uuid4

import requests
from django.http import HttpResponse, JsonResponse
from django.views import View

from mobile_invent.services.action_handler import ActionHandler

from .services.blanks.worddocument import WordDocument

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
        store =  json.loads(request.body.decode("utf-8")).get('store', '')
        if store:
            insight_data = requests.post('http://127.0.0.1:8000/iql/join', 
                            json={
                                "scheme":1, 
                                "iql": f'objectTypeId=8 AND Type IN ("LAPTOP", "WIRELESS HANDHELD") AND Store in ({store}) AND State IN ("Free", "ApprovedToBeSent", "Working", "Stock OK")', 
                                'joined_iql': 'objectTypeId=78', 
                                'on':'Инв No и модель',
                                })
            if insight_data.status_code == 200:
                jira = get_reqs()
                return JsonResponse(self.zip_it(insight_data.json(), jira), safe=False)
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
                    "$DEVICE":  get_field_by_name(hardware['attrs'], "Model").get("values", [])[0].get('label', ''),
                    "$NUMBER": f"{get_field_by_name(hardware['attrs'], 'Serial No').get("values", [])[0].get('label', '')} / {get_field_by_name(hardware['attrs'], 'INV No').get("values", [])[0].get('label', '')}",
                    }
            WordDocument(path).change_table(data=data).save(response)
            WordDocument(path).change_table(data=data).save("./word.docx")
            response["Content-Dispostal"] = 'attachment; filename=document.docx'
        return response

    def check_type(self, item) -> str:
        item_type = get_field_by_name(item['attrs'], "Model").get("values", [])[0].get('label','').lower()
        if "nokia" in item_type:
            return "nokia"
        elif "ipad" in item_type:
            return "ipad"
        else:
            return get_field_by_name(item['attrs'], "Type").get("values", [])[0].get("label", '').lower()


class HandleActionView(View):
    http_method_names = ['post']

    def post(self, request):
        data = self.form_data(request)
        operation_id = str(uuid4())[-12:]
        # mobile_logger.info(f'{operation_id}: {data.user['email']} {data.action=}')
        res, err = (1, 2)
        match data["action"]:
            case "takeback":
                result = ActionHandler.takeback(operation_id,**data)
            case "giveaway":
                res, err = (1, 2)
            case "send":
                res, err = (1, 2)
        return JsonResponse({"result": res, "error": err})



    def form_data(self, request) -> dict:
        action = request.POST.get('action', '')
        item = json.loads(request.POST.get("item", '{}'))
        file = request.FILES.get("file", '')
        user = request.session.get('user', USER)
        return {'action': action, "item": item, "file": file, "user": user}

        

def get_field_by_name(fields: list[dict], name: str):
    for field in fields:
        if field["name"] == name:
            return field
    return {}
