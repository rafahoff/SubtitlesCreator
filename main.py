import os
import subprocess
import transcribe
import winsound
from alerts.alert_handler import alert
import json

###########
input_dir = "C:\\rascunho\\traduzir\\"
turnoff_beep = False
verboseTranscription = False
###########

with open('config.json') as json_file:
    data = json.load(json_file)

model_size = data["MODEL"]
translate_to = data["TRANSLATE_TO"]

file_extension_allowed = [".mp4", ".avi", ".mkv", ".mp3", ".aac", ".wav", ".flac", ".ogg", ".m4a", ".wma", ".webm", ".opus"]
total_files = 0
total_processed = 0

shut_down = input("Deseja desligar o computador após a execução do script? (s/n) ").lower() == "s"
if shut_down:
    print("O computador será desligado após a execução do script.")

# Inicia o serviço do LibreTranslate
print("Iniciando LibreTranslate...")
libreTranslate_process = subprocess.Popen("libreTranslate", stdout=subprocess.PIPE)

print("Processando diretório " + input_dir + "...")
media_files = []
for file_searched in os.listdir(input_dir):
    if file_searched.endswith(tuple(file_extension_allowed)):
        media_files.append(file_searched)

total_files = len(media_files)
alert("---------------------- \nEncontrado " + str(total_files) + " arquivo(s) no diretório de transcrições")
for file in media_files:
    total_processed += 1
    processed_file = os.path.join(input_dir, file)
    
    alert("Transcrevendo o arquivo ("+ str(total_processed) +"/"+str(total_files)+"): \n" + file)
    transcribe.transcribe(processed_file, model_size, verbose=verboseTranscription, translate=True, dest_lang=translate_to)
    
alert("Processo de transcrições concluído. \n ----------------------")
libreTranslate_process.terminate()

if not turnoff_beep:
    winsound.Beep(2000, 200)
    winsound.Beep(2000, 200)
    winsound.Beep(1000, 800)    

if shut_down:
    alert("Computador sendo desligado...")
    os.system("shutdown /s /t 1")
  

