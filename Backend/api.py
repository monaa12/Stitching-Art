from flask import Flask, jsonify, request, send_from_directory, redirect, flash, url_for
from werkzeug.utils import secure_filename
import numpy as np
import cv2
import io
import os
import globals
import run

app = Flask(__name__, static_folder='static')
app.secret_key = 'super secret'
UPLOAD_FOLDER = './UPLOAD_FOLDER'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'PNG'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
globals.app = app


@app.route("/automatic_crop")
def crop_by_obj_detection():
    globals.obj_flag = True
    globals.label = request.args['label']
    run.init_app()
    return ""


@app.route("/manual_crop")
def manual_crop():
    globals.obj_flag = False
    run.init_app()
    return ""


@app.route("/params", methods=['GET', 'POST'])
def post_width_height():
    if request.method == "POST":
        # TODO:To be changed into number_of_grids_width only
        # globals.number_of_grids_width = int(request.args['number_of_grids_width'])
        globals.width = int(request.args['width'])
        globals.height = int(request.args['height'])
    return ""


# TODO:Create an api to get the width and height in cms and check it's route
# @app.route("/params")
def get_width_height():
    return jsonify(width=globals.width, height=globals.height)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/<path:filename>')
@app.route("/automatic_crop/<path:filename>")
@app.route("/manual_crop/<path:filename>")
def send_file(filename):
    return send_from_directory(app.static_folder, filename)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/', methods=['GET', 'POST'])
def POST_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'photo' not in request.files:
            flash('No image is sent')
            return redirect(request.url)
        # Here is the code to convert the post request to an OpenCV object
        if 'photo' in request.files:
            globals.photo = request.files['photo']
            if globals.photo.filename == '':
                flash('No selected image')
                return redirect(request.url)
            if globals.photo and allowed_file(globals.photo.filename):
                photo_name = secure_filename(globals.photo.filename)
            # in_memory_file = io.BytesIO()
            # photo.save(in_memory_file)
            # data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
            # color_image_flag = 1
            # img = cv2.imdecode(data, color_image_flag)
            globals.photo.save(os.path.join(app.config['UPLOAD_FOLDER'], globals.photo.filename))
            # return img
            return redirect(url_for('uploaded_file', filename=photo_name))

    return ""


if __name__ == '__main__':
    globals.initialize()
    app.run(debug=True)
