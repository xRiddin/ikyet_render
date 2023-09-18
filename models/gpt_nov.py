import time
import tiktoken
import openai


def generate(sys, user=None):
    print("this is for gpt3.5-nova")
    openai.api_base = 'https://api.nova-oss.com/v1'
    openai.api_key = 'nv-QcufbFJJPucp91LI4hr2N0V4x0SScIHsbkjdlWvbjWUhyMcx'
    num_tokens = tokens(user)
    if num_tokens > 16000:
        new_messages = generate("summarize the messages", user)
        user = new_messages
    for _ in range(5):
        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo-16k-0613',
                messages=[
                    {'role': 'system', 'content': sys},
                    {'role': 'user', 'content': user},
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


def tokens(message):
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(message))
    print("number of tokens:", num_tokens)
    return num_tokens
