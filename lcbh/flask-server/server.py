from flask import Flask, request, jsonify
from flask_cors import CORS
from CS_X_MODEL import responseGenerator

app = Flask(__name__)
CORS(app)

rg = responseGenerator(dataset_file= r"Help_Desk_Data_Cleaned_for_Category_Model_Mark_2.csv")

@app.route("/inquiry", methods = ["POST"])
def home():
    if request.method == "POST":
        text = request.json.get("inquiry")

        response = rg.get_response(text)[0]
        cat = rg.get_response(text)[1]
        matched_ans = rg.get_response(text)[2]
        
        return jsonify({"inquiry": [response, cat, matched_ans]})

if __name__ == "__main__":
    app.run(debug= True)