from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import Response
from PIL import Image
import requests
from cStringIO import StringIO
import pdb
import base64

app = Flask(__name__)
WIDTH = 200
HEIGHT = 150

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/filter', methods=['POST','GET'])
def filter():
    img_url = request.form.get('img-url')
    response = requests.get(img_url)
    img = Image.open(StringIO(response.content))
    img_gray = img.convert('L')
    w, h = img_gray.size
    aspect = 1.0*w/h
    if aspect > 1.0*WIDTH/HEIGHT:
        width = min(w, WIDTH)
        height = width/aspect
    else:
        height = min(h, HEIGHT)
        width = height*aspect
    io = StringIO()
    img_gray.save(io, format="png")
    contents = io.getvalue()
    io.close()
    img_str = base64.b64encode(contents)

    image = {
        'width': int(width),
        'height': int(height),
        'data': img_str
    }
    return jsonify(image)

@app.route('/submit_img', methods=['POST'])
def submit_img():
    img_url = request.form['img-url']
    images = []
    response = requests.get(img_url)
    img = Image.open(StringIO(response.content))
#    img_gray = img.convert('L')
    w, h = img.size
    aspect = 1.0*w/h
    if aspect > 1.0*WIDTH/HEIGHT:
        width = min(w, WIDTH)
        height = width/aspect
    else:
        height = min(h, HEIGHT)
        width = height*aspect
    images.append({
        'width': int(width),
        'height': int(height),
        'src': img_url,
    })
    return render_template('index.html', images=images)

@app.route('/hello')
def hello():
    return 'Hello World'

if __name__ == '__main__':
    app.run(debug=True)
