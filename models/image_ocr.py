import requests


def generate(file):
    print("this is caption_daku")
    url = 'https://api.daku.tech/v1/images/interrogations'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer sk-WyEvXylgYH4+XGAsT3BlbkFJWyEvXylgYH4+XGAs'
    }

    files = {
        'file': open(file, 'rb'),
        'model': (None, 'stable-caption'),
    }
    for _ in range(5):
        try:
            response = requests.post(url, headers=headers, files=files)
            res = response.json()
            caption = res['results']['caption']
            print(caption)
            return caption
        except Exception as e:
            print(e, 'retrying')
