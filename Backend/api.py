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


@app.route("/automatic_crop", methods=['GET', 'POST'])
def crop_by_obj_detection():
    if request.method == "POST":
        globals.obj_flag = True
        content = request.json
        globals.label = content['label']
        return jsonify(message="Crop by object detection is activated")
    return jsonify(message="Not a post request on object detection")


# Not used
@app.route("/manual_crop")
def manual_crop():
    globals.obj_flag = False
    run.init_app()
    return jsonify(message="")


@app.route("/params", methods=['GET', 'POST'])
def post_width_height():
    if request.method == "POST":
        # TODO:To be changed into number_of_grids_width only
        dim = request.json
        globals.width = dim['width']
        globals.height = dim['height']
        run.init_app()
        return jsonify(message="width in server side=" + str(globals.width))
    return jsonify(message="Not a post request on posting width and height")


# TODO:Create an api to get the width and height in cms and check it's route
@app.route("/params")
def get_width_height():
    return jsonify(width=globals.width, height=globals.height)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/<path:filename>')
# @app.route("/automatic_crop/<path:filename>")
@app.route('/grided')
def send_file():
    filename = "grided.png"
    return send_from_directory(app.static_folder, filename)


# Not used
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/', methods=['GET', 'POST'])
def POST_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'photo' not in request.files:
            flash('No image is sent')
            return jsonify(message="No image is sent")
        # Here is the code to convert the post request to an OpenCV object
        if 'photo' in request.files:
            globals.photo = request.files['photo']
            if globals.photo.filename == '':
                flash('No selected image')
                return jsonify(message="No selected image")
            if globals.photo and allowed_file(globals.photo.filename):
                photo_name = secure_filename(globals.photo.filename)
                # in_memory_file = io.BytesIO()
                # photo.save(in_memory_file)
                # data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
                # color_image_flag = 1
                # img = cv2.imdecode(data, color_image_flag)
                globals.photo.save(os.path.join(app.config['UPLOAD_FOLDER'], globals.photo.filename))
                # return img
                # return redirect(url_for('uploaded_file', filename=photo_name))
                return jsonify(message="Successfully uploaded" + globals.photo.filename)

    return jsonify(message="Not a POST request")


if __name__ == '__main__':
    globals.initialize()
    app.run(debug=True, threaded=True)
