import aiohttp


async def generate_response(system, user, *args):
    urls = ['https://free.churchless.tech/v1/chat/completions', 'https://api4.gravityengine.cc/v1/chat/completions',
            'https://ai.chatgpt.org.uk/api/openai/v1/chat/completions',
            'https://gpt4.xunika.uk/api/openai/v1/chat/completions']
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'model': 'gpt-3.5-turbo-16k-0613',
        'temperature': 1,
        'messages': [
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]
    }

    for i in urls:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f'{i}', headers=headers, json=data) as response:
                    res_data = await response.json(content_type='application/json')
                    print(res_data)
                    choices = res_data['choices']
        except Exception as e:
            print(f"error:{e} retrying....")
        else:
            print("this is from generated")
            print(choices[0]['message']['content'])
            return choices[0]['message']['content']
