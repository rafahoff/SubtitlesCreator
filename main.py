import os
import subprocess
import transcribe
import winsound
from alerts.alert_handler import alert
import json
import file_helper
from pydub.utils import mediainfo

###########
turnoff_beep = False
verboseTranscription = False
###########

with open('config.json') as json_file:
    data = json.load(json_file)

model_size = data["MODEL"]
translate_to = data["TRANSLATE_TO"]
input_dir = data["INPUT_DIR"]

file_extension_allowed = [".mp4", ".avi", ".mkv", ".mp3", ".aac", ".wav", ".flac", ".ogg", ".m4a", ".wma", ".webm", ".opus"]
total_files: int = 0
total_processed: int = 0
total_size: float = 0
total_duration: float = 0

shut_down = input("Deseja desligar o computador após a execução do script? (s/n) ").lower() == "s"
if shut_down:
    print("O computador será desligado após a execução do script.")

print(f"Model '{model_size}' escolhido para transcrição."
      f"Traduzir para '{translate_to}'.")

# Inicia o serviço do LibreTranslate
print("Iniciando LibreTranslate...")
libreTranslate_process = subprocess.Popen("libreTranslate", stdout=subprocess.PIPE)

print("Processando diretório " + input_dir + "...")
media_files = [] # [file_name, file_size, time_duration]

for file_searched in os.listdir(input_dir):
    if file_searched.endswith(tuple(file_extension_allowed)):
        full_path = os.path.join(input_dir, file_searched)
        file_info = mediainfo(full_path)
#        file_size = os.path.getsize(full_path) / (1024 * 1024) # MB
        file_size = float(file_info["size"]) / (1024 * 1024) # MB
        total_size += file_size
        duration = float(file_info["duration"]) # seconds
        total_duration += duration
        media_files.append([file_searched, file_size, duration])

total_files = len(media_files)
total_hours = int(total_duration // 3600)
total_minutes = int((total_duration % 3600) // 60)
total_seconds = int(total_duration % 60)

total_time_formatted = f"{total_hours:02d}h{total_minutes:02d}m{total_seconds:02d}s"

alert(f"---------------------- \n"
      f"Encontrado no diretório de transcrições:\n"
      f" Arquivos: {str(total_files)}\n"
      f" Tamanho total: {total_size:.2f} MB\n"
      f" Duração total: {total_time_formatted}")

for file in media_files:
    total_processed += 1
    processed_file = os.path.join(input_dir, file[0])
    
    hours = int(file[2] // 3600)
    minutes = int((file[2] % 3600) // 60)
    seconds = int(file[2] % 60)

    formatted_time = f"{hours:02d}h{minutes:02d}m{seconds:02d}s"

    alert("Transcrevendo ("+ str(total_processed) +"/"+str(total_files)+"): \n" + 
        " Arquivo: " + file_helper.makeFileNameReadable(file[0]) + "\n" + 
        " Tamanho: " + "{:.2f}".format(file[1]) + " MB\n" +
        " Duração: " + formatted_time)
    
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
  

