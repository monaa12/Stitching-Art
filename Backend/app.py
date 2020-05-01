from flask import Flask, jsonify, request, send_from_directory, redirect, flash, url_for
from flask_restful import Resource, Api
import numpy as np
import cv2
import io
import os

app = Flask(__name__, static_folder='static')
# api = Api(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
global img


# image_name = 'a&p.PNG'
# label = "apple"
# @app.route("/<string:image_name, label>")
# class ImageClass(Resource):
#    def get(self):
#        return {'hello': 'world'}
# api.add_resource(HelloWorld, '/')


@app.route('/<path:filename>')
def send_file(filename):
    return send_from_directory(app.static_folder, filename)


@app.route('/', methods=['GET', 'POST'])
def receive_file():
    global img
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
    # Here is the code to convert the post request to an OpenCV object
    if 'photo' in request.files:
        photo = request.files['photo']
        in_memory_file = io.BytesIO()
        photo.save(in_memory_file)
        data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
        color_image_flag = 1
        img = cv2.imdecode(data, color_image_flag)
        photo.save(os.path.join(app.static_folder, photo.filename))
    # return img
    return redirect(url_for('uploaded_file', filename=photo.filename))


if __name__ == '__main__':
    app.run(debug=True)
