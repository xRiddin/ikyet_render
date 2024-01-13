import openai


def vision(sys, user, url):
    openai.api_base = 'https://app.oxyapi.uk/v1'
    openai.api_key = 'oxy-Ap5tjmgYuXwL0lgsNrkO2OJQtT4BmjpNaeUKWax5h9yGm'
    response = openai.ChatCompletion.create(
            model='gpt-4-vision-preview',
            messages=[
                {
                    'role': 'system', 'content': sys
                },
                {
                    'role': 'user', 'content': [
                    {
                        'type': 'text', 'text': user
                    },
                    {
                        'type': 'image_url',
                        'image_url': {
                            "url": url
                        },
                    },
                ],
                }
            ],
        )
    choices = response['choices']
    print(choices)
    res = choices[0]['message']['content']
    print(res)
    return res