import random
import re, os
import time

import yaml

from models import gpt_ca as g, gpt4_nov as ge
import write_file as w

with open('config.yml', 'r', encoding='utf-8') as config_file:
    config = yaml.safe_load(config_file)
    gen = config['GENERATE']
    rewrite = config['re_write']
    unit = config['UNIT']
    fixs = config['fix_code']
    spec = config['spec']
    gpt4 = config['gpt4']
    gpt4code = config['gpt4code']
    form = config['format']


async def final(prompt, dire, websocket):
    file = []
    await websocket.send_json({'type': 'logs', 'output': " 📄 An architect is currently engaged in the process of designing the application's blueprint..."})
    filepaths, specs = await filepath(prompt)
    await websocket.send_json({'type': 'output', 'output': specs})
    pattern = r"'([^']+)'\s*"
    filenames = re.findall(pattern, filepaths)
    print(len(filenames))
    await websocket.send_json({'type': 'logs', 'output': " 🧑‍💻 Our engineers ⚙️ are actively engaged in developing the software..."})
    for _ in range(len(filenames)):
        print(filenames[_])
        await websocket.send_json({'type': 'logs', 'output': f'🧑‍💻 Our coder working on file number: {_}'})
        final_code = await gpt41(file=filenames[_], specs=specs, direct=dire)
        file.append(final_code)
        await websocket.send_json({'type': 'output', 'output': final_code})
    await websocket.send_json({'type': 'logs', 'output': ', '.join(file)})
    await websocket.send_json({'type': 'logs', 'output': ' 👩‍💻Testers are developing unit tests for the developed software...'})
    unit_t = await unit_test(filepath_string=filepaths, fi_nal=specs, direct=dire)
    await websocket.send_json({'type': 'output', 'output': unit_t})


async def gpt41(file, specs, direct):
    while True:
        try:
            final_code = ge.generate( gpt4 + f"""
            these are the specifications for the files {specs},
            and this is the only file you should edit:{file}:
            """, )
            fi_nal = await generate_final(file=file, specs=specs, finals=final_code)
            w.write(chat=fi_nal, direct=f'{direct}/', filename=file)
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
    chat = g.generate(
        gen +
        f"""
           We have broken up the program into per-file generation.
           Now your job is to generate only the code for the file{filepaths_string}
           Make sure to have consistent filenames if you reference other files we are also generating.

           Remember that you must obey 3 things:
              - you are generating code for the file {filepaths_string} 
              - do not stray from the names of the files and the shared dependencies we have decided on
              - MOST IMPORTANT OF ALL - the purpose of our app is {prompt} 
              - every line of code you generate must be valid code. there shouldn't be any explanation, if there is any explanation add it in comments. every line you generate must be valid code.  Do not include code fences in your response, for example

           Begin generating the code now.
           """,
    )
    return chat


async def generate_final(file=None, specs=None, finals=None):
    resp = g.generate(
        f"""   you're an expert at markdown, you will follow this markdown format: {form}
               Now your job is to rewrite only the code in the above markdown format.
               Make sure to have consistent filenames if you reference other files we are also generating.

               Remember that you must obey 4 things:
                  - rewrite only the code in the above markdown format.
                  - do not stray from the names of the files and the shared dependencies we have decided on
                  - MOST IMPORTANT OF ALL - the purpose of our app is {specs} 
                  - every line of code you generate must be valid code. there shouldn't be any explanation, if there is any explanation add it in comments. every line you generate must be valid code.  Do not include code fences in your response.
               Begin generating the code now.
               """ + finals
    )
    return resp


async def filepath(prompt):
    specs = ge.generate(spec + prompt)

    filepaths_string = g.generate(
        f"""
            you should read the specifications and intelligently list the required files for an application to work.
            please only list the filepaths you would write, and return them as a python array of strings.
            do not add any other explanation, only return a python array of strings.
            do not write any other explanation, you should write only a python array of strings.
            """ + '/n' +
        specs
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
        prompt=unit + fi_nal,
    )
    w.write(testing, f"{direct}/unit_tests")
    return testing
