import translation as translate


def translate_pressed(txt, usr_lang):
    detected_text_lang = translate.detect_inquiry_language(txt)
    if detected_text_lang != usr_lang:
        return translate.translate_text(txt, detected_text_lang, usr_lang)
    else:
        return translate.translate_text(txt, usr_lang, "en")
    
def detect_inquiry_language(txt):
    return translate.detect_inquiry_language(txt)