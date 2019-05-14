from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from skimage.transform import resize
import numpy as np
import os
im_width = 128
im_height = 128
border = 5
im_chan = 2
n_features = 1


def pre_process_me(id_image, uploads=True):

    X = np.zeros((1, im_height, im_width, im_chan), dtype=np.float32)
    X_feat = np.zeros((n_features), dtype=np.float32)

    try:
        if uploads:
            img = load_img(os.path.join(os.getcwd(),"uploads",id_image), grayscale=True)
        else:

            img = load_img(os.path.join("Hydrocarbon-Exploration-using-Seismic-Imaging","data",'train',"images",id_image), grayscale=True)
        x_img = img_to_array(img)
        x_img = resize(x_img, (128, 128, 1), mode='constant', preserve_range=True)

        # Create cumsum x
        x_center_mean = x_img[border:-border, border:-border].mean()
        x_csum = (np.float32(x_img) - x_center_mean).cumsum(axis=0)
        x_csum -= x_csum[border:-border, border:-border].mean()
        x_csum /= max(1e-3, x_csum[border:-border, border:-border].std())

        # Save images
        X[0, ..., 0] = x_img.squeeze() / 255
        X[0, ..., 1] = x_csum.squeeze()
        print(X.shape)

        return X, X_feat
    except Exception as e:
        raise e


# X, X_feat= pre_process_me("000e218f21.png", "000e218f21.png")
# X, X_feat= pre_process_me("0aabdb423e.png", "0aabdb423e.png")
# X, X_feat= pre_process_me("0cc1d0e4c4.png", "0cc1d0e4c4.png")
# print(predict_me(X, X_feat, "0cc1d0e4c4.png", 70))
