import time

import openai


def generate(user, **kwargs):
    print("this is for gpt4")
    openai.api_base = 'https://api.nova-oss.com/v1'
    openai.api_key = 'nv-QcufbFJJPucp91LI4hr2N0V4x0SScIHsbkjdlWvbjWUhyMcx'
    for _ in range(5):
        try:
            response = openai.ChatCompletion.create(
                model='gpt-4-0613',
                messages=[
                    {
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
            time.sleep(10)
