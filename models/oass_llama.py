import openai


def gen(user):
    openai.api_key = "_1odz14jRUhEDXaEBU2NHQxl6gaUlX_LsKNR3_cAWW8"
    openai.api_base = "https://chimeragpt.adventblocks.cc/api/v1"
    response = openai.ChatCompletion.create(
        model='oasst-sft-6-llama-30b',
        messages=[
            {'role': 'user', 'content': user},
        ],
        allow_fallback=True
    )
    choices = response['choices']
    res = choices[0]['message']['content']
    return res
