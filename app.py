import numpy as np 
import pickle
from flask import Flask,request,jsonify,render_template
#from tensorflow import keras
import os

app = Flask(__name__)
model_blood_count = pickle.load(open("MLcode/model.pkl","rb"))
model_heart_failure = pickle.load(open("MLcode/model_heart_failure.pkl","rb"))
#model_pneumonia = keras.models.load_model('MLcode/model_xray')




@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predictnfs",methods=["POST"])
def predictnfs():
    input_features = [float(x) for x in request.form.values()]
    final_features = [np.array(input_features)]
    prediction = model_blood_count.predict(final_features)

    if prediction[0] == 1:
        output = "Semble normal"
    else:
        output = "s'éloigne de la marge"
    return render_template("nfs.html",predict_nfs = "Votre numeration de formule sanguine est {}".format(output))


@app.route("/nfs")
def nfs():
    return render_template("nfs.html") 


@app.route("/heartfailure")
def heart_failure():
    return render_template("heartfailure.html")


@app.route("/predictheart", methods = ["POST"])
def predictheart():
    input_features = [float(x) for x in request.form.values()]
    input_features.insert(0,1)
    final_features = [np.array(input_features)]
    prediction = model_heart_failure.predict(final_features)
    if prediction[0] == 1:
        output = "You are at high risk"
    else:
        output = "You are at low risk"
    return render_template("heartfailure.html",predict_heart = output)


@app.route("/pneumonia")
def pneumonia():
    return render_template("pneumonia.html")


if __name__ == "__main__":
    app.run(debug=True)