import time

import openai
import tiktoken

#from ..llama2 import generate as g


def generate(sys, user):
    for _ in range(10):
        try:
            num_tokens = tokens(user)
            if num_tokens > 16000:
                new_messages = oxy("summarize the messages", user)
                user = new_messages
            """
            if num_tokens < 20:
                print("this is llama 70b")
                return g(sys, user)
            """
            res = oxy(sys, user)
            if res:
                break
            else:
                res = ai(sys, user)
                if res:
                    break
                else:
                    res = zuki(sys, user)
                    if res:
                        break
                    else:
                        res = naga(sys, user)
                        if res:
                            break
                        else:
                            print(e, 'retrying in 10 sec')
                            time.sleep(10)
        except Exception as e:
            print(e, 'retrying in 10 sec...')
            time.sleep(10)
    return res


def oxy(sys, user):
    print("this is for gpt oxy")
    openai.api_base = 'https://app.oxyapi.uk/v1'
    openai.api_key = 'oxy-Ap5tjmgYuXwL0lgsNrkO2OJQtT4BmjpNaeUKWax5h9yGm'
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-16k',
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
        print(e, "oxy failed")
        return False


def ai(sys, user):
    print("this is for gpt ai")
    openai.api_key = 'ht-7x7HDwTJJAR7j678m9B5nnK4uHOuiuTnvAd5NkgyfAhqFmbN'
    openai.api_base = 'https://api.hentaigpt.xyz/v1'
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-16k',
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
        print(e)
        return False


def naga(sys, user):
    print("this is for gpt naga")
    openai.api_base = 'https://api.naga.ac/v1'
    openai.api_key = '_1odz14jRUhEDXaEBU2NHQxl6gaUlX_LsKNR3_cAWW8'
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-0613',
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
        print(e)
        return False


def zuki(sys, user):
    print("this is for zukij")
    openai.api_base = 'https://zukijourney.xyzbot.net'
    openai.api_key = 'zu-90c043196ee79f73789e7cc289aab6f9'
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
        print(e)
        return False


def tokens(message):
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(message))
    print("number of tokens:", num_tokens)
    return num_tokens
