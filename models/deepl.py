import random
import time
import requests


def deepl(text, target_lang='EN'):
    headers = {
        'authority': 'www2.deepl.com',
        'accept': '*/*',
        'accept-language': 'en-GB,en;q=0.6',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://www.deepl.com',
        'pragma': 'no-cache',
        'referer': 'https://www.deepl.com/',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    }

    params = {
        'method': 'LMT_handle_jobs',
    }

    json_data = {
        'jsonrpc': '2.0',
        'method': 'LMT_handle_jobs',
        'params': {
            'jobs': [
                {
                    'kind': 'default',
                    'sentences': [
                        {
                            'text': text,
                            'id': 1,
                            'prefix': '',
                        },
                    ],
                    'raw_en_context_before': [],
                    'raw_en_context_after': [],
                    'preferred_num_beams': 4,
                    'quality': 'fast',
                },
            ],
            'lang': {
                'target_lang': target_lang,
                'preference': {
                    'weight': {
                        'DE': 1.2058,
                        'EN': 21.41759,
                        'ES': 0.20962,
                        'FR': 2.18838,
                        'IT': 0.21424,
                        'JA': 0.05172,
                        'NL': 0.31977,
                        'PL': 0.35582,
                        'PT': 0.12458,
                        'RU': 0.04911,
                        'ZH': 0.23828,
                        'BG': 0.03386,
                        'CS': 0.17691,
                        'DA': 0.15404,
                        'EL': 0.03648,
                        'ET': 0.09162,
                        'FI': 0.0983,
                        'HU': 0.1312,
                        'LT': 0.10407,
                        'LV': 0.09558,
                        'RO': 0.10284,
                        'SK': 0.12179,
                        'SL': 1.11206,
                        'SV': 0.14108,
                        'TR': 0.08438,
                        'ID': 0.08331,
                        'UK': 0.0416,
                        'KO': 0.04433,
                        'NB': 0.13021,
                    },
                    'default': 'default',
                },
                'source_lang_user_selected': 'EN',
            },
            'priority': -1,
            'commonJobParams': {
                'mode': 'translate',
                'textType': 'plaintext',
                'browserType': 1,
            },
            'timestamp': int(time.time() * 1000),
        },
        'id': random.Random().randint(10000000, 99999999)
    }

    response = requests.post('https://www2.deepl.com/jsonrpc', params=params, headers=headers, json=json_data)
    print(response)
    resp = response.json()
    print(resp)

deepl("hallo, wie geht es dir?")