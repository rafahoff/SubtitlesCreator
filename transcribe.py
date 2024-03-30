import subprocess
import os
import re
import libreTranslate
import shutil
from alerts.alert_handler import alert
from pathvalidate import sanitize_filename
import time
import traceback
import file_helper

def transcribe(
    input_file: str = "",
    model: str =[ "tiny", "base", "small", "medium", "large", "large-v2"],
    translate: bool = False,
    dest_lang: str = "en",
    verbose = False): 
    
    whisper_path = "whisper-faster"
    language = "auto"
    
    source_lang = ""
    status = ""
    
    input_dir = os.path.dirname(input_file)
    just_file_name, ext = os.path.splitext(input_file)
    just_file_name = file_helper.makeFileNameSafe(os.path.basename(just_file_name))
        
    # rename the file 
    shutil.move(input_file, os.path.join(input_dir, just_file_name + ext))    
      
    processed_dir = os.path.join(input_dir, "processed\\")
    subtitles_dir = os.path.join(processed_dir, "subtitles\\")
    subtitle_file = os.path.join(subtitles_dir, just_file_name + ".srt")
    input_file = os.path.join(input_dir, just_file_name + ext)
       
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)
        
        if not os.path.exists(subtitles_dir):
            os.makedirs(subtitles_dir)


    args = "--model " + model
    args = args + " --output_dir " + subtitles_dir + " --output_format srt --beep_off --verbose " + str(verbose)
    if not verbose:
        args = args + " --print_progress"

    if language != "auto":
        args = args + " --language " + language
                
    whisper_args = whisper_path + " " + input_file + " " + args

    if os.path.exists(subtitle_file):
        bkp_srt_file = subtitles_dir + just_file_name + "_bkp.srt"
        
        if os.path.exists(bkp_srt_file):
            os.remove(bkp_srt_file)
            
        os.rename(subtitle_file, bkp_srt_file)
        print("Backup da legenda anterior criado em: " + bkp_srt_file)

    try:
        process = subprocess.Popen(whisper_args, stdout=subprocess.PIPE)

        for line in process.stdout:
            status = line.decode().strip()
            start_time = time.time()

            elapsed_minutes = (time.time() - start_time) / 60 # minutes
            
            # heartbeat every 10 minutes
            if elapsed_minutes >= 10:
                alert("Transcrição em andamento...")
                start_time = time.time()
            
            if 'Detected language ' in status:
                source_lang =  re.search("Detected language '(.*?)' with probability", status).group(1)
                source_lang = source_lang.replace("'", "")
                source_lang = libreTranslate.returnLanguageCode(source_lang)
                print("Idioma detectado: " + source_lang)
            
            print(status)

        alert("Transcrição concluída para: \n" + just_file_name)
        shutil.move(input_file, processed_dir)
        
    except Exception as e:
        traceback.print_exc()
        tryError = f"(!) ERRO ao transcrever o arquivo: \n {str(e)}"
        alert(tryError)
        raise Exception(tryError)

    if translate:
        if os.path.exists(subtitle_file):
            print(f"Arquivo de legenda encontrado: \n {subtitle_file}")
            
            if source_lang != dest_lang:
                if source_lang == "":
                    print("Não foi possível detectar o idioma de origem. Definindo como 'auto'")
                    source_lang = "auto"
                
                with open(subtitle_file, 'r') as file:
                    subtitle_content = file.read()      
                
                # rename the subtitle file
                shutil.move(subtitle_file, subtitles_dir + just_file_name + " (" + source_lang.upper() + ").srt")      
                
                alert("Traduzindo legenda de '" + source_lang + "' para '" + dest_lang + "'...")                            
                translated_text = libreTranslate.translate_text(subtitle_content, source_lang, dest_lang)
                translated_subtitle_file = subtitles_dir + just_file_name + ".srt"

                with open(translated_subtitle_file, 'w', encoding='utf-8') as file:
                    file.write(translated_text)
                
                alert("Tradução concluída")
            else:
                alert("Idioma de origem e destino são iguais.\n"
                      "Nenhuma tradução necessária.")
        else:
            alert("ERRO: arquivo de legenda não encontrado:" + subtitle_file)
