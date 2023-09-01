import random
import time

import yaml

from models import generate as g, gpt4_nov as ge
import write_file as w

with open('config.yml', 'r', encoding='utf-8') as config_file:
    config = yaml.safe_load(config_file)
    gen = config['GENERATE']
    phil = config['PHILOSOPHY']
    rewrite = config['re_write']
    test = config['UNIT']
    fixs = config['fix_code']
    spec = config['spec']
    gpt4 = config['gpt4']


async def final(prompt, dire, websocket):
    await websocket.send_json({'type': 'logs', 'output': 'generating specifications for your application..'})

    filepaths, specs = await filepath(prompt)
    await websocket.send_json({'type': 'output', 'output': specs})
    filess = await files(filepaths, specs)
    await websocket.send_json({'type':'logs', 'output': 'generating the files for your application'})
    gpt = await gpt41(filepaths, filess, specs, dire)
    await websocket.send_json({'type': 'output', 'output': gpt})
    await websocket.send_json({'type': 'output', 'output': 'generating unit tests for your application'})
    unit = await unit_test(filepaths, filess, dire)
    await websocket.send_json({'type': 'output', 'output': unit})

async def generate_file(filepaths_string=None, prompt=None):
    chat = await g.generate_response(
        f'{gen} + {phil}',
        f"""
           We have broken up the program into per-file generation.
           Now your job is to generate only the code for the file{filepaths_string}
           Make sure to have consistent filenames if you reference other files we are also generating.

           Remember that you must obey 3 things:
              - you are generating code for the file {filepaths_string} 
              - do not stray from the names of the files and the shared dependencies we have decided on
              - MOST IMPORTANT OF ALL - the purpose of our app is {prompt} - every line of code you generate must be valid code. there shouldn't be any explanation, if there is any explanation add it in comments. every line you generate must be valid code.  Do not include code fences in your response, for example

           Begin generating the code now.
           """,
    )
    return chat


async def generate_final(filepaths_string=None, prompt=None, final=None):
    resp = await g.generate_response(
        f'{gen + rewrite}',
        f"""
               Now your job is to generate only the code for the file{filepaths_string}
               Make sure to have consistent filenames if you reference other files we are also generating.

               Remember that you must obey 4 things:
                  - you are generating code for the file {filepaths_string} 
                  - do not stray from the names of the files and the shared dependencies we have decided on
                  - the code to be corrected and re-written is {final}
                  - MOST IMPORTANT OF ALL - the feedback or changes you have to do is {prompt} - every line of code you generate must be valid code. there shouldn't be any explanation, if there is any explanation add it in comments. every line you generate must be valid code.  Do not include code fences in your response.

               Begin generating the code now.
               """,
    )
    return resp


async def filepath(prompt):
    specs = await g.generate_response(f'{spec}', prompt, )

    filepaths_string = await g.generate_response(
        f"""
        please only list the filepaths you would write, and return them as a python array of strings.
        do not add any other explanation, only return a python array of strings.
        do not write any other explanation, you should write only a python array of strings.
        """,
        specs,
    )
    print(specs)
    return filepaths_string, specs


async def files(filepaths_string, specs):
    chat = await generate_file(filepaths_string, prompt=specs)
    """
    fix = await g.generate_response(
        f"{fixs}",
        f'{chat}',
    )
    fixed = await generate_file(filepaths_string, prompt=fix)
    """
    return chat


async def gpt41(filepaths_string, chat, specs, direct):
    while True:
        try:
            final_code = ge.generate(gpt4 + f""" please follow everything that is said to you now: {fixs}
            these are the specifications for the files {specs}
            these are the files you will be working on {filepaths_string}
            and these are the codes you will be working on {chat}""", )
            finalcode = await generate_final(filepaths_string=filepaths_string, prompt=final_code, final=chat)
            w.write(finalcode, f'{direct}/')
            return finalcode
        except Exception as e:
            for _ in range(3):
                print(f'error:{e}, retrying after 10s...')
                time.sleep(10)
            feed = await g.generate_response(gpt4, chat, )
            response = await generate_file(filepaths_string, feed + chat)
            w.write(response, direct)
            return response


"""
async def feedback(filepaths_string, history, prompt, directory):
    while True:
        try:
            feed = gpt44.generate(gpt4, history+prompt, )
            response = await generate_file(filepaths_string, feed)
            w.write(response, directory)
            return response
        except Exception as e:
            for _ in range(5):
                print(f'error:{e}')
                time.sleep(10)
            feed = await g.generate_response(gpt4, history+prompt,)
            response = await generate_file(filepaths_string, feed)
            w.write(response, directory)
            return response
"""


def director():
    count = random.randint(0, 999999)
    return str(count)


async def unit_test(filepath_string, final, direct):
    testing = await generate_file(
        filepaths_string=filepath_string,
        prompt=f'{test}' + final,
    )
    w.write(testing, f"{direct}/unit_tests")
    return testing
