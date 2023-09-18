from .claude_api import Client


SESSION_KEY = "__cf_bm=RNkxkN5Pnf8x2.bhA8tjTbHK.D8hVJbjT5JG2ma9LwA-1694918420-0-AV7bo+LTz6IVIVUy3+7FGFoYsYXPd8fRHzvIw7X548cCftVlhdjRSa7cC7Ojte4qsK1TANBcF76YfceExCbweLA=; cf_clearance=2m7AzMArl5_N2ckA3cmUGb_vwgNTF5NeRcolmJfxd6E-1694918423-0-1-9ce7f260.a4aafa5c.cbe6ad80-0.2.1694918423; intercom-device-id-lupk8zyo=d88ca19d-429d-4280-bfc0-736aaf3cf335; sessionKey=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; intercom-session-lupk8zyo=aDRhQUR2SlpDN1NKb2JzQ2ZDdFNlK2VmS3l6UXdQQXFJZFB0cGFoODlQN0tyZDVCaHpJVW1DS0g4RExqemQyZi0tMGRyYkhHeG9DSGl3VGdMNHFQTGx4Zz09--6143d3d68836a0d48d989f306644cdec76e9e3db"

def file(files):
    print("this is claude2")
    claude = Client(SESSION_KEY)
    conversation = claude.create_new_chat()
    conv_id = conversation['uuid']
    resp = claude.send_message(files, conv_id)
    print(resp)
    deleted = claude.delete_conversation(conv_id)
    if deleted:
        print("conv deleted")
    else:
        print("not deleted")
    return resp
