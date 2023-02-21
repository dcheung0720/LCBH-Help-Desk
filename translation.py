from translate import Translator
from langdetect import detect
#need to install Translator from pypi.org, and pip install langdetect

#Takes in inquiry as a string (txt) and returns the english translated form of it
# Right now I only call this for spanish inquiries, but potentially could use to translate all non-English questions and/or canned responses
def translate_text(txt, lang):
    translator = Translator(to_lang="en", from_lang = lang)
    translation = translator.translate(txt)
    return translation


#Returns the language code detected in a string
def detect_inquiry_language(txt):
    return detect(txt)

#takes in an inquiry and returns tuple with language tag and translated (if not in english) inquiry
def inquiry_sort(inquiry):
    lang = detect_inquiry_language(inquiry)
    if lang == "es":
        return ("es", translate_text(inquiry, lang))
    else:
        return (lang, inquiry)

# Assuming we can filter inquiries, and if they have the spanish tag, we can first categorize it as if it were english, 
# then use the category to grab a spanish response

#TESTING PRINT STATEMENTS
#print(inquiry_sort("estoy siendo desalojado"))
#print(inquiry_sort("i am being evicted"))
#print(inquiry_sort("Problema en el baño desde hace más de un año y los dueños hacen poco caso en arreglarlo, ellos solo piden la renta"))