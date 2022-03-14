from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from location import get_location
from VKorINST import JPEG
from exif import Image
from classification.inference import prediction_of_geo
import os



UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
LOCAL = False

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods = ['GET', 'POST'])
def index():
    message = ''
    location = []
    origin_of_photo = 'Cannot locate social network.'
    if request.method == 'POST':
        image_file = request.files['file']
        LOCAL = bool(int(request.form['options']))
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
        _, file_extension = os.path.splitext(filename)
        if file_extension in ['.jpg', '.jpeg']:
            binary_file = image_file.read()
            location = get_location(Image(binary_file))
            origin_of_photo = JPEG(binary_file).decode()
        if type(location) == tuple:
            latitude, longitude = location
            return render_template('index1.html',
                                   message=message,
                                   latitude=latitude,
                                   longitude=longitude)
        else:
            files_to_remove = [os.path.join(app.config['UPLOAD_FOLDER'], f) for f in
                               os.listdir(app.config['UPLOAD_FOLDER'])]
            for f in files_to_remove:
                os.remove(f)
            message = 'Location is not available from EXIF'
            image_file.seek(0)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            geo_marks = prediction_of_geo(LOCAL)

            # os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('index1.html', message=message,
                                   origin_of_photo=origin_of_photo,
                                   geo_marks=geo_marks)

    return render_template('index1.html')
