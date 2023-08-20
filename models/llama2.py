import requests


def generate(sys, user, *args):
    headers = {
        'content-type': 'application/json',
        'referer': 'https://replicate.com/replicate/llama-2-70b-chat',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    }
    json_data = {
        'inputs': {
            'top_k': 250,
            'top_p': 1,
            'temperature': 0.5,
            'system_prompt': sys,
            'max_new_tokens': 1000,
            'min_new_tokens': -1,
            'repetition_penalty': 1,
            'repetition_penalty_sustain': 256,
            'token_repetition_penalty_decay': 128,
            'prompt': user,
        },
    }
    response = requests.post(
        'https://replicate.com/api/models/replicate/llama-2-70b-chat/versions/2c1608e18606fad2812020dc541930f2d0495ce32eee50074220b87300bc16e1/predictions',
        headers=headers,
        json=json_data,
    )
    resp = response.json()
    uuid = resp['uuid']
    print(uuid)
    while True:
        respon = requests.get(
            f'https://replicate.com/api/models/replicate/llama-2-70b-chat/versions/2c1608e18606fad2812020dc541930f2d0495ce32eee50074220b87300bc16e1/predictions/{uuid}')
        respp = respon.json()
        data = respp['prediction']['status']
        if data == "processing":
            print(data)
        else:
            print(data)
            output = respp['prediction']['output']
            out = ''.join(output)
            print(out)
            return out
