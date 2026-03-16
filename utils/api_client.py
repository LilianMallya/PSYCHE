import requests
import config

class APIClient:
   

    HF_API_URL = "https://api-inference.huggingface.co/models/"

    def __init__(self):
        self.headers = {"Authorization": f"Bearer {config.HUGGINGFACE_API_KEY}"}

    def call_huggingface(self, model: str, text: str):
        url = self.HF_API_URL + model
        try:
            resp = requests.post(url, headers=self.headers, json={"inputs": text[:512]}, timeout=25)
            if resp.status_code == 200:
                return resp.json()
            return None
        except Exception:
            return None
