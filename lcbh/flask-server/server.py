from flask import Flask, request, jsonify
from flask_cors import CORS
from CS_X_MODEL import responseGenerator

app = Flask(__name__)
CORS(app)

@app.route("/inquiry", methods = ["POST"])
def home():
    if request.method == "POST":
        text = request.json.get("inquiry")
        rg = responseGenerator(dataset_file= r"Help_Desk_Data_Cleaned_for_Category_Model_Mark_2.csv")
        data = rg.get_response(text)
        return jsonify({"inquiry": data})

if __name__ == "__main__":
    app.run(debug= True)