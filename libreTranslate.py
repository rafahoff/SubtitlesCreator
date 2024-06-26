import requests
from alerts.alert_handler import alert
import traceback

def translate_text(text: str,
                   orig_lang: str = "auto", 
                   trans_lang: str = "pt"):
    
    url = "http://localhost:5000/translate"
    
    dataJSON = {
        'q': text.encode('utf-8'),
        'source': orig_lang,
        'target': trans_lang
    }
    print(f"Traduzindo de '{orig_lang}' para '{trans_lang}'...")
    
    try:
        response = requests.post(url, data=dataJSON)
    except Exception as e:
        traceback.print_exc()
        alert("(!) Erro ao traduzir a legenda de '" + orig_lang + "' para '" + trans_lang + "': \n" + str(e)) 
    
    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        if 'translatedText' in response.json():
            return response.json()['translatedText']
        else:
            print(f"Response não contém 'translatedText'. Revise o formato do JSON: {response.json()}")
    else:
        alert(f"Requisição de tradução falhou com o código de status {response.status_code}. Resposta: {response.text}")


def returnLanguageCode(language_name: str):
    
    translation_languages = [
    {'code':'ar','name':'Arabic'},
    {'code':'az','name':'Azerbaijani'},
    {'code':'zh','name':'Chinese'},
    {'code':'cs','name':'Czech'},
    {'code':'da','name':'Danish'},
    {'code':'nl','name':'Dutch'},
    {'code':'en','name':'English'},
    {'code':'fi','name':'Finnish'},
    {'code':'fr','name':'French'},
    {'code':'de','name':'German'},
    {'code':'el','name':'Greek'},
    {'code':'he','name':'Hebrew'},
    {'code':'hi','name':'Hindi'},
    {'code':'hu','name':'Hungarian'},
    {'code':'id','name':'Indonesian'},
    {'code':'ga','name':'Irish'},
    {'code':'it','name':'Italian'},
    {'code':'ja','name':'Japanese'},
    {'code':'ko','name':'Korean'},
    {'code':'fa','name':'Persian'},
    {'code':'pl','name':'Polish'},
    {'code':'pt','name':'Portuguese'},
    {'code':'ru','name':'Russian'},
    {'code':'sk','name':'Slovak'},
    {'code':'es','name':'Spanish'},
    {'code':'sv','name':'Swedish'},
    {'code':'tr','name':'Turkish'},
    {'code':'uk','name':'Ukranian'},
    {'code':'pt','name':'Portuguese'}
]
    for language in translation_languages:
        if language['name'].lower() == language_name.lower():
            return language['code']
