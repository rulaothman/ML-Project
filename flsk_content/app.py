import os
import io
import numpy as np
import sys

from flask import request
from flask import url_for
from flask import render_template

from flask import Flask, request, redirect, url_for, jsonify

# Importing for mongo usage
from flask_pymongo import PyMongo


app = Flask(__name__, static_folder='./static', static_url_path='')
app.config['UPLOAD_FOLDER'] = 'static/Uploads'

# Create path to handle addl scripts
sys.path.insert(0, 'templates/other')
import htr_main 

# URL for mongo database
mongo = PyMongo(app, uri="mongodb://localhost:27017/g5")

#Defining routes
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/info")
def backgroundinformation():
    return render_template('backgroundinformation.html')

# Text analysis route
@app.route("/text_analysis", methods=['GET', 'POST'])
def textanalysis():
	# Load page with empty variables
    if request.method != 'POST':
        return render_template('textanalysis.html', var="", accuracy = "", word = "", filepath = "")
	# Process post request
    elif request.method == 'POST':
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
            function_result = htr_main.main2('static/Uploads/'+filename)
            accuracy = function_result[0]
            recognized_word = function_result[1]        
            return render_template('textanalysis.html', var=var, accuracy = accuracy, word = recognized_word, filepath = filepath) 
        else:
            pass
    else:
        return render_template('textanalysis.html', var="Something's wrong!", accuracy = "", word = "", filepath = "")

    return render_template('textanalysis.html', var="Something's wrong!", accuracy = "", word = "", filepath = "")

#about page    
@app.route("/about")
def about():
    everything = mongo.db.colt.find()
    return render_template('about.html', everything=everything)

if __name__ == "__main__":
    app.run(debug=True)