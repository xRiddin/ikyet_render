import requests


async def yt(link, websockets, is_whisper=False):
    video_id = getVideoId(link)
    i = [
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXRhaWxzIjp7ImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9mb3llci13b3JrIiwiYXVkIjoiZm95ZXItd29yayIsImF1dGhfdGltZSI6MTY5MjY0NDM4MSwidXNlcl9pZCI6Ik5LVUx5TG0xQlZNVTVJcW9ibTA1dUlwWEV4UzIiLCJzdWIiOiJOS1VMeUxtMUJWTVU1SXFvYm0wNXVJcFhFeFMyIiwiaWF0IjoxNjkyNjQ0MzgxLCJleHAiOjE2OTI2NDc5ODEsImVtYWlsIjoibWVrZWxhYzUzNkBjd3RhYS5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsibWVrZWxhYzUzNkBjd3RhYS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9LCJ1aWQiOiJOS1VMeUxtMUJWTVU1SXFvYm0wNXVJcFhFeFMyIn0sImlhdCI6MTcwMDkyNzgyNywiZXhwIjoxNzA2MTExODI3fQ.FdSrqT0zgFuq56H6QMro9KkRb1d431S3nkVX4DZNDa0']
    for _ in i:
        resp = requests_yt(video_id, _, is_whisper)
        print(resp)
        if resp['status'] == 'error':
            print(resp['error'])
        if resp['status'] == 'warning':
            print(resp['warning'])
            resp = requests_yt(video_id, _, "true")
            while True:
                if resp['status'] == 'success':
                    summary = resp['data']['summary']
                    print(summary)
                    await websockets.send_json({'type': 'output', 'output': " ✅Summary of the YouTube Video:"})
                    for topics in summary:
                        title = topics['content']
                        await websockets.send_json({'type': "logs", 'output': '## ' + title})
                        content = topics['explaination']
                        for points in content:
                            print("-" + points)
                            await websockets.send_json({'type': "logs", 'output': '- ' + points})
                        print("heading:", title)
                    return
                elif resp['usage']['batches']['queriesConsumed'] == 0:
                    print("working but error")
                    await websockets.send_json({'type': 'output', 'output': "ERROR ‼️ upload a lengthy video or other video.."})
                    break
                else:
                    resp = requests_yt(video_id, _, "true")
        elif resp['usage']['batches']['queriesConsumed'] == 0:
            print("working but error")
            await websockets.send_json({'type': 'output', 'output': "ERROR ‼️ upload a lengthy video or other video.."})
            break
        else:
            if resp['status'] == 'success':
                summary = resp['data']['summary']
                print(summary)
                await websockets.send_json({'type': 'output', 'output': " ✅Summary of the YouTube Video:"})
                for topics in summary:
                    title = topics['content']
                    await websockets.send_json({'type': "logs", 'output': '## ' + title})
                    content = topics['explaination']
                    for points in content:
                        print("-" + points)
                        await websockets.send_json({'type': "logs", 'output': '- ' + points})
                    print("heading:", title)
                return


def requests_yt(video_id, _, is_whisper=False):
    headers = {
        'authority': 'merlin-uam-yak3s7dv3a-uw.a.run.app',
        'accept': '*/*',
        'accept-language': 'en-GB,en;q=0.6',
        'authorization': f'Bearer {_}',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://www.youtube.com',
        'pragma': 'no-cache',
        'referer': 'https://www.youtube.com/',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-model': '"Nexus 5"',
        'sec-ch-ua-platform': '"Android"',
        'sec-ch-ua-platform-version': '"6.0"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'x-merlin-version': 'extension-6.7.0',
    }

    json_data = {
        'language': 'AUTO',
        'useCache': False,
        'videoId': video_id,
        'estimatedQueryCost': 1,
        'isWhisper': is_whisper,
    }

    response = requests.post(
        'https://merlin-uam-yak3s7dv3a-uw.a.run.app/summarize/youtube?&customJWT=true',
        headers=headers,
        json=json_data,
    )
    resp = response.json()
    return resp



def getVideoId(youtube_link):
    video_id = youtube_link.split("v=")
    if len(video_id) > 1:
        return video_id[1]
    video_id = youtube_link.split("youtu.be/")
    if len(video_id) > 1:
        return video_id[1]

    raise Exception("Unable to find video id")
