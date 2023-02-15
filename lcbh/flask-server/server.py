from flask import Flask, request, jsonify
from flask_cors import CORS
from CS_X_MODEL import responseGenerator

app = Flask(__name__)
CORS(app)

@app.route("/inquiry", methods = ["POST"])
def home():
    if request.method == "POST":
        text = request.json.get("inquiry")
        rg = responseGenerator(dataset_file= r"Help_Desk_Data_Cleaned_for_Category_Model_Mark_2.csv", n_neighbors=3)
        # response = rg.get_response(text)[0]
        # cat = rg.get_response(text)[1]
        
        return jsonify({"inquiry": rg.get_response(text)})

if __name__ == "__main__":
    app.run(debug= True)