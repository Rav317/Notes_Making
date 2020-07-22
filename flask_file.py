import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

from notemaker import *

import speech_recognition as sr
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
import subprocess

from summarize import summarize_htmlpage, summarize_caption

from scrape import generate_scraped_content

from nlp import generate_keywords_file

from youtube_search import generate_transcripts_for_youtube

UPLOAD_FOLDER = '/home/tanishq/MAVIS/DotSlash2020/Working_code/main/finalworkingcode'
ALLOWED_EXTENSIONS = set(['mp4','txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'log'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # print("\n\n\n",file.filename,"\n\n\n")
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            extract_caption(UPLOAD_FOLDER+filename)
            filename = "captions"
            caption_filename =  filename + "_n.txt"
            make_para(filename)

            generate_keywords_file()

            generate_transcripts_for_youtube("words.txt")

            generate_summary(caption_filename)

            # generate_scraped_content("words.txt")
            return "DONE"

    return '''
    </!DOCTYPE html>
    <center>
    <title>Notemaker For Videos</title>
    <h1>Upload new File</h1>
    <style>
    
    title
    {
        border : 1px solid black;
        border-radius: 50%;
        padding: 20px;
    }

    body
    {
        background-color: #f3f3f3;
    }

    .button
    {
        background-color: #110314   ;
        color: white;
        font-size: 20px;
        padding: 10px 90px;
        border: 0px;
        border-radius: 5px;
        width: 300px;
        height: 45px;
    }
    .button:hover
    {
        background-color: grey;
    }

    </style>
    <form action="" method=post enctype=multipart/form-data>
      <p><input class="button" type=file name=file>
         <input class="button" type=submit value=Upload>
      </p>
    </form>
    </center>
    '''

# main driver function 
if __name__ == '__main__': 

    # run() method of Flask class runs the application 
    # on the local development server. 
    app.run(debug  = True)
    # debug  = True, '0.0.0.0:5000'
