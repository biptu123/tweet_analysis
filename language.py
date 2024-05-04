from googletrans import Translator
from langdetect import detect

translator = Translator()

def translate_text(text):
    try:
        src_lang = detect(text)
        
        translation = translator.translate(text=text, src=src_lang, dest="en")
        
        return translation.text
    except Exception as e:
        print(f"Error occurred: {e}")
        return False


