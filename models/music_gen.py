import os

import requests


def music(prompt, dire):
    tokens = [
        'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZ4amxzNTlibnpzbEI3RlB4b3Y3dyJ9.eyJpc3MiOiJodHRwczovL3N0YWJsZWF1ZGlvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NTA1MjEwZTU2YTYxZjc2MjhkZWQ5NzYiLCJhdWQiOlsiaHR0cHM6Ly9zdGFibGVhdWRpby5jb20iLCJodHRwczovL3N0YWJsZWF1ZGlvLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2OTUwMDg3NDEsImV4cCI6MTY5NTA5NTE0MSwiYXpwIjoiTnJtRkFuN1I5WUV0WkFLaVhqYkg1R2Q5S0hCa1ExMHgiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIG9mZmxpbmVfYWNjZXNzIiwicGVybWlzc2lvbnMiOltdfQ.VBO6YjJiowyHPiEi_rADiYbiv9xIAVvwv1ZuATx-RiDrT3mfbbmxbn4LeuIkFFoPIcsZv5gZmju6EbykRNLnHBHJU1SVbpLs2-IzzrsfXEKXlivN_d_eKZ2-OOnmd-oY6AcxfXCbgJ499_5PZCEXPNqklkSqKde35jE4d7Gp7-eYaSaclmL5r5quh9VDykAdfX8PigbPy_jiMI9O76WV_-gMPlyR85e3zChSHoyaRvdJ_O_3GhEWHD9YtEtYuVVoGNjuwKMVYm2m0M6uiN2NMuFOgHyQ7P2BTyokvfC743OvXX1ySIf7dDpoa2UMhThvHKhDMtCASYopmWoG8v2EPQ',
        'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZ4amxzNTlibnpzbEI3RlB4b3Y3dyJ9.eyJpc3MiOiJodHRwczovL3N0YWJsZWF1ZGlvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NTA1Mjc2NWE2NmU4OGZiM2U4ZGVkOTEiLCJhdWQiOlsiaHR0cHM6Ly9zdGFibGVhdWRpby5jb20iLCJodHRwczovL3N0YWJsZWF1ZGlvLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2OTQ5NjkyNjgsImV4cCI6MTY5NTA1NTY2OCwiYXpwIjoiTnJtRkFuN1I5WUV0WkFLaVhqYkg1R2Q5S0hCa1ExMHgiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIG9mZmxpbmVfYWNjZXNzIiwicGVybWlzc2lvbnMiOltdfQ.lT5XQmaATnzt3ONLb7N_TZtV_PA3-2MeAMG0_vmFilmaFjEjpu-EOl8Aovrd_kry6S7_uoMueFc46t71rk2hNrUQQUZWTJWu7Xc7XvQlQfkKH7KVBDhTaX3giNz1Y46MBOOI8ogDB-AZKIg7MprRj5AYfHNF5ONHNeBU2zI9Q58tN7S5wMPfyqU-C4Fr7-HjvJpVpsoama6hmIZyYUJ6XBogCsYw81k4L2Ey7zMObbxSxPkdzoiGlhZJpy3-DNNlMfolAfs_eHCpBJ4cXRGsnsNiXnOnEoCB-DFc8K13o3L8mGw6MLPOsNa7D8_jFcRnkWnNYocHMhDdx6NUW9ogbw'
    ]
    try:
        for i in tokens:
            headers = {
                'authorization': f'Bearer {i}',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
            }

            json_data = {"data": {"type": "generations", "attributes": {
                "prompts": [
                    {"text": f"{prompt}", "weight": 1}],
                "length_seconds": 45, "seed": -30391}}}

            resp = requests.post(
                "https://api.stableaudio.com/v1alpha/generations/stable-audio-audiosparx-v1-0/text-to-music",
                headers=headers, json=json_data)
            print(resp.status_code)
            if resp.status_code == 400:
                print("token expired")
                return
            links = resp.json()
            print(links)
            link = links['links']['self']
            print(link)

            while True:
                resp_0 = requests.get(url=link, headers=headers)
                arti = resp_0.json()
                print('this is arti', arti)
                if arti['data']['attributes']['status']['status'] == "complete":
                    artifact = arti['links']["artifacts"]
                    respo = requests.get(url=artifact, headers=headers)
                    data = respo.json()
                    datao = data['data'][0]['links']['self']
                    print(datao)
                    musics = requests.get(url=datao, headers=headers)
                    if musics.status_code == 200:
                        os.makedirs(f"{dire}")
                        with open(f"{dire}/audio.mp3", "wb") as f:
                            f.write(musics.content)
                        return True
                    else:
                        print("Failed to download audio:", musics.status_code)
                        # audio = AudioSegment.from_file("audio.mp3")
                        # play(audio)
                        return False
                else:
                    pass
    except Exception as e:
        print("error:", e)
        return False
