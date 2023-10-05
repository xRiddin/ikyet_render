token = 'sk-WyEvXylgYH4+XGAsT3BlbkFJWyEvXylgYH4+XGAs'

import time
import openai


def generate(messages, model):
    print("this is for gpt_daku")
    openai.api_base = 'https://api.daku.tech/v1'
    openai.api_key = 'sk-WyEvXylgYH4+XGAsT3BlbkFJWyEvXylgYH4+XGAs'

    for _ in range(5):
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=0.7
            )
            choices = response['choices']
            res = choices[0]['message']['content']
            print(res)
            return res
        except Exception as e:
            print(f'error:{e}, retrying in 20sec')
            time.sleep(10)

print(generate([{'role': 'user', 'content': 'hi'}], ""))