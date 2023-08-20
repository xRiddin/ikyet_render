import requests


def query(file):
    API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
    headers = {"Authorization": "Bearer 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"}

    with open(file, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    respon = response.json()
    resp = respon[0]
    return resp['generated_text']
