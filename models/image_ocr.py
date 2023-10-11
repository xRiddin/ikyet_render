from gradio_client import Client
import ast


def kosmos(url):
    client = Client("https://ydshieh-kosmos-2.hf.space/")
    result = client.predict(url, "Detailed", fn_index=4)
    print(result)
    text = result[2]
    text_data = ast.literal_eval(text)
    output = []
    for i in text_data:
        text1 = i[0]
        output.append(text1)
    print(', '.join(output))
    return output


def clipi2(url):
    client = Client("https://fffiloni-clip-interrogator-2.hf.space/")
    result = client.predict(url, "best",  2,  # int | float (numeric value between 2 and 24) in 'best mode max flavors' Slider component
        api_name="/clipi2")
    # (classic, fast, best)
    print(result)
    output = result[0]
    print(output)
    return output
