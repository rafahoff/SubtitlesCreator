from pathvalidate import sanitize_filename
import re

def makeFileNameSafe(string):
    string = string.replace('：', ':')  # replace chinese colon with english colon
    string = re.sub(r'[&\/\\#,+()$~%.\'":*?<>{}!]', '', string)  # remove special characters
    string = re.sub(r'\s+', '_', string)  # replace spaces with underscores
    return sanitize_filename(string, replacement_text="_") 

def makeFileNameReadable(string):
    string = string.replace("_", " ")  # replace underscores with spaces
    return string