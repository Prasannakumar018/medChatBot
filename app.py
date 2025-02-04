from flask import Flask,render_template,request,jsonify
from flask_cors import CORS
from chat import get_response

app=Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    text=request.get_json("message")
    texty=str(text['message'])
    response=get_response(texty)
    message={"answer": response}
    return jsonify(message)

if __name__=="__main__":
    app.run(debug=True)