from PIL import Image
import socket
import os
from flask import Flask, render_template, request

app = Flask(__name__)

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['image']
        f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(f)
        try:
            im = Image.open(f)
            prediction = "Image Uploaded"
        except IOError as e:
            prediction = f"<i>{e}</i>"
            os.remove(f)
        html = f'''<h3>Hello {os.getenv("NAME", "world")}!</h3>
             <b>Hostname:</b> {socket.gethostname()}<br/>
             <b>Message:</b> {prediction}<br/>'''
        im.thumbnail((101,101))
        im.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename.split(".")[0]+".PNG"))
        del im

    return html


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

