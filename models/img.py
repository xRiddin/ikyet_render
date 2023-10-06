import requests
import time
token = 'sk-WyEvXylgYH4+XGAsT3BlbkFJWyEvXylgYH4+XGAs'


def generate(prompt, model):
    print("this is for img_daku")
    url = 'https://api.daku.tech/v1/images/generations'
    headers = {
        'accept': 'application/json',
        'authorization': f'bearer {token}'
    }
    json = {
        'model': model,
        'n': 1,
        'prompt': prompt,
        'size': '1024x1024'
    }
    for _ in range(5):
        try:
            response = requests.post(url, headers=headers, json=json)
            res = response.json()
            print(res)
            img = res['data'][0]['url']
            print(img)
            return img
        except Exception as e:
            print(f'error:{e}, retrying in 5sec')
            time.sleep(5)
