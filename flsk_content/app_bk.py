import os
import io
import numpy as np

import htr_main 

# import keras
# from keras.preprocessing import image
# from keras.preprocessing.image import img_to_array
# from keras.applications.xception import (
#     Xception, preprocess_input, decode_predictions)
# from keras import backend as K

from flask import request
from flask import url_for
from flask import render_template

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import text

from flask import Flask, request, redirect, url_for, jsonify

# Importing for mongo usage
from flask_pymongo import PyMongo


#Calling flask app and defining location of uploads folder.          
#Base = declarative_base()

#Importing HTR_MODEL
# from htr_model.src.DataLoader import DataLoader, Batch
# from htr_model.src.Model import Model, DecoderType
# from htr_model.src.main import main

# from main import inferTest

#load_dotenv()
#pymysql.install_as_MySQLdb()

# Database Connection (Usually, you'd put these in an .env file)
#username = os.getenv("database_username")
#password = os.getenv("database_password")
#host = os.getenv("database_host")
#port = os.getenv("database_port")
#database = os.getenv("database_database")

# Format:
# `<Dialect>://<Username>:<Password>@<Host Address>:<Port>/<Database>`
# Using f-string notation: https://docs.python.org/3/reference/lexical_analysis.html#f-strings
# fstrings require Python 3!
#connection = f"mysql://{username}:{password}@{host}:{port}/{database}"
# Python 2 compatible string concatenation:
# connection = "mysql://" + username + ':' + password + '@' + host + ':' + port + '/' + database 

#engine = create_engine(connection)
#conn = engine.connect()
#session = Session(bind=engine)
#         
app = Flask(__name__, static_folder='./static', static_url_path='')
app.config['UPLOAD_FOLDER'] = 'static/Uploads'

# URL for mongo database
mongo = PyMongo(app, uri="mongodb://localhost:27017/g5")

# model = None

# def load_model():
#     global model
#     model = Xception(weights="imagenet")

# load_model()

# def prepare_image(img):
#     img = img_to_array(img)
#     img = np.expand_dims(img, axis=0)
#     img = preprocess_input(img)
#     # return the processed image
#     return img

#Defining routes
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/info")
def backgroundinformation():
    return render_template('backgroundinformation.html')

@app.route("/text_analysis", methods=['GET', 'POST'])
def textanalysis():
    var = "Default"
    filename = ""

    if request.method == 'POST':
        #break into 2 one function to get form and the second to handle the upload doesnt need view can just have refirect
        #look into flash messages 

        if request.files.get('file'):
            # read the file
            file = request.files['file']

            # read the filename
            filename = file.filename
            filepath = url_for('static', filename='Uploads/'+filename)
            # Save the file to the uploads folder
            basedir = os.path.abspath(os.path.dirname(__file__))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            #return "Image Saved!"
            var = "Image Uploaded!"
    # function_result = htr_main.main2('static/Uploads/'+filename)
    # accuracy = function_result[0]
    # recognized_word = function_result[1]  
    # accuracy = accuracy, word = recognized_word, filepath = filepath      
    return render_template('textanalysis.html', var=var)

@app.route("/about")
def about():
    everything = mongo.db.colt.find()
    return render_template('about.html', everything=everything)

if __name__ == "__main__":
    app.run(debug=True)