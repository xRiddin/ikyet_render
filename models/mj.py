import re

import aiohttp


async def mj(prompt, websocket):
    cookies = {
        'sb-bjbdsdwatviaxduylrdq-auth-token': '%5B%22eyJhbGciOiJIUzI1NiIsImtpZCI6ImQ4STRQOFppVVRWV25NaUwiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNjk1MjcxNzI3LCJpYXQiOjE2OTUxODUzMjcsImlzcyI6Imh0dHBzOi8vYmpiZHNkd2F0dmlheGR1eWxyZHEuc3VwYWJhc2UuY28vYXV0aC92MSIsInN1YiI6ImQ0ZTNiMmUzLWI2ODUtNGQ3Zi1iNzAwLTg2NDFiZjU3Y2ViNCIsImVtYWlsIjoicmVnYXIzNDc4OUB1dHdva28uY29tIiwicGhvbmUiOiIiLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJlbWFpbCIsInByb3ZpZGVycyI6WyJlbWFpbCJdfSwidXNlcl9tZXRhZGF0YSI6e30sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoicGFzc3dvcmQiLCJ0aW1lc3RhbXAiOjE2OTUxODUzMjd9XSwic2Vzc2lvbl9pZCI6ImY4MmE1MjM3LWU4Y2UtNDA4Yy05ZWI5LTdhM2UxZTYwYzMyYSJ9.FHDMWtrElFDEB2r7RA_d6kAZak-yaUW3yrBqBD5h4cA%22%2C%22lxoOQsZPrTgxz2LGlVUKBQ%22%2Cnull%2Cnull%2Cnull%5D',
        'cf_clearance': 'yP3ypG2w0aqKltPvxL72W2ggLxFk0YcAICrK3N60nOE-1691774586-0-1-1a7d5828.2ea11aa9.4667b4e9-0.2.1691774586',
    }

    headers = {
        'authority': 'chat10.fastgpt.me',
        'accept': 'text/event-stream',
        'accept-language': 'en-GB,en;q=0.9',
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6ImQ4STRQOFppVVRWV25NaUwiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNjk1MjcxNzI3LCJpYXQiOjE2OTUxODUzMjcsImlzcyI6Imh0dHBzOi8vYmpiZHNkd2F0dmlheGR1eWxyZHEuc3VwYWJhc2UuY28vYXV0aC92MSIsInN1YiI6ImQ0ZTNiMmUzLWI2ODUtNGQ3Zi1iNzAwLTg2NDFiZjU3Y2ViNCIsImVtYWlsIjoicmVnYXIzNDc4OUB1dHdva28uY29tIiwicGhvbmUiOiIiLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJlbWFpbCIsInByb3ZpZGVycyI6WyJlbWFpbCJdfSwidXNlcl9tZXRhZGF0YSI6e30sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoicGFzc3dvcmQiLCJ0aW1lc3RhbXAiOjE2OTUxODUzMjd9XSwic2Vzc2lvbl9pZCI6ImY4MmE1MjM3LWU4Y2UtNDA4Yy05ZWI5LTdhM2UxZTYwYzMyYSJ9.FHDMWtrElFDEB2r7RA_d6kAZak-yaUW3yrBqBD5h4cA',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        # 'cookie': 'sb-bjbdsdwatviaxduylrdq-auth-token=%5B%22eyJhbGciOiJIUzI1NiIsImtpZCI6ImQ4STRQOFppVVRWV25NaUwiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNjk1MjcxNzI3LCJpYXQiOjE2OTUxODUzMjcsImlzcyI6Imh0dHBzOi8vYmpiZHNkd2F0dmlheGR1eWxyZHEuc3VwYWJhc2UuY28vYXV0aC92MSIsInN1YiI6ImQ0ZTNiMmUzLWI2ODUtNGQ3Zi1iNzAwLTg2NDFiZjU3Y2ViNCIsImVtYWlsIjoicmVnYXIzNDc4OUB1dHdva28uY29tIiwicGhvbmUiOiIiLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJlbWFpbCIsInByb3ZpZGVycyI6WyJlbWFpbCJdfSwidXNlcl9tZXRhZGF0YSI6e30sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoicGFzc3dvcmQiLCJ0aW1lc3RhbXAiOjE2OTUxODUzMjd9XSwic2Vzc2lvbl9pZCI6ImY4MmE1MjM3LWU4Y2UtNDA4Yy05ZWI5LTdhM2UxZTYwYzMyYSJ9.FHDMWtrElFDEB2r7RA_d6kAZak-yaUW3yrBqBD5h4cA%22%2C%22lxoOQsZPrTgxz2LGlVUKBQ%22%2Cnull%2Cnull%2Cnull%5D; cf_clearance=xaHj.X__pbxcx7Yt8Kjkh5x1k6bfgNGyXrEQbRtpi90-1695194634-0-1-cb54fb7a.2e5325a7.9c55a49a-250.2.1695194634',
        'origin': 'https://chat10.fastgpt.me',
        'plugins': '2',
        'pragma': 'no-cache',
        'referer': 'https://chat10.fastgpt.me/',
        'sec-ch-ua': '"Brave";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'usesearch': 'false',
        'x-requested-with': 'XMLHttpRequest',
    }

    json_data = {
        'messages': [
            {
                'role': 'user',
                'content': {prompt},
            },
        ],
        'stream': True,
        'model': 'gpt-3.5-turbo',
        'temperature': 0.5,
        'presence_penalty': 0,
        'credentials': 'include',
        'withCredentials': True,
    }
    mj_id = 0

    async with aiohttp.ClientSession() as session:
        response = await session.post('https://chat10.fastgpt.me/api/command', cookies=cookies, headers=headers,
                                      json=json_data, stream=True)
        async for line in response.content.iter_chunked(1024):
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith('data:') and 'result' in decoded_line:
                    jline = decoded_line
                    print(jline)
                    jstring = re.search(r'.*result\\":\\"(\d+)\\".*', jline)
                    mj_id = int(jstring.group(1))
                handle_event(decoded_line)

    header = {
        'authority': 'bjbdsdwatviaxduylrdq.supabase.co',
        'accept': 'application/vnd.pgrst.object+json',
        'accept-language': 'en-GB,en;q=0.9',
        'accept-profile': 'public',
        'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJqYmRzZHdhdHZpYXhkdXlscmRxIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODQ0MTgwOTAsImV4cCI6MTk5OTk5NDA5MH0.kmZD6NmvcF522MgYH0KWf6VQcoXdAGfLMFpQS7pW2HE',
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6ImQ4STRQOFppVVRWV25NaUwiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNjk1MjcxNzI3LCJpYXQiOjE2OTUxODUzMjcsImlzcyI6Imh0dHBzOi8vYmpiZHNkd2F0dmlheGR1eWxyZHEuc3VwYWJhc2UuY28vYXV0aC92MSIsInN1YiI6ImQ0ZTNiMmUzLWI2ODUtNGQ3Zi1iNzAwLTg2NDFiZjU3Y2ViNCIsImVtYWlsIjoicmVnYXIzNDc4OUB1dHdva28uY29tIiwicGhvbmUiOiIiLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJlbWFpbCIsInByb3ZpZGVycyI6WyJlbWFpbCJdfSwidXNlcl9tZXRhZGF0YSI6e30sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoicGFzc3dvcmQiLCJ0aW1lc3RhbXAiOjE2OTUxODUzMjd9XSwic2Vzc2lvbl9pZCI6ImY4MmE1MjM3LWU4Y2UtNDA4Yy05ZWI5LTdhM2UxZTYwYzMyYSJ9.FHDMWtrElFDEB2r7RA_d6kAZak-yaUW3yrBqBD5h4cA',
        'cache-control': 'no-cache',
        'origin': 'https://chat10.fastgpt.me',
        'pragma': 'no-cache',
        'referer': 'https://chat10.fastgpt.me/',
        'sec-ch-ua': '"Brave";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'x-client-info': '@supabase/auth-helpers-nextjs@0.7.2',
    }

    while True:
        async with aiohttp.ClientSession() as session:
            respons = await session.get(
                f'https://bjbdsdwatviaxduylrdq.supabase.co/rest/v1/user_mj_tasks?select=*&id=eq.{mj_id}',
                headers=header, )
            db = await respons.json()
            status = db['status']
            if status == 'SUCCESS':
                img = db['imageurl']
                print(img)
                return img
            else:
                print(db['imageurl'])
                await websocket.send_json({'type': 'links'})
                pass


def handle_event(event_data):
    print(event_data)
