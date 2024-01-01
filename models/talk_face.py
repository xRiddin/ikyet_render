from gradio_client import Client


def gen(img, audio):
	client = Client("https://camenduru-com-one-shot-talking-face.hf.space/")
	result = client.predict(
		img,
		# str (filepath on your computer (or URL) of image) in 'parameter_5' Image component
		audio,
		# str (filepath on your computer (or URL) of file) in 'parameter_6' Audio component
		fn_index=1
	)
	print(result)
	return result
