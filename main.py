from flask import Flask, request, render_template
from location import get_location


app = Flask(__name__)

@app.route("/", methods = ['GET', 'POST'])
def index():
    message = ''
    if request.method == 'POST':
        image_file = request.files['file']
        answer = get_location(image_file.read())
        if type(answer) == tuple:
            latitude, longitude = answer
            return render_template('index.html', message=message, latitude=latitude, longitude=longitude)
        else:
            message = answer
            return render_template('index.html', message=message)
    return render_template('index.html')
