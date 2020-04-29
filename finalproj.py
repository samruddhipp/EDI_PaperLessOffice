"""
author - Mohit.
"""

from flask import Flask, request, redirect, render_template
import io
import PyPDF2
import os
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
root = os.getcwd()


file = "m"


@app.route('/')
def first_page():
    return render_template('first.html')


@app.route('/redirect', methods=['GET', 'POST'])
def redirect():
    return render_template('Frontend.html')


@app.route('/re', methods=['GET', 'POST'])
def re():
    return render_template('adminfp.html')


@app.route('/send', methods=['GET', 'POST'])
def send():

    if request.method == 'POST':
        file = request.form['id']
        path = root
        path = path+"\\" + file
        if os.path.isdir(path):
            os.chdir(path)
        else:
            os.mkdir(path)
            os.chdir(path)

        return render_template('upload_page.html')
    return render_template('Frontend.html')


@app.route('/pdf_upload', methods=['GET', 'POST'])
def pdf_upload():
    client = pymongo.MongoClient(
        "mongodb+srv://mohit13:vitsucks13@m13-kpbkz.mongodb.net/test?retryWrites=true&w=majority")
    db = client.trail
    coll = db.test
    doc =[]
    if request.method == 'POST':
        files = request.files.getlist('file')
        for fileup in files:
            content = fileup.read()

            pdf = PyPDF2.PdfFileReader(io.BytesIO(content))
            count = 0
            text = ""
            num_pages = pdf.numPages
            name = fileup.filename
            while count < num_pages:
                pageObj = pdf.getPage(count)
                count += 1
                text += pageObj.extractText()

            name = name[:-4]
            
            doc.append(text)
            # ON Device.................................................
            #     if os.path.isfile(name):
            #         f = open(name + ".txt", "a")
            #     else:
            #         f = open(name + ".txt", "w+")

            #     f.write(text)
            #     f.close()

            # path = root
            # return render_template('uploadedpdf.html', file=text)
            # os.rmdir(path)
        def insertdoc(pt):
            data ={
                "_id":file,
                "docs": pt
            }
            coll.insert_one(data)
        insertdoc(doc)
    return render_template('upload_page.html')


if __name__ == '__main__':
    app.run(debug=True)
