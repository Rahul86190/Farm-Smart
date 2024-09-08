# app.py
from flask import Flask, render_template, request ,jsonify
import joblib,pandas as pd 


from pymongo import MongoClient
std_scaler=joblib.load("./models/std_scaler.lb")
kmeans_model=joblib.load("./models/kmeans_model.lb")
df=pd.read_csv("./models/filter_crops.csv")
app = Flask(__name__)

connection_string= "mongodb+srv://rahulsaini132005:20QWO9wOz43Tj3Ur@newproject1.xuqcm.mongodb.net/?retryWrites=true&w=majority&appName=NEWproject1"
client = MongoClient(connection_string)
# database , collection 
database = client["Farmer2"]    # database 
collection = database['FarmerData1']  # table create or collection 


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/suggestion')
def suggestion():
    return render_template('suggestion.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/quiz')
def quiz():
    return render_template('quiz.html')
@app.route('/experience')
def experience():
    return render_template('experience.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/experience_data', methods=["POST"])
def experience_data():
    if request.method=="POST":
        name = request.form.get('name')
        email = request.form.get('email')
        experience = request.form.get('experience')

        file=open("experience_data","a")
        file.write(f"Name - {name},\nEmail - {email},\nExperience - {experience}\n\n")
        file.close()
        return jsonify({'message': 'Success'}), 200
@app.route('/contact_info', methods=["POST"])
def contact_info():
    if request.method=="POST":
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        file=open("messages","a")
        file.write(f"Name - {name},\nEmail - {email},\nMessage- {message}\n\n")
        file.close()
        return jsonify({'message': 'Success'}), 200

@app.route('/submit', methods=['POST'])
def submit():
    if request.method=="POST":
        nitrogen = int(request.form.get('nitrogen'))
        phosphorus = int(request.form.get('phosphorus'))
        potassium = int(request.form.get('potassium'))
        temperature = float(request.form.get('temperature'))
        humidity =float( request.form.get('humidity'))
        ph = float(request.form.get('ph'))
        rainfall = float(request.form.get('rainfall'))
        
        # You can now use these variables to process or store the data
        print(f"N: {nitrogen}, K: {potassium}, P: {phosphorus}, Temp: {temperature}, Humidity: {humidity}, pH: {ph}, Rainfall: {rainfall}")
        
        unseen_data= [[nitrogen,phosphorus,potassium,temperature,humidity,ph,rainfall]]
        # return unseen_data

        trasnformer_data= std_scaler.transform(unseen_data)
        cluster=kmeans_model.predict(trasnformer_data)[0]
        # return f" your cluster no is{cluster}"
        suggestion_crops=list(df[df["cluster_no"]==cluster]["label"].unique())

        data = {"N":nitrogen,"P":phosphorus,"K":potassium,"temperature":temperature,"humidity":humidity,"PH":ph,"rainfall":rainfall,"Suggested_Crop":suggestion_crops}
        data_id = collection.insert_one(data).inserted_id
        print("Your data is inserted into the mongodb your record id is : ",data_id)

        # return f"suggestedd crops :{suggestion_crops}"
        return render_template("output.html",
                               nitrogen=nitrogen,
                               phosphorus=phosphorus,
                               potassium=potassium,
                               temperature=temperature,
                               humidity=humidity,
                               ph=ph,
                               rainfall=rainfall,
                               suggestion_crops=suggestion_crops)


if __name__ == '__main__':
    app.run(debug=True)
