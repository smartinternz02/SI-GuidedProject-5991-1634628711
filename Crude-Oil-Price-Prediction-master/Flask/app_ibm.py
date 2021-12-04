import numpy as np #used for numerical analysis
from flask import Flask,render_template,request #Flask is a application used to run/serve our aplication
# request is used to access the file which is uploaded by the user in our application
#render_template is used for rendering the html pages
from tensorflow.keras.models import load_model #we are loading our model from keras
import requests 
#import numpy as np 
# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account. 
API_KEY = "lfsI2GnruLv09Xw0XmqqVbn4K-zYOvxVpF7Aymk2aVjm" 
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'}) 
mltoken = token_response.json()["access_token"] 
 
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


app = Flask(__name__) #our flask app
#model = load_model('crude_oil.h5',) #loading the model in the flask app

@app.route('/') #rendering html template
def home() :
    return render_template("index.html") #rendering html template
@app.route('/about')
def home1() :
    return render_template("index.html") #rendering html template
@app.route('/predict')
def home2() :
    return render_template("web.html") #rendering html template

@app.route('/login',methods = ['POST']) #route for our prediction
def login() :
    x_input=str(request.form['year']) #requesting the file
    x_input=x_input.split(',')
    print(x_input)
    for i in range(0, len(x_input)): 
        x_input[i] = float(x_input[i])
    
            
    x_input=np.array(x_input).reshape(1,-1)
    n_steps=10
    i=0
    while(i<1):
        x_input = x_input.reshape((n_steps,1))
        payload_scoring = {"input_data": [{"fields": [["Closing Value"]], "values": [x_input.tolist()]}]}
        response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/217b4796-ac1e-4ee7-9ff8-d6dad471d267/predictions?version=2021-12-02', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
        yhat =response_scoring.json()
        i=i+1
        yhat=yhat['predictions'][0]['values'][0][0]
        #print(yhat[0])
        return render_template('web.html',showcase = 'The next day predicted value is : '+str(yhat))
    
if __name__ == '__main__' :
    app.run(debug = False,port=5000)
