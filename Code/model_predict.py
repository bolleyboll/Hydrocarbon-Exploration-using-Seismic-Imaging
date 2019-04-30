from keras.models import load_model
from PIL import Image
import numpy as np

w, h = 128, 128

UNET = load_model('model-tgs-salt-2.h5')
UNET.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


def predict_me(X, X_feat):

    Y = UNET.predict({'img': X, 'feat': X_feat})
    print(Y)
    Y = Y.squeeze() * 255
    Y = np.array([[thres(int(j), 70) for j in i] for i in Y])
    print(Y.shape)
    print(Y)
    im = Image.new('1', (w, h))
    im.putdata(Y)
    im.save('result.png')
    # img = Image.fromarray(Y)

    # img.show()
    return Y


def salt_proportion(imgArray):
    try:
        unique, counts = np.unique(imgArray, return_counts=True)
        # The total number of pixels is 101*101 = 10,201
        return counts[1] / 10201.

    except:
        return 0.0


def thres(x, t):
    if x >= t * 255 / 100:
        return 255
    else:
        return 0
