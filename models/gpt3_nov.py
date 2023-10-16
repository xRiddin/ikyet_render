import openai
import time


def generate(sys, user):
    print("this is for gpt3.5-nova")
    openai.api_base = 'https://api.nova-oss.com/v1'
    openai.api_key = 'nv2-jtZwohKYBXLUpoMjeU84_NOVA_v2_0bdZXg16HJqPv7h5KUzB'
    for _ in range(5):
        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo-16k-0613',
                messages=[
                    {
                        'role': 'system', 'content': sys
                    },
                    {
                        'role': 'user', 'content': user
                    }
                ],
                temperature=0.7
            )
            choices = response['choices']
            res = choices[0]['message']['content']
            print(res)
            return res
        except Exception as e:
            print(f'error:{e}, retrying in 20sec')
            time.sleep(10)