from PIL import Image
import socket
import os
from flask import Flask, render_template, request, session
from pre import pre_process_me
app = Flask(__name__)

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
MASK_FOLDER = os.path.basename('masks')
app.config['MASK_FOLDER'] = MASK_FOLDER

#   TODO:
#   MASK UPLOAD IN WEBSITE, PREDICT BUTTON
#   MODEL model-tgs-salt-2.h5


@app.before_request
def make_session_active():
    session.modified = True


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=300)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if get_mask() and get_image():
            prediction = "Uploaded Successfully"
        else:
            prediction = "Error :("
        html = f'''<h3>Hello {os.getenv("NAME", "world")}!</h3>
             <b>Hostname:</b> {socket.gethostname()}<br/>
             <b>Message:</b> {prediction}<br/>'''

    return html


@app.route('/', methods=['POST'])
def upload_file():
    if 'mask_file_name' in session and 'image_file_name' in session:
        X, X_feat, Y = pre_process_me(session['image_file_name'], session['mask_file_name'])
        #call in model and predict

    return html


def get_image():
    file = request.files['image']
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(f)
    flag = False
    try:
        im = Image.open(f)
        flag = True
        session['image_file_name'] = file.filename
    except IOError as e:
        os.remove(f)
    im.thumbnail((101, 101))
    im.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename.split(".")[0] + ".PNG"))
    del im
    return flag


def get_mask():
    file = request.files['mask']
    f = os.path.join(app.config['MASK_FOLDER'], file.filename)
    file.save(f)
    flag = False
    try:
        im = Image.open(f)
        flag = True
        session['mask_file_name'] = file.filename
    except IOError as e:
        os.remove(f)
    im.thumbnail((101, 101))
    im.save(os.path.join(app.config['MASK_FOLDER'], file.filename.split(".")[0] + ".PNG"))
    del im
    return flag


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
