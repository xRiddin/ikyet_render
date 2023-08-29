from .claude_api import Client


SESSION_KEY = "__cf_bm=uc20EBxEM9OCj6h9eAN8SBVp4LL8k1jB2xUaV_b3tlU-1692503038-0-ASdmUD23xjZ/dRFfCs80mLtiPBqGJ71JsDa/RSdgeHOGHYUfw+6cDIyaZITJ4BdbWmS16aja8Y9njY1cWKovuWI=; cf_clearance=9akkMJnkdtIToPp.1WNeAh8cX5swRDIG.VoD8IBoC9A-1692503043-0-1-d0efbd5d.2346dc50.87eee2bd-0.2.1692503043; intercom-device-id-lupk8zyo=9ee9e7a4-8719-480c-b13b-315d81b0546e; sessionKey=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; intercom-session-lupk8zyo=cWE4ajNiNDRZYkhPYXlNQVFicDFwSDByRzVUOFdQNXJWU2hzWXBEM0pNZWhxaW5jS1E1bDd1ZEFzZGNENzcrMy0tS01FK2FJekZLQUp3Mm9BOHhxWExMUT09--e8a1d936b26ba13e78bfd8e0a2c44d85567a40af"


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
