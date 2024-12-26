import requests


class Mars:
    url: str = ''

    @classmethod
    def get_items(cls, iql: str):
        resp = requests.post(f'{cls.url}/api/insight/iql', data={"scheme": 1, "iql": iql})
        if resp.status_code == 200:
            return resp.json()
        return {}
