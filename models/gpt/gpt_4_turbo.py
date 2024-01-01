import openai

openai.api_base = 'https://app.oxyapi.uk/v1'
openai.api_key = 'oxy-Ap5tjmgYuXwL0lgsNrkO2OJQtT4BmjpNaeUKWax5h9yGm'
response = openai.ChatCompletion.create(
        model='gpt-4-1106-preview',
        messages=[
            {
                'role': 'system', 'content': 'assistant'
            },
            {
                'role': 'user', 'content': 'hi'
            }
        ],
    )
choices = response['choices']
print(choices)
res = choices[0]['message']['content']
print(res)