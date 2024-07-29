import datetime
import requests

discord_url = "https://discord.com/api/webhooks/1259644999977668689/TP_nmYUQU4nIRdPktbdVRmhE4G430I6WorzYHw4K6Hts8smX_U0Wf7mHh9exWzTlKdTo"
#디스코드 채널로 메세지 전송
def discord_send_message(text):
    now = datetime.datetime.now()
    message = {"content": f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] {str(text)}"}
    requests.post(discord_url, data=message)
    print(message)