import json

import requests
from django.http import HttpResponse, JsonResponse
from django.views import View

from .services.blanks.worddocument import WordDocument


# Create your views here.
class GetDeviceListView(View):
    def post(self, request) -> JsonResponse:
        res = requests.post('http://127.0.0.1:8000/iql/join', 
                            json={
                                "scheme":1, 
                                "iql": 'objectTypeId=8 AND Type IN ("LAPTOP", "WIRELESS HANDHELD") AND Store in (1014)', 
                                'joined_iql': 'objectTypeId=78', 
                                'on':'Инв No и модель',
                                })
        if res.status_code == 200:
            return JsonResponse(res.json(), safe=False)
        return JsonResponse([], safe=False)




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
