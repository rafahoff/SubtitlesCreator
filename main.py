import os
import subprocess
import transcribe
import winsound

###########
input_dir = "C:\\rascunho\\traduzir\\"
model_size = "tiny"
translate_to = "pt"
###########

file_extension_allowed = [".mp4", ".avi", ".mkv", ".mp3", ".aac", ".wav", ".flac", ".ogg", ".m4a", ".wma", ".webm", ".opus"]

# Inicia o serviço do LibreTranslate
print("Iniciando LibreTranslate...")
libreTranslate_process = subprocess.Popen("libreTranslate", stdout=subprocess.PIPE)

print("Processando diretório " + input_dir + "...")
for file in os.listdir(input_dir):
    if file.endswith(tuple(file_extension_allowed)):
        media_file = os.path.join(input_dir, file)
        
        transcribe.transcribe(media_file, model_size, translate=True, dest_lang=translate_to)
    
print("Processo concluído.")
libreTranslate_process.terminate()

winsound.Beep(2000, 200)
winsound.Beep(2000, 200)
winsound.Beep(1000, 800)
  

