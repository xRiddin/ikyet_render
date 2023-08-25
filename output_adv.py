import random
import re
import time

import yaml

from models import generate as g, gpt44 as ge
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
    gpt4code = config['gpt4code']


async def final(prompt, dire, websocket):
    await websocket.send_json({'type': 'logs', 'output': 'generating specifications for the application'})
    filepaths, specs = await filepath(prompt)
    await websocket.send_json({'type': 'output', 'output': specs})
    pattern = r"'([^']+)'\s*"
    filenames = re.findall(pattern, filepaths)
    print(len(filenames))

    for _ in range(len(filenames)):
        fil = await files(filenames[_], specs)
        print(filenames[_])
        time.sleep(15)
        await websocket.send_json({'type': 'logs', 'output': f'generating the codes for file: {_}'})
        final_code = await gpt41(filepaths_string=filepaths, file=filenames[_], chat=fil, specs=specs, direct=dire)
        await websocket.send_json({'type': 'output', 'output': final_code})
    await websocket.send_json({'type': 'logs', 'output': 'generating unit tests...'})
    unit = await unit_test(filepaths, final_code, dire)
    await websocket.send_json({'type': 'output', 'output': unit})


async def gpt41(filepaths_string, file, chat, specs, direct):
    while True:
        try:
            final_code = ge.generate( gpt4code + f"""
            these are the specifications for the files {specs},
            these are the other files that are worked upon later and shouldn't be edited now {filepaths_string},
            and this is the only file you should edit:{file},
            and this is the code of {file} that you will working on {chat}""", )
            fi_nal = await generate_final(file, specs, chat, final_code)
            w.write(fi_nal, f'{direct}/')
            return fi_nal
        except Exception as e:
            for _ in range(3):
                print(f'error:{e}, retrying after 10s...')
                time.sleep(10)
        """
        else:
            feed = await g.generate_response(gpt4, chat, )
            response = await generate_file(filepaths_string, feed + chat)
            w.write(response, direct)
            return response
        """


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


async def generate_final(file=None, specs=None, finals=None, change=None):
    resp = await g.generate_response(
        f'{gen + rewrite}',
        f"""
               you have been given feedback and improvements and changes to do:{change}
               Now your job is to generate only the code for the file:{file}
               Make sure to have consistent filenames if you reference other files we are also generating.

               Remember that you must obey 4 things:
                  - you are generating code for the file {file} 
                  - do not stray from the names of the files and the shared dependencies we have decided on
                  - the code to be corrected and re-written is {finals}
                  - MOST IMPORTANT OF ALL - the purpose of our app is {specs} - every line of code you generate must be valid code. there shouldn't be any explanation, if there is any explanation add it in comments. every line you generate must be valid code.  Do not include code fences in your response.

               Begin generating the code now.
               """,
    )
    return resp


async def filepath(prompt):
    specs = ge.generate(f'{spec}' + f'please generate the specifications for: {prompt}', )

    filepaths_string = await g.generate_response(
        f"""
        please only list the filepaths you would write, and return them as a python array of strings.
        do not write any other explanation, you should write only a python array of strings.
        output in the following format only: Where FILENAME is the filename of the code and EXTENSION is the extension of the file.
        ['FILENAME.EXTENSION', ]
        """,
        specs,
    )
    return filepaths_string, specs


async def files(filepaths_string, specs):
    chat = await generate_file(filepaths_string, prompt=specs)
    return chat


"""
async def feedback(filepaths_string, history, prompt, directory):
    while True:
        try:
            feed = gpt44.generate(gpt4, history + prompt, )
            response = await generate_file(filepaths_string, feed)
            w.write(response, directory)
            return response
        except Exception as e:
            for _ in range(5):
                print(f'error:{e}')
                time.sleep(10)
            feed = await g.generate_response(gpt4, history + prompt, )
            response = await generate_file(filepaths_string, feed)
            w.write(response, directory)
            return response
"""


def director():
    count = random.randint(0, 999999)
    return str(count)


async def unit_test(filepath_string, fi_nal, direct):
    testing = await generate_file(
        filepaths_string=filepath_string,
        prompt=f'{test}' + ', '.join(fi_nal),
    )
    w.write(testing, f"{direct}/unit_tests")
    return testing
