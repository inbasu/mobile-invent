import json
import re

import requests
from django.http import HttpResponse, JsonResponse
from django.views import View

from .services.blanks.worddocument import WordDocument

USER = {
        "username": "ivan.fisenko",
        "roles": ["MCC_RU_INSIGHT_IT_ROLE"],
        "store_role": ["1074"]
        }


# Create your views here.
class GetDeviceListView(View):
    def post(self, request) -> JsonResponse:
        user = USER
        
        stores = ' ,'.join(user["store_role"])
        if stores:
            insight_data = requests.post('http://127.0.0.1:8000/iql/join', 
                            json={
                                "scheme":1, 
                                "iql": f'objectTypeId=8 AND Type IN ("LAPTOP", "WIRELESS HANDHELD") AND Store in ({stores})', 
                                'joined_iql': 'objectTypeId=78', 
                                'on':'Инв No и модель',
                                })
            if insight_data.status_code == 200:
                return JsonResponse(self.zip_it(insight_data.json(), []), safe=False)
        return JsonResponse([], safe=False)

    def zip_it(self, insight_data: list[dict], jira_data: list[dict]) -> list:
        for item in insight_data:
            numbers = [attr["values"][0]["label"] for attr in item["attrs"] if attr["name"] in {"Serial No", "INV No"}]
            for idx, req in enumerate(jira_data):
                item_no = self.get_item_number(req.get('fields', {}).get('customfield_13400', '')) # 13400 поле inv.
                if item_no in numbers:
                    item["itreq"] = {
                            "Key": req.get('key',''),
                            "For user": req.get('fields', {}).get('customfield_13004', ''),
                            "Issue Location" : req.get('fields', {}).get('customfield_10702', ''),
                            "inv.": req.get('fields', {}).get('customfield_13400', ''),
                            }
                    jira_data.pop(idx)
                    break
        
        return insight_data + [{
            "id": 0,
            "label": '',
            "attrs": [],
            "joined": [],
            "itreq": {
                "Key": req.get('key', ''),
                "For user": req.get('fields', {}).get('customfield_13004', ''),
                "Issue Location" : req.get('fields', {}).get('customfield_10702', ''),
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




def get_field_by_name(fields: list[dict], name: str):
    for field in fields:
        if field["name"] == name:
            return field
    return {}
