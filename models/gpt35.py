import time

import openai


def generate(system, user, **kwargs):
    openai.api_base = 'https://chimeragpt.adventblocks.cc/api/v1'
    openai.api_key = '_1odz14jRUhEDXaEBU2NHQxl6gaUlX_LsKNR3_cAWW8'
    for _ in range(5):
        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo-16k',
                messages=[
                    {'role': 'system', 'content': system,
                     'role': 'user', 'content': user},
                ],
                temperature=0.2
            )
            choices = response['choices']
            res = choices[0]['message']['content']
            print(res)
            return res
        except Exception as e:
            print(f'error:{e}, retrying in 20sec')
            time.sleep(20)
