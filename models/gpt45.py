import requests


def generate(messages, model):
    while True:
        headers = {
            'authority': 'chatgpt-vercel-seven-eta.vercel.app',
            'accept': '*/*',
            'content-type': 'text/plain;charset=UTF-8',
            'referer': 'https://chatgpt-vercel-seven-eta.vercel.app/',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        }
        data = {"messages": messages, "temperature": 0.7, "password": "", "model": model}

        res = requests.post('https://chatgpt-vercel-seven-eta.vercel.app/api', headers=headers, json=data)
        if res.status_code == 200:
            res_data = res.text
            print(res_data)
            return res_data
        else:
            pass

