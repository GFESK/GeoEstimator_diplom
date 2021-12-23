from flask import Flask, request, render_template
from location import get_location
from jpg_decoder import detect_origin

app = Flask(__name__)

@app.route("/", methods = ['GET', 'POST'])
def index():
    message = ''
    if request.method == 'POST':
        image_file = request.files['file']
        location = get_location(image_file.read())
        #origin_of_photo = detect_origin(image_file.read())
        if type(location) == tuple:
            latitude, longitude = location
            return render_template('index.html', message=message,
                                   latitude=latitude,
                                   longitude=longitude)
        else:
            message = location
            return render_template('index.html', message=message)
    return render_template('index.html')
