# importing flask modules
from flask import Flask , request , render_template , jsonify

# importing firebase_admin module
import firebase_admin

# importing firestore.py module to create firestore client
from firebase_admin import firestore

# importing credentials.py module from firebase_admin folder
from firebase_admin import credentials

# creating authentication file
cred = credentials.Certificate("display-meter-89885-firebase-adminsdk-qc41f-07895c8e03.json")

# connect this python script/app with firebase using the authentication credentials
firebase_admin.initialize_app(cred)

# creating firestore client

db_client = firestore.client()
# creating flask object
app = Flask(__name__)

# first api : index page, only GET requests allowed at this API 
@app.route('/',methods=['GET'])
def index():
        try:
                # getting values from firebase document
                # convert it to python dictionary format
                pot= db_client.collection('Project 252').document('potentiometer values').get().to_dict()

                # extracting value from dictionary
                val=pot['pot val']

                # rendering index.html template and pass the extracted value
                return render_template('index.html',value=val)
        
        except Exception as e:
                print(e)
                return jsonify({'status': 'failed'})
                




# second api : adding data , only POST request allowed at this API
@app.route('/add' , methods = ['POST'])

def add():
        try:
                # getting potentiometer value from esp32
                pot_val = request.json.get('potentiometer')

                # sending potentiometer value on firebase
                db_client.collection('Project 252').document('potentiometer values').set({'pot val' : pot_val})


                # return status is json format
                return jsonify({'status': 'success'})
        
        except Exception as e:
                print(e)                        # printing error first
                return jsonify({'status' : 'failed'})
        
        
# x=[a,b,c,d]  a=0,b=1,c=2,d=3 list in python n array in js
# json= java script object notation 
# student={
        # name:"Jai Jackson",
        # age:15,
        # country:"New Zealand"
        
# }

# var options={
#     restitution    :0.5,
#     friction:2
# }

# print(x[2]) o/p c
# print(student.age) o/p 15




# start the server
if __name__  ==  "__main__":
    app.run(host = '0.0.0.0' , debug = True)

