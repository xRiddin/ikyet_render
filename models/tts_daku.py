import requests
import time
token = 'sk-WyEvXylgYH4+XGAsT3BlbkFJWyEvXylgYH4+XGAs'


def generate(message, model='voice-patrick'):
    print("this is for tts_daku")
    url = 'https://api.daku.tech/v1/audio/speech'
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json'
    }
    json_data = {
        'input': message,
        'model': model,
    }
    for _ in range(5):
        try:
            response = requests.post(url, headers=headers, json=json_data)
            res = response.json()
            link = res['url']
            print(link)
            return link
        except Exception as e:
            print(f'error:{e}, retrying in 10 sec')
            time.sleep(10)
