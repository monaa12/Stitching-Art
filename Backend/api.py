from flask import Flask, jsonify, request, send_from_directory, redirect, flash, url_for
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename
import numpy as np
import cv2
import io
import os

app = Flask(__name__, static_folder='static')
UPLOAD_FOLDER = './UPLOAD_FOLDER'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'PNG'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
global img


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/<path:filename>')
def send_file(filename):
    return send_from_directory(app.static_folder, filename)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/', methods=['GET', 'POST'])
def receive_file():
    global img
    if request.method == 'POST':
        # check if the post request has the file part
        if 'photo' not in request.files:
            flash('No file part')
            return redirect(request.url)
        # Here is the code to convert the post request to an OpenCV object
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if photo and allowed_file(photo.filename):
                photo_name = secure_filename(photo.filename)
            # in_memory_file = io.BytesIO()
            # photo.save(in_memory_file)
            # data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
            # color_image_flag = 1
            # img = cv2.imdecode(data, color_image_flag)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo.filename))
            # return img
            return redirect(url_for('uploaded_file', filename=photo_name))
    return ""


if __name__ == '__main__':
    app.run(debug=True)
