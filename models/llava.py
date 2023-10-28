from gradio_client import Client
import json


def llava(q: str, img: str):
	client = Client("https://ysharma-llava-v1.hf.space/--replicas/sdrv5/")
	client.predict(q, img, "Crop", fn_index=9)
	set = client.predict(
		"llava-v1.5-13b-4bit",  # str (Option from: []) in 'parameter_7' Dropdown component
		0.7,  # int | float (numeric value between 0.0 and 1.0) in 'Temperature' Slider component
		1,  # int | float (numeric value between 0.0 and 1.0) in 'Top P' Slider component
		1024,  # int | float (numeric value between 0 and 1024) in 'Max output tokens' Slider component
		fn_index=10
	)
	with open(set[0], 'rb') as fi:
		res = fi.readlines()
		print(res)
		c = res[0]
		file = json.loads(c)
		ans = file[0][1]
		print(ans)
	return ans
