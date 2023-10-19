import os
import shutil
import tempfile
import threading
import tiktoken
import time
import yaml
from typing import List

import uvicorn
from fastapi import FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from ikyet_render.models.gpt.gpt_messages import generate as g
from output_adv import final as m
from output_quick import director
from output_quick import final as n
from playground_websocket import PlayGrd
from run import WebSocketManager

app = FastAPI()

# Mount the static files directory to serve your HTML/CSS/JS files
app.mount("/static", StaticFiles(directory="static"), name="static")

current_directory = None
file_path = None
manager = WebSocketManager()
templates = Jinja2Templates(directory="client")

with open('config.yml', 'r', encoding='utf-8') as config_file:
    config = yaml.safe_load(config_file)
    jenn = config['jen']

messages = [{'role': 'system', 'content': jenn}]
websocket_connections = {}


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "report": None})


@app.get("/aidev.html")
async def chat(request: Request):
    return templates.TemplateResponse("aidev.html", {"request": request, "report": None})


@app.get("/pw.html")
async def plygrd(request: Request):
    return templates.TemplateResponse("pw.html", {"request": request, "report": None})


@app.websocket_route("/ws")
async def playgrd(websocket: WebSocket):
    current_directory = get_directory()
    await manager.connect(websocket)
    while True:
        try:
            data = await websocket.receive_json()
            print(data)
            prompt = data["input"]
            print(prompt)
            web = data["web"]
            model = data["model"]
            global file_path
            if file_path:
                fin = PlayGrd(prompt, file_path, model, websocket, web)
                res = await fin.final()
                print(res)
                await websocket.send_json({'type': 'output', 'output': res})
                file_path = None
            else:
                fin = PlayGrd(prompt, current_directory, model, websocket, web)
                res = await fin.final()
                print(res)
                await websocket.send_json({'type': 'output', 'output': res})
        except WebSocketDisconnect:
            break


@app.websocket("/jen")
async def jen(websocket: WebSocket):
    await websocket.accept()
    # websocket_connections[client_id] = websocket
    while True:
        try:
            data = await websocket.receive_json()
            print(data)
            prompt = data["input"]
            messages.append({'role': 'user', 'content': prompt})
            res = g(messages, 'gpt-3.5-turbo-16k')
            messages.append({'role': 'assistant', 'content': res})
            '''
            num_tokens = tokens(messages['content'])
            if num_tokens > 16000:
              new_messages = g("summarize the messages", user)
              user = new_messages
            '''
            print(messages)
            await websocket.send_json({'output': res})
        except WebSocketDisconnect:
            print("websocket disconnected")
            # del websocket_connections[client_id]
            await websocket.close()
            break


@app.websocket_route("/aidev")
async def ma_in(websocket: WebSocket):
    get_directory()
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_json()
            print(data)
            prompt = data["input"]
            adv = data["adv"]
            web = data["web"]
            if adv is True:
                await websocket.send_json({'type': 'logs', 'output': '🏢Building a team of quality engineers...'})
                resp = await advance(prompt, websocket)
                await websocket.send_json({'type': 'output', 'output': resp})
            else:
                await websocket.send_json({'type': 'logs', 'output': 'your AI developer is booting..'})
                resp = await quick(prompt, websocket)
                await websocket.send_json({'type': 'output', 'output': resp})
        except WebSocketDisconnect:
            break


async def advance(prompt: str, websocket):
    directory_path = current_directory
    res = await m(prompt, directory_path, websocket)


async def quick(prompt: str, websocket):
    directory_path = current_directory
    resp = await n(prompt, directory_path, websocket)


@app.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    current_directory = director()
    for file in files:
        if file.filename == "":
            continue
        filename = file.filename
        file_paths = os.path.join(current_directory, filename.strip())
        dirt = os.path.dirname(file_paths)
        os.makedirs(dirt, exist_ok=True)
        with open(file_paths, "wb") as f:
            f.write(file.file.read())
        app.mount(f"/{current_directory}", StaticFiles(directory=current_directory), name=current_directory)
        global file_path
        file_path = file_paths
    return {"file_path": file_path}


@app.get("/files_download")
async def download():
    directory_path = current_directory
    temp_dir = tempfile.mkdtemp()
    zip_file_path = os.path.join(temp_dir, "ikyet.zip")
    try:
        shutil.make_archive(os.path.join(temp_dir, "ikyet"), "zip", directory_path)
        return FileResponse(zip_file_path, media_type="application/zip")
    except Exception as e:
        print(e)
    finally:
        threading.Thread(target=delayed_delete, args=(directory_path,)).start()
    # finally:
    # shutil.rmtree(temp_dir)
    # shutil.rmtree(directory_path)


def delayed_delete(*paths):
    time.sleep(30)  # wait 30 seconds before deleting
    for path in paths:
        shutil.rmtree(path)


def get_directory():
    global current_directory
    if current_directory is None or current_directory == current_directory:
        current_directory = generate_directory_name()
    return current_directory


def generate_directory_name():
    directory = director()
    return directory


def tokens(message):
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(message))
    print("number of tokens:", num_tokens)
    return num_tokens


uvicorn.run(app, host='0.0.0.0', port=8000)
