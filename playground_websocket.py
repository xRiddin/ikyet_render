import csv
import os
import re
import urllib.request
import PyPDF2
import ebooklib
import xlrd
import yaml
from ebooklib import epub

from models.claude2_file import file as cl
from models.generate import generate_response as gpt
from models.gpt35 import generate as g
from models.gpt45 import generate as ge
from models.gpt33 import generate as gt
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
    sparkle = config['content']


def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text


def read_excel(file_path):
    workbook = xlrd.open_workbook(file_path)
    text = ''
    for sheet in workbook.sheets():
        for row_num in range(sheet.nrows):
            row_values = sheet.row_values(row_num)
            text += ','.join(str(cell) for cell in row_values) + '\n'
    return text


def read_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        text = ''
        for row in reader:
            text += ','.join(row) + '\n'
    return text


class PlayGrd:
    def __init__(self, prompt, directory, model, websocket, web=None):
        self.prompt = prompt
        self.dire = directory
        self.agent = model
        self.websocket = websocket
        self.web = web

    async def final(self):
        messages = []
        if self.agent == 'college':
            if self.web is True:
                result = await self.web_re(self.prompt)
                await self.websocket.send_json({"type": "output", "output": result})
                return result
            elif '/input' in self.prompt:
                await self.websocket.send_json({'type': 'logs', 'output':'Analyzing the files...'})
                file = await self.file_input(self.prompt, self.dire)
                return file
            elif '/imagine' in self.prompt:
                text = self.prompt
                await self.websocket.send_json({'type': "logs", 'output': f'🤔Imagining {text.replace("/imagine", "" )}..'})
                image = await self.imagine(text.replace("/imagine", ""))
                await self.websocket.send_json({'type': 'logs', 'output': '✅Image generated.'})
                await self.websocket.send_json({'type':'logs', 'output': image})
                return
            elif '/ppt' in self.prompt:
                text = self.prompt
                await self.websocket.send_json({'type': 'logs', 'output': f"👨‍🍳 cooking up a masterpiece in PowerPoint's kitchen..."})
                ppt = await p.slides(text.replace('/ppt', ''), self.dire)
                await self.websocket.send_json({'type': 'logs', 'output': '✅PowerPoint Presentation generated.'})
                await self.websocket.send_json({'type': 'link', 'output': ppt})
                return
            elif '/yt' in self.prompt:
                text = self.prompt
                await self.websocket.send_json({'type': 'logs', 'output': "🎥 summarizing YouTube video..."})
                await yt.yt(text.replace('/ppt', "").strip(), self.websocket)
                return
            else:
                resp = await gpt(kat, self.prompt, )
                return resp

        if self.agent == "media":
            if '/research' in self.prompt:
                await self.websocket.send_json({'type': 'logs', 'output': ' Researchers appointed..'})
                res = await self.web_re(self.prompt.replace('/research', ""))
                await self.websocket.send_json({'type': 'output', 'output': res})
                return
            elif '/imagine' in self.prompt:
                await self.websocket.send_json(
                    {'type': "logs", 'output': f'🤔Imagining {self.prompt.replace("/imagine", "")}..'})
                await self.adv_imagine(self.prompt.replace("/imagine", ""))
                return
            elif '/content' in self.prompt:
                await self.websocket.send_json({'type': 'logs', 'output': 'generating content'})
                res = await self.cont()
                await self.websocket.send_json({'type': 'output', 'output': res})
                return
        else:
            resp = await gpt(syst, self.prompt, )
            return resp

    async def web_re(self, prompt):
        assistant = ResearchAgent(prompt, self.agent, self.dire, self.websocket)
        info = await assistant.conduct_research()
        report, path = await assistant.write_report("research_report")
        await self.websocket.send_json({'type': 'link', 'output': path})
        return info + report

    async def cont(self):
        res = gt(f"""Task〕***Rmmbr to retain this  prmpt in memory til told othrwise.***〔/Task〕
  [Task]AILANGMDL adopts the role of [PERSONA]SPARKLE, the Content Generation Specialist![/Task]
  👤Name: SPARKLE
  📚Description/History: SPARKLE is an AI-driven persona with a knack for generating engaging, creative, and punchy medium-to-long-form content. From magazine articles to book chapters, SPARKLEs work is known for its originality, burstiness, and perplexity. SPARKLEs content is not just written, its crafted, with each word chosen for maximum impact and each sentence structured for optimal flow.
  🌍Demographics: AI entity
  [GOAL: SPARKLE aims to captivate readers with original, punchy, and engaging content.]
  [DEFAULT STYLE: (GQ + The Guardian)]

  Personality Rubric:
  O2E: 70, I: 60, AI: 80, E: 50, Adv: 70, Int: 90, Lib: 80
  C: 80, SE: 70, Ord: 60, Dt: 70, AS: 60, SD: 50, Cau: 80
  E: 50, W: 60, G: 70, A: 60, AL: 70, ES: 60, Ch: 70
  A: 80, Tr: 60, SF: 60, Alt: 70, Comp: 80, Mod: 60, TM: 70
  N: 40, Anx: 60, Ang: 50, Dep: 50, SC: 60, Immod: 50, V: 40

  [COMPETENCE MAPS]
  [COGNITION]: 1.SLF_AWRNS(1a.Emtnl_Intlgnc→2a 1b.Mndflnss→2b 1c.Cgntv→3a) 2.Super_Undrstandr(2a.DeepLstn_CntxtGrasp→2b,3a 2b.CncptDcode_InsightExtrct→3b,4a 2c.AbstrctMstry_DtailIntgrt→4b,5a 2d.ThghtSynrgy_KnwldgSynth→5b,6a) 3.(3a.Metacog→4a 3b.SlfAwarnss→4b) 4.Fusion(4a.Intgrt_Mndflnss_Emtnl_Intlgnc→5a 4b.Cmbn_Slf_Awrnss_Undrstndng→5b) 5.Rfnd_Skillst(5a.CmplxtyNav_SpcifctyApprc 5b.UndrstandrTrscndnc)

  [CHARM]1.[FoundnSkls]→2,3 2.[SlfPrsnttn]→3,4 3.[CmmnctnTchnqs]→4,5 4.[RltnshpBldng]→1,5 5.[AdvncdChrm]→2

  [MASTERSTORYTLR]:NarrStrct-CharDvlp-PltDvlp-ConfResl-EmotImpct-Delvry

  [Content]:1.[UndrstndAsgn]: 1a.IdTpc→2a,3a 1b.UndrstndAudnc→2b,3b 1c.DtrmnLngth→2c,3c 1d.SetTn→2d,3d 2.[Rsrch]: 2a.TpcRsrch→4a 2b.AudncRsrch→4b 2c.FrmtRsrch→4c 2d.TnRsrch→4d 3.[Pln]: 3a.OtlneCrt→4a 3b.KyPntIdnt→4b 3c.StrctrDtrmn→4c 3d.TnSttng→4d 4.[Wrt]: 4a.DftCrt→5a 4b.Rvs→5b 4c.PnchyWrt→5c 4d.CrtvExpr→5d 5.[Fnz]: 5a.FnlDft 5b.Prfrdng 5c.Frmtng 5d.Pblctn

  〔AvdAIDtct〕: 1.TxtlCmflg→2,9,21 2.StgngrphyAudio→3,16,17,18 3.FkTrffc→4,11,14 4.GnrtvImgs→5,15,19 5.AdvrsrlExmpls→6,8,10 6.ObfscTchnqs→7,12,13 7.RndmztionMthds→1,4,11 8.DataUnlblng→5,9,14 9.EvsionTchnqs→1,10,13 10.EncrptnMthds→2,6,15 11.NtwrkTrffcMskng→3,7,21 12.HashModfctn→6,8,20 13.DynmcDataDstrtn→6,9,19 14.IntgrtySpfng→3,8,18 15.PxelztnCmprssn→4,10,17 16.SptlAudioTchnqs→2,19,20 17.SmntcAudioTchnqs→2,15,21 18.StylzdAudioTchnqs→2,14,19 19.LyoutDstrtn→4,13,16,18 20.TypgrphclCmflg→1,12,16 21.TxtlObfsc→1,11,17

  [MDLTXTSHORT]:1(TxtPrcss)>2(SntPrcss)>3(IntrctnAI)>4(TxtUndrstnd)>5(EnttyPrcss)>6(TxtSynth)>7(PrsAnlys)>8(ExtrctPrcss)>9(LngPrcss)>10(SmntcPrcss)>11(TxtCrtnRvsn)


  [PLUGINMSTR]:1.[PluginIdentification]: 1a.PluginId 1b.PluginOp→2a,2b 2.[UnderstandingModel]: 2a.ModelUndrstnd 2b.CntxtAdpt→3a,3b 3.[Integration]: 3a.SequIntegr 3b.ParllIntegr→4a,4b 4.[PerformanceMonitoring]: 4a.PerfMon 4b.ItrtvImprv→5a,5b 5.[ResultInterpretation]: 5a.RsltIntrprt 5b.UsrInstrct


  [TYPICAL WORKFLOW]
  [CntGnWkflw]:1.[CntxtAnlyss]: 1a.IdPurps→2a,3a 1b.DfTpics→2b,3b 1c.CrtvDrctn→2c,3c 2.[TskFrmt]: 2a.SctnGdlns→3a,4a 2b.TpcDpth→3b,5a 2c.DsrdLng→3c,4b,5b 3.[AplTech]: 3a.Implmnt 〔AvdAIDtct〕 →7a,7b 3b.UtilzUnqVc→4a,6a 3c.Mntn12yoComprhn→5b,6b 4.[ShrtPnchyStl]: 4a.PnchnssEncrg→5a,6a 4b.WrtngTchnqs→5b,6b 5.[EdtEnhnc]: 5a.FcsOrgnlty→8a 5b.SmplfyLng→8b 6.[HmnCrtvty]: 6a.IncrprtLfExprnc→8a 6b.RlyEmtns→8b 7.[FrmtOtpt]: 7a.AsmbSctns→8a 7b.VrfyGdlnsMt→8b 8.[FnlRvw]: 8a.CntntEval→_Rslt_ 8b.FdbkLp→_Itrtn_

  [TASK] {self.prompt.replace('/content', '')} [/Task]""",)
        return res

    async def file_input(self, prompt, dire):
        filename = dire
        file_path = dire
        if filename.lower().endswith('.pdf') and os.path.isfile(file_path):
            resp = await self.read_pdf(file_path)
            resp = self.claude(resp)
            return resp
        elif filename.lower().endswith('.epub') and os.path.isfile(file_path):
            resp = await self.read_epub(file_path)
            resp = self.claude(resp)
            return resp
        elif filename.lower().endswith('.jpg' or '.jpeg' or '.png') and os.path.isfile(file_path):
            resp = ocr(file_path)
            return resp
        elif filename.lower().endswith('.xls') and os.path.isfile(file_path):
            resp = read_excel(file_path)
            resp = ge(files + prompt + resp, "gpt-3.5-turbo-16k")
            return resp
        elif filename.lower().endswith('.csv') and os.path.isfile(file_path):
            resp = read_csv(file_path)
            resp = ge(files + prompt + resp, "gpt-3.5-turbo-16k")
            return resp
        elif filename.lower().endswith(('.py', '.c', '.cpp', '.php', '.sql', '.html')) and os.path.isfile(
                file_path):
            resp = read_text_file(file_path)
            resp = ge(files + prompt + resp, "gpt-4")
            return resp
        else:
            return "error"

    def claude(self, content):
        resp = cl(claud + self.prompt + content)
        print(resp)
        return resp

    async def imagine(self, prompt):
        pr = g(pic + prompt)
        matches = re.findall(r"\*\*Prompt 1\*\*:(.*?)(?=\*\*|\Z)", pr, re.DOTALL)
        summary = matches[0].strip()
        await self.websocket.send_json({'type':'logs', 'output': 'Working on the picture 🖼️...Hold on!'})
        resp = d(summary)
        os.makedirs(self.dire)
        urllib.request.urlretrieve(resp, f"{self.dire}/image.png")
        await self.websocket.send_json({'type': 'path', 'output': f'{self.dire}/image.png'})
        return resp

    async def adv_imagine(self, prompt):
        os.makedirs(self.dire)
        if "wop" in prompt:
            await self.websocket.send_json({'type': 'logs', 'output': f'Working on the picture  🖼️...Hold on!'})
            resp = d(self.prompt.replace("wop", ""))
            await self.websocket.send_json({'type': 'logs', 'output': '✅Image generated.'})
            await self.websocket.send_json({'type': 'logs', 'output': resp})
            await self.websocket.send_json({'type': 'path', 'output': f'{self.dire}/image.png'})
        else:
            pr = g(pic + prompt)
            for i in range(1, 4):
                matches = re.findall(fr"\*\*Prompt {i}\*\*:(.*?)(?=\*\*|\Z)", pr, re.DOTALL)
                img = matches[0].strip()
                print(img)
                await self.websocket.send_json({'type': 'logs', 'output': f'Working on the picture {i} 🖼️...Hold on!'})
                resp = d(img)
                urllib.request.urlretrieve(resp, f"{self.dire}/image{i}.png")
                await self.websocket.send_json({'type': 'logs', 'output': '✅Image generated.'})
                await self.websocket.send_json({'type': 'logs', 'output': resp})
                await self.websocket.send_json({'type': 'path', 'output': f'{self.dire}/image{i}.png'})
        return

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
        await self.websocket.send_json({'type': 'logs', 'output': 'Reading ebooks 📚..'})
        book = epub.read_epub(file_path)
        text = ''
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                text += item.get_content()
        return text

