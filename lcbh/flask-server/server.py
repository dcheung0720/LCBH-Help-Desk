from flask import Flask, request, jsonify
from flask_cors import CORS
from CS_X_MODEL import responseGenerator
from translate_model import translate_pressed, detect_inquiry_language



app = Flask(__name__)
CORS(app)


@app.route("/lang", methods = ["POST"])
def default_lang():
    if request.method == "POST":
        lang = detect_inquiry_language(request.json.get("inquiry"))
        return jsonify({"lang": lang})


@app.route("/inquiry", methods = ["POST"])
def home():
    if request.method == "POST":
        text = request.json.get("inquiry")
        rg = responseGenerator(n_neighbors = 5)
        # response = rg.get_response(text)[0]
        # cat = rg.get_response(text)[1]
        
        return jsonify({"inquiry": rg.get_response(text)})
    

# #Takes in inquiry as a string (txt) and returns the english translated form of it
# # Right now I only call this for spanish inquiries, but potentially could use to translate all non-English questions and/or canned responses
# def translate_text(txt, lang):
#     translator = Translator(to_lang="en", from_lang = lang)
#     translation = translator.translate(txt)
#     return translation


# #Returns the language code detected in a string
# def detect_inquiry_language(txt):
#     return detect(txt)

# #takes in an inquiry and returns tuple with language tag and translated (if not in english) inquiry
# def inquiry_sort(inquiry):
#     lang = detect_inquiry_language(inquiry)
#     if lang == "es":
#         return ("es", translate_text(inquiry, lang))
#     else:
#         return (lang, inquiry)
    
@app.route("/translation", methods = ["POST"])
def translate():
    if request.method == "POST":
        print(request.json.get("inquiry"))
        print(request.json.get("lang"))
        translated = translate_pressed(request.json.get("inquiry"), request.json.get("lang"))
        return jsonify({"translation": translated})
        

if __name__ == "__main__":
    app.run(debug= True)