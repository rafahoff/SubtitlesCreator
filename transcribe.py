import subprocess
import os
import re
import libreTranslate
import shutil


def transcribe(
    input_file: str = "",
    model: str =[ "tiny", "base", "small", "medium", "large"],
    translate: bool = False,
    dest_lang: str = "en"): 
    
    whisper_path = "whisper-faster"
    language = "auto"
    verbose = False
    source_lang = ""
    status = ""
    
    just_file_name = os.path.splitext(os.path.basename(input_file))[0]
    input_dir = os.path.dirname(input_file)
    processed_dir = os.path.join(input_dir, "processed\\")
    subtitles_dir = os.path.join(processed_dir, "subtitles\\")
    subtitle_file = os.path.join(subtitles_dir, just_file_name + ".srt")
       
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)
        
        if not os.path.exists(subtitles_dir):
            os.makedirs(subtitles_dir)


    args = "--model " + model
    args = args + " --output_dir " + subtitles_dir + " --output_format srt --print_progress --beep_off --verbose " + str(verbose)

    if language != "auto":
        args = args + " --language " + language
        
    input_file = input_file
        
    whisper_args = whisper_path + " " + input_file + " " + args

    if os.path.exists(subtitle_file):
        bkp_srt_file = subtitles_dir + just_file_name + "_bkp.srt"
        
        if os.path.exists(bkp_srt_file):
            os.remove(bkp_srt_file)
            
        os.rename(subtitle_file, bkp_srt_file)
        print("Backup da legenda anterior criado em: " + bkp_srt_file)

    process = subprocess.Popen(whisper_args, stdout=subprocess.PIPE)

    for line in process.stdout:
        status = line.decode().strip()
        
        if 'Detected language ' in status:
            source_lang =  re.search("Detected language '(.*?)' with probability", status).group(1)
            source_lang = source_lang.replace("'", "")
            source_lang = libreTranslate.returnLanguageCode(source_lang)
            print("Idioma detectado: " + source_lang)
        
        print(status)

    print("Transcrição concluída.")

    if translate:
        if os.path.exists(subtitle_file):
            print("Arquivo de legenda encontrado: " + subtitle_file)
            
            if source_lang != dest_lang:
                if source_lang == "":
                    print("Não foi possível detectar o idioma de origem. Definindo como 'auto'")
                    source_lang = "auto"
                
                with open(subtitle_file, 'r') as file:
                    subtitle_content = file.read()      
                
                # rename the subtitle file
                shutil.move(subtitle_file, subtitles_dir + just_file_name + " (" + source_lang.upper() + ").srt")      
                            
                translated_text = libreTranslate.translate_text(subtitle_content, source_lang, dest_lang)
                translated_subtitle_file = subtitles_dir + just_file_name + ".srt"

                with open(translated_subtitle_file, 'w') as file:
                    file.write(translated_text)
                
                print("Legenda traduzida em: " + os.path.join(subtitles_dir, translated_subtitle_file))
            else:
                print("Idioma de origem e destino são iguais. Nenhuma tradução necessária.")
            
            shutil.move(input_file, processed_dir)
        else:
            print("ERRO: arquivo de legenda não encontrado:" + subtitle_file)


  

