import requests


def gen(prompt, w=1280, h=1280):
    headers = {
        'authority': 'replicate.com',
        'accept': 'application/json',
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }

    json_data = {
        'inputs': {
            'width': w,
            'height': h,
            'prompt': prompt,
            'refine': 'expert_ensemble_refiner',
            'scheduler': 'DDIM',
            'num_outputs': 1,
            'guidance_scale': 7.5,
            'high_noise_frac': 0.8,
            'prompt_strength': 0.8,
            'num_inference_steps': 50,
            "negative_prompt": "(nsfw:1.5),verybadimagenegative_v1.3, ng_deepnegative_v1_75t, (ugly face:0.8),cross-eyed,sketches, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, bad anatomy, DeepNegative, facing away, tilted head, {Multiple people}, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worstquality, low quality, normal quality, jpegartifacts, signature, watermark, username, blurry, bad feet, cropped, poorly drawn hands, poorly drawn face, mutation, deformed, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, extra fingers, fewer digits, extra limbs, extra arms,extra legs, malformed limbs, fused fingers, too many fingers, long neck, cross-eyed,mutated hands, polar lowres, bad body, bad proportions, gross proportions, text, error, missing fingers, missing arms, missing legs, extra digit, extra arms, extra leg, extra foot, repeating hair, nsfw, [[[[[bad-artist-anime, sketch by bad-artist]]]]], [[[mutation, lowres, bad hands, [text, signature, watermark, username], blurry, monochrome, grayscale, realistic, simple background, limited palette]]], close-up, (swimsuit, cleavage, armpits, ass, navel, cleavage cutout), (forehead jewel:1.2), (forehead mark:1.5), (bad and mutated hands:1.3), (worst quality:2.0), (low quality:2.0), (blurry:2.0), multiple limbs, bad anatomy, (interlocked fingers:1.2),(interlocked leg:1.2), Ugly Fingers, (extra digit and hands and fingers and legs and arms:1.4), crown braid, (deformed fingers:1.2), (long fingers:1.2)"
        },
    }
    r = requests.post(
        'https://replicate.com/api/models/stability-ai/sdxl/versions/2b017d9b67edd2ee1401238df49d75da53c523f36e363881e057f5dc3ed3c5b2/predictions',
        headers=headers,
        json=json_data,
    )
    res = r.json()
    uuid = res['uuid']
    print(uuid)

    while True:
        rs = requests.get(
            f'https://replicate.com/api/models/stability-ai/sdxl/versions/2b017d9b67edd2ee1401238df49d75da53c523f36e363881e057f5dc3ed3c5b2/predictions/{uuid}')
        res = rs.json()
        data = res['prediction']['status']
        output = res['prediction']['output']
        if data == "processing":
            print(data)
        elif data == "succeeded":
            if output[0] is not None:
                output = res['prediction']['output']
                print(output[0])
                return output[0]
