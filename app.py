
import argparse
import io
from PIL import Image
import datetime

import torch
import cv2
import numpy as np
from re import DEBUG, sub
from flask import Flask, render_template, request, redirect, send_file, url_for, Response
from werkzeug.utils import secure_filename, send_from_directory
import os
import subprocess
from subprocess import Popen
import re
import requests
import shutil
import time

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index_demo.html')


# The display function is used to serve the image or video from the folder_path directory.
@app.route('/<path:filename>')
def display(filename):
    folder_path = 'runs/detect'
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    latest_subfolder = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
    directory = folder_path+'/'+latest_subfolder
    filename = predict_img.imgpath
    print(filename)
    file_extension = filename.rsplit('.', 1)[1].lower()
    environ = request.environ
    print(directory,filename,environ)
    if file_extension == 'jpg' or 'png':
        return send_from_directory(directory,filename,environ)
    else:
        return "Invalid File Format."


@app.route("/", methods=["GET", "POST"])
def predict_img():
    if request.method == "POST":
        if 'file' in request.files:
            f = request.files['file']
            basepath = os.path.dirname(__file__)
            filepath = os.path.join(basepath,'uploads',f.filename)
            print("Upload Folder is ", filepath)
            f.save(filepath)

            predict_img.imgpath = f.filename
            print("Printing ::: ", predict_img)

            file_extension = f.filename.rsplit('.', 1)[1].lower()
            if file_extension == 'jpg' or 'png':
                process = Popen(["python", "detect.py", '--source', filepath, 
                "--classes", "1", "--img-size", "256", "--weights", "best.pt"], shell=False)
                process.wait()


    folder_path = 'runs/detect'
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    latest_subfolder = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
    image_path = folder_path+'/'+latest_subfolder+'/'+f.filename
    return render_template('index_demo.html', files_path=image_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask App")
    parser.add_argument("--port", default=8000, type=int, help="port number")
    args = parser.parse_args()
    app.run(host="0.0.0.0", port=args.port)
