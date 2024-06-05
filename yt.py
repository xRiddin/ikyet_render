import requests


async def yt(link, websockets, is_whisper=False):
    video_id = getVideoId(link)
    i = [
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXRhaWxzIjp7InJvbGUiOiJmcmVlIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2ZveWVyLXdvcmsiLCJhdWQiOiJmb3llci13b3JrIiwiYXV0aF90aW1lIjoxNzA2ODUyMDIxLCJ1c2VyX2lkIjoibjB1cE9DRVlrbmhhT3RlanAxVmxhNm5HNVpEMiIsInN1YiI6Im4wdXBPQ0VZa25oYU90ZWpwMVZsYTZuRzVaRDIiLCJpYXQiOjE3MDY4NTIwOTksImV4cCI6MTcwNjg1NTY5OSwiZW1haWwiOiJwYXIudG9uLmcubG8uYi5hQGdvb2dsZW1haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsicGFyLnRvbi5nLmxvLmIuYUBnb29nbGVtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn0sInVpZCI6Im4wdXBPQ0VZa25oYU90ZWpwMVZsYTZuRzVaRDIifSwiaWF0IjoxNzE3MzM0NjAyLCJleHAiOjE3MjI1MTg2MDJ9.WRrBslRWL7gXWHXebAqVgjxtlgXQ45Pj2MAHbXO4PRM']
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
        'https://uam.getmerlin.in/summarize/youtube?&customJWT=true',
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
