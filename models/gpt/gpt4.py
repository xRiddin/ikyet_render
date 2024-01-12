import time

import openai
import tiktoken

#from ..llama2 import generate as g


def generate(sys, user):
    for _ in range(10):
        try:
            num_tokens = tokens(user)
            if num_tokens > 8000:
                new_messages = oxy("summarize the messages", user)
                user = new_messages
            """
            if num_tokens < 10:
                print("this is llama 70b")
                return g(sys, user)
            """
            res = oxy(sys, user)
            if res:
                return res
            else:
                res = mandril(sys, user)
                if res:
                    return res
                else:
                    res = ai(sys, user)
                    if res:
                        return res
                    else:
                        res = zuki(sys, user)
                        if res:
                            return res
                        else:
                            res = naga(sys, user)
                            if res:
                                return res
                            else:
                                print(e, 'retrying in 10 sec')
                                time.sleep(10)
        except Exception as e:
            print(e, 'retrying in 10 sec')
            time.sleep(10)


def generate_response(api_base, api_key, sys, user, model):
    print(f"this is for {api_base}")
    openai.api_base = api_base
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model=model,
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


def oxy(sys, user):
    return generate_response('https://app.oxyapi.uk/v1', 'oxy-Ap5tjmgYuXwL0lgsNrkO2OJQtT4BmjpNaeUKWax5h9yGm', sys, user, 'gpt-4-0314')


def ai(sys, user):
    return generate_response('https://api.hentaigpt.xyz/v1', 'ht-ct93pyy1ukyqcqp8bsalsiptkncmsz1e914k8sm6d77dov', sys, user, 'gpt-4-0314')


def naga(sys, user):
    return generate_response('https://api.naga.ac/v1', '_1odz14jRUhEDXaEBU2NHQxl6gaUlX_LsKNR3_cAWW8', sys, user, 'gpt-3.5-turbo-16k-0613')


def zuki(sys, user):
    return generate_response('https://zukijourney.xyzbot.net', 'zu-90c043196ee79f73789e7cc289aab6f9', sys, user, 'gpt-4')


def mandril(sys, user):
    return generate_response('https://api.mandrillai.tech/v1', 'md-ZawlujQfMIgjbfRFFMnVTUiqGAuOzMAcqufbniKpbWdpzFQA', sys, user, 'gpt-4')

def tokens(message):
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(message))
    print("number of tokens:", num_tokens)
    return num_tokens
