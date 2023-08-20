import csv
import os
import re

import PyPDF2
import ebooklib
import xlrd
import yaml
from ebooklib import epub

from models.claude2_file import file as cl
from models.generate import generate_response as gpt
from models.gpt35 import generate as g
from models.gpt45 import generate as ge
from models.image_ocr import query as ocr
from models.sdxl import gen as d
import ppt as p
from research_agent import ResearchAgent
import yt

with open('config.yml', 'r', encoding='utf-8') as config_file:
    config = yaml.safe_load(config_file)
    rewrite = config['re_write']
    gpt4 = config['gpt4']
    pic = config['imgprompt']
    claud = config['claud']
    syst = config['syst']
    files = config['files']
    kat = config['kat']


class PlayGrd:
    def __init__(self, prompt, directory, model, websocket, web=None):
        self.prompt = prompt
        self.dire = directory
        self.agent = model
        self.websocket = websocket
        self.web = web

    async def final(self):
        history = []
        if self.agent == 'college':
            if self.web is True:
                result = await self.web_re()
                await self.websocket.send_json({"type": "output", "output": result})
                return result
            if '/input' in self.prompt:
                await self.websocket.send_json({'type': 'logs', 'output':'Analyzing the files...'})
                file = await self.file_input(self.prompt, self.dire)
                return file
            if '/imagine' in self.prompt:
                text = self.prompt
                await self.websocket.send_json({'type': "logs", 'output': f'🤔Imagining {text.replace("/imagine", "" )}..'})
                image = await self.imagine(text.replace("/imagine", ""))
                await self.websocket.send_json({'type': 'logs', 'output': '✅Image generated.'})
                await self.websocket.send_json({'type':'output', 'output': image})
                return
            if '/ppt' in self.prompt:
                text = self.prompt
                await self.websocket.send_json({'type': 'logs', 'output': f"👨‍🍳 cooking up a masterpiece in PowerPoint's kitchen..."})
                ppt = await p.slides(text.replace('/ppt', ''), self.dire)
                await self.websocket.send_json({'type': 'logs', 'output': '✅PowerPoint Presentation generated.'})
                await self.websocket.send_json({'type': 'link', 'output': ppt})
                return
            if '/yt' in self.prompt:
                text = self.prompt
                await self.websocket.send_json({'type': 'logs', 'output': "🎥 summarizing YouTube video..."})
                content = await yt.yt(text.replace('/ppt', "").strip(), self.websocket)
                return
            else:
                resp = await gpt(kat, self.prompt, )
                return resp

        else:
            resp = await gpt(syst, self.prompt, )
            return resp

    async def web_re(self):
        assistant = ResearchAgent(self.prompt, self.agent, self.dire, self.websocket)
        info = await assistant.conduct_research()
        report, path = await assistant.write_report("research_report")
        await self.websocket.send_json({'type': 'link', 'output': path})
        return info + report

    async def file_input(self, prompt, dire):
        filename = dire
        file_path = dire
        if filename.lower().endswith('.pdf') and os.path.isfile(file_path):
            content = await self.read_pdf(file_path)
            resp = self.claude(content)
            return resp
        elif filename.lower().endswith('.epub') and os.path.isfile(file_path):
            content = await self.read_epub(file_path)
            resp = self.claude(content)
            return resp
        elif filename.lower().endswith('.jpg' or '.jpeg' or '.png') and os.path.isfile(file_path):
            resp = ocr(file_path)
            return resp
        elif filename.lower().endswith('.xls') and os.path.isfile(file_path):
            content = self.read_excel(file_path)
            resp = ge(files + prompt + content, "gpt-3.5-turbo-16k")
            return resp
        elif filename.lower().endswith('.csv') and os.path.isfile(file_path):
            content = self.read_csv(file_path)
            resp = ge(files + prompt + content, "gpt-3.5-turbo-16k")
            return resp
        elif filename.lower().endswith(('.py', '.c', '.cpp', '.php', '.sql', '.html')) and os.path.isfile(
                file_path):
            content = self.read_text_file(file_path)
            resp = ge(files + prompt + content, "gpt-4")
            return resp
        else:
            return "error"

    def claude(self, content):
        resp = cl(claud + self.prompt + content)
        print(resp)
        return resp

    async def imagine(self, prompt):
        pr = g(pic, pic + prompt, )
        matches = re.findall(r"\*\*Prompt 1\*\*:(.*?)(?=\*\*|\Z)", pr, re.DOTALL)
        summary = matches[0].strip()
        await self.websocket.send_json({'type':'logs', 'output':'Working on the picture 🖼️...Hold on!'})
        resp = d(summary)
        return resp

    async def read_pdf(self, file_path):
        await self.websocket.send_json({'type': 'logs', 'output':'Reading pdf pages 📖..'})
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ''
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        return text

    async def read_epub(self, file_path):
        await self.websocket.send_json({'type': 'logs', 'output':'Reading ebooks 📚..'})
        book = epub.read_epub(file_path)
        text = ''
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                text += item.get_content()
        return text

    def read_csv(self, file_path):
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            text = ''
            for row in reader:
                text += ','.join(row) + '\n'
        return text

    def read_text_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text

    def read_excel(self, file_path):
        workbook = xlrd.open_workbook(file_path)
        text = ''
        for sheet in workbook.sheets():
            for row_num in range(sheet.nrows):
                row_values = sheet.row_values(row_num)
                text += ','.join(str(cell) for cell in row_values) + '\n'
        return text

