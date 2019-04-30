from keras.models import load_model
from PIL import Image
import numpy as np

w, h = 128, 128

UNET = load_model('model-tgs-salt-2.h5')
UNET.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


def predict_me(X, X_feat, file_name):
    Y = UNET.predict({'img': X, 'feat': X_feat})
    Y = Y.squeeze() * 255
    img = Image.fromarray(data, '1')
    img.save('result_.png')
    img.show()
    return Y
