import json
import requests
from telegram import Bot
import constants

with open(constants.configFile) as json_file:
    data = json.load(json_file)

if data["TELEGRAM_ALERTS"] == False : 
    exit()
    
TOKEN = data['TELEGRAM_TOKEN']
CHAT_ID = data['TELEGRAM_CHAT_ID']

if TOKEN == "" or CHAT_ID == "":
    raise Exception("Token ou Chat ID não configurados. Verifique o arquivo config.json")
    
bot = Bot(token=TOKEN)

def check_internet_connection():
    try:
        requests.get('http://www.google.com', timeout=5)
        return True
    except requests.ConnectionError:
        return False

async def send(message: str):
    if not check_internet_connection():
        print("Alerta: Sem conexão com a internet. Prosseguindo com a execução.")
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message)