import json
from telegram import Bot

with open('config.json') as json_file:
    data = json.load(json_file)

if data["TELEGRAM_ALERTS"] == False : 
    exit()
    
TOKEN = data['TELEGRAM_TOKEN']
CHAT_ID = data['TELEGRAM_CHAT_ID']

if TOKEN == "" or CHAT_ID == "":
    raise Exception("Token ou Chat ID não configurados. Verifique o arquivo config.json")
    

bot = Bot(token=TOKEN)

async def send(message: str):
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message)



