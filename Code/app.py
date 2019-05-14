from PIL import Image
import socket
import os
from flask import Flask, render_template, request, session, flash
from pre import pre_process_me
from datetime import timedelta
from model_predict import predict_me
app = Flask(__name__)
app.secret_key = b'some_secret'
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


@app.route('/')
def default_access():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def home_page():
    if request.method == 'POST':
        if request.args.get('type') == "upload_me":
            if get_image() and get_thres():
                flash("Upload Success")
            else:
                flash("Upload Failed")

            return render_template("index.html")


@app.route('/predict', methods=['GET', 'POST'])
def predicts_me():
    if 'thres' in session and 'image_file_name' in session:
        X, X_feat = pre_process_me(session['image_file_name'])
        #call in model and predict
        salt_prop, mask_graph, scats = predict_me(X, X_feat, "0cc1d0e4c4.png", session['thres'])
        flash('Plot Me')
        print(salt_prop, mask_graph)
        return render_template("index.html", salt_prop=salt_prop, mask_graph=mask_graph, plots=scats)
    else:
        flash("Please Upload Seismic Image and Threshold Value")
        return render_template("index.html")
    return render_template("index.html")


def get_thres():
    try:
        thres = request.form['Thres']
        session['thres'] = int(thres)
        print(session)
        return True
    except Exception as e:
        return False


def get_image():
    file = request.files['Simage']
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(f)
    flag = False
    try:
        im = Image.open(f)
        flag = True
        session['image_file_name'] = file.filename.split(".")[0] + ".PNG"
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
        session['mask_file_name'] = file.filename.split(".")[0] + ".PNG"
    except IOError as e:
        os.remove(f)
    im.thumbnail((101, 101))
    im.save(os.path.join(app.config['MASK_FOLDER'], file.filename.split(".")[0] + ".PNG"))
    del im
    return flag


