from translate import Translator
from langdetect import detect
import langid
#need to install Translator from pypi.org, and pip install langdetect

#Takes in inquiry as a string (txt) and returns the english translated form of it
# Right now I only call this for spanish inquiries, but potentially could use to translate all non-English questions and/or canned responses
def translate_text(txt, lang, to_lang):
    print("HELLO")
    translator = Translator(to_lang=to_lang, from_lang = lang)
    if len(txt) > 500:
        result = ""
        num_parts = int(len(txt)/500)
            
        if num_parts % 500 > 0:
            num_parts += 1
        print("NUM_PARTS=",num_parts)
        for i in range(num_parts):
            result += translator.translate(txt[i*500:i*500+500],'es')
        return result
    
    translation = translator.translate(txt)
    return translation

#Returns the language code detected in a string
def detect_inquiry_language(txt):
    return langid.classify(txt)[0]

#takes in an inquiry and returns tuple with language tag and translated (if not in english) inquiry
def inquiry_sort(inquiry):
    lang = detect_inquiry_language(inquiry)
    if lang == "es":
        return ("es", translate_text(inquiry, lang, "en"))
    #could technically translate any text, not just spanish with the language code, but i didn't cause sometimes it assumes english is swedish
    else:
        try:
            return (lang, translate_text(inquiry, lang, "en"))
        except:
            return(detect(inquiry), translate_text(inquiry, detect(inquiry), "en"))

# Assuming we can filter inquiries, and if they have the spanish tag, we can first categorize it as if it were english, 
# then use the category to grab a spanish response

#TESTING PRINT STATEMENTS
#print(inquiry_sort("estoy siendo desalojado"))
#print(inquiry_sort("i am being evicted"))
#print(inquiry_sort("Problema en el baño desde hace más de un año y los dueños hacen poco caso en arreglarlo, ellos solo piden la renta"))