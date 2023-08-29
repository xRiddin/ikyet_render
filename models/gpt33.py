import time
import tiktoken
import openai


def generate(sys, user, **kwargs):
    print("this is for gpt3.5-nova")
    messages = []
    messages.append(user)
    openai.api_base = 'https://api.nova-oss.com/v1'
    openai.api_key = 'nv-QcufbFJJPucp91LI4hr2N0V4x0SScIHsbkjdlWvbjWUhyMcx'
    num_tokens = tokens(', '.join(messages))
    if num_tokens > 16000:
        new_messages = generate("summarize the messages", messages)
        messages.clear()
        messages.append(new_messages)
    for _ in range(5):
        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo-16k-0613',
                messages=[
                    {
                     'role': 'user', 'content': sys + ', '.join(messages)},
                ],
                temperature=0.7
            )
            choices = response['choices']
            res = choices[0]['message']['content']
            messages.append(res)
            messages.reverse()
            print(res)
            print(messages)
            return res
        except Exception as e:
            print(f'error:{e}, retrying in 20sec')
            time.sleep(10)


def tokens(message):
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(message))
    print("number of tokens:", num_tokens)
    return num_tokens
