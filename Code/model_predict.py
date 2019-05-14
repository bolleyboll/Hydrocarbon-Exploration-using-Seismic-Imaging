from keras.models import load_model
from PIL import Image
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly
import plotly.graph_objs as go
import plotly.plotly as py
import json
import tensorflow as tf
import pickle
import pandas as pd
import os

w, h = 128, 128


UNET = load_model('model-tgs-salt-2.h5')
# UNET._make_predict_function()
gr = tf.get_default_graph()
with gr.as_default():
    UNET.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


def scatter_random():
    try:
        file = open('..\\..\\..\\scatter.pickle', 'rb')
    except Exception as e:
        file=open(os.path.join(os.getcwd(),"scatter.pickle"),'rb')    
    df = pickle.load(file)
    trace = go.Scatter(
        x=df['salt_proportion'], y=df['z'],
        mode='markers'
    )

    data = [trace]
    layout = go.Layout(
        title='Correlation between Depth and the Presence of Salt',
        autosize=True,
        width=1280,
        height=700,
        xaxis=dict(
            title='Salt Proportion',
        ),
        yaxis=dict(
            title='Depth',
        ),

    )
    graphJSON = (json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder), json.dumps(layout, cls=plotly.utils.PlotlyJSONEncoder))
    return graphJSON


def predict_me(X, X_feat, file_name, threshold=None, gen_results=False):
    global gr
    with gr.as_default():
        Y = UNET.predict({'img': X, 'feat': X_feat})
    # print(Y)
    if gen_results:
        mask_graph = get_mask_graph(Y, threshold, ret_Y=True)
    else:
        mask_graph = get_mask_graph(Y, threshold)

    Y = Y.squeeze() * 255
    salt_prop = 0
    if threshold:
        Y = np.array([[thres(int(j), threshold) for j in i] for i in Y])
        salt_prop = salt_proportion(Y, threshold)
    else:
        Y = np.array([[int(j) for j in i] for i in Y])
        salt_prop = salt_proportion(Y, 70)
    # print(Y.shape)
    # print(Y)
    # im = Image.new('1', (w, h))
    # im.putdata(Y)
    # im.save('result.png')
    # img = Image.fromarray(Y)
    # plt.imshow(Y, cmap='hot', interpolation='nearest')
    # # plt.axis('off')
    # plt.show()
    # plt.savefig('.\\results\\result_' + file_name)

    # plt.savefig("test.png", bbox_inches='tight')
    # img.show()
    # return salt_prop, 'result_' + file_name
    return salt_prop, mask_graph, scatter_random()


def salt_proportion(Y, threshold):
    try:
        Y = np.array([[thres(int(j), threshold, ret=False) for j in i] for i in Y])
        unique, counts = np.unique(Y, return_counts=True)
        # The total number of pixels is 101*101 = 10,201
        return counts[1] / 15744.

    except:
        return 0.0


def thres(x, t, ret=True, mul=1):
    if (x * mul) >= t * 255 / 100:
        if ret:
            return x
        else:
            return 255
    else:
        return 0


def get_mask_graph(Z, threshold, ret_Y=False):
    Z = Z.squeeze()
    Z = np.array([[thres(round(j, 2), threshold, mul=255) for j in i] for i in Z])
    if ret_Y:
        return Z
    trace = go.Heatmap(z=Z, colorscale='Hot')
    data = [trace]
    layout = go.Layout(
        title='Regions with salt above Threshold' + ' ' + str(threshold) + '%',
        autosize=True,
        width=700,
        height=700,
        yaxis=dict(autorange='reversed')
    )
    graphJSON = (json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder), json.dumps(layout, cls=plotly.utils.PlotlyJSONEncoder))
    return graphJSON
