import time

import openai
import tiktoken


def generate(messages, model):
    for _ in range(10):
        try:
            for _ in messages:
                contents = messages[_]['content']

            if "gpt-3.5-16k" in model:
                num_tokens = tokens(contents)
                if num_tokens > 16000:
                    new_messages = nova(messages=[{'role': 'system', 'content': "summarize the messages"},
                                                  {'role': 'user', 'content': contents}],
                                        model='gpt-3.5-turbo-16k-0613')
                    messages = [{'role': 'system', 'content': 'Continue from here'},
                                {'role': 'user', 'content': new_messages}]

            elif "gpt-4" in model:
                num_tokens = tokens(contents)
                if num_tokens > 8000:
                    new_messages = nova(messages=[{'role': 'system', 'content': "summarize the messages"},
                                                  {'role': 'user', 'content': contents}],
                                        model='gpt-3.5-turbo-16k-0613')
                    messages = [{'role': 'system', 'content': 'Continue from here'},
                                {'role': 'user', 'content': new_messages}]

            res = nova(messages, model)
            if res is False:
                res = naga(messages, model)
            else:
                return res
            if res is False:
                res = zuki(messages, model)
            else:
                return res
            return res

        except Exception as e:
            print(e, 'retrying in 10 sec')
            time.sleep(10)


def nova(messages, model):
    print("this is for gpt nova")
    openai.api_base = 'https://app.oxyapi.uk/v1'
    openai.api_key = 'oxy-Ap5tjmgYuXwL0lgsNrkO2OJQtT4BmjpNaeUKWax5h9yGm'
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
        print(e)
        return False


def naga(messages, model='gpt-3.5-turbo-16k-0613'):
    print("this is for gpt naga")
    openai.api_base = 'https://api.naga.ac/v1'
    openai.api_key = '_1odz14jRUhEDXaEBU2NHQxl6gaUlX_LsKNR3_cAWW8'
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
        print(e)
        return False


def zuki(messages, model):
    print("this is for zukij")
    openai.api_base = 'https://zukijourney.xyzbot.net'
    openai.api_key = 'zu-90c043196ee79f73789e7cc289aab6f9'
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
        print(e)
        return False


def tokens(message):
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(message))
    print("number of tokens:", num_tokens)
    return num_tokens
