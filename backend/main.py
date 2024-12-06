
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_methods=["*"])

def get_value(item, name: str) -> dict:
    for attr in item["attrs"]:
        if attr["name"] == name:
            return attr["values"]
    return {}

@app.post('/example/1014')
def get_pack():
    items = requests.post("http://127.0.0.1:8000/iql", 
                          json={
                              "scheme": 1, 
                              "iql": 'objectTypeId = 8 AND Store = 1014 AND Type in ("LAPTOP", "WIRELESS HANDHELD")'
                              })
    ereqs = requests.post("http://127.0.0.1:8000/iql", 
                          json={
                              "scheme": 1, 
                              "iql": 'objectTypeId = 78 AND Store = 1014 AND "Инв No и модель" is not empty'
                              })
    items = items.json()
    for item in items:
        item['ereq'] = {"id": 0}
        for ereq in ereqs.json():
            if  item["ereq"]['id'] < ereq["id"] and item['id'] in [e['id'] for e in get_value(ereq, "Инв No и модель") if e]:
                item['ereq'] = ereq
    return items



