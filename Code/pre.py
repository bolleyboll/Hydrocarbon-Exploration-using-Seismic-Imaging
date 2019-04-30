from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from skimage.transform import resize
import numpy as np
from model_predict import *
im_width = 128
im_height = 128
border = 5
im_chan = 2
n_features = 1


def pre_process_me(id_image, id_mask):

    # Get and resize train images and masks

    X = np.zeros((1, im_height, im_width, im_chan), dtype=np.float32)
    y = np.zeros((1, im_height, im_width, 1), dtype=np.float32)
    X_feat = np.zeros((n_features), dtype=np.float32)

    try:

        img = load_img('D:\\Github Repos\\Hydrocarbon-Exploration-using-Seismic-Imaging\\Code\\uploads\\' + id_image, grayscale=True)
        x_img = img_to_array(img)
        x_img = resize(x_img, (128, 128, 1), mode='constant', preserve_range=True)

        # Create cumsum x
        x_center_mean = x_img[border:-border, border:-border].mean()
        x_csum = (np.float32(x_img) - x_center_mean).cumsum(axis=0)
        x_csum -= x_csum[border:-border, border:-border].mean()
        x_csum /= max(1e-3, x_csum[border:-border, border:-border].std())

        # Load Y
        mask = img_to_array(load_img('D:\\Github Repos\\Hydrocarbon-Exploration-using-Seismic-Imaging\\Code\\masks\\' + id_mask, grayscale=True))
        mask = resize(mask, (128, 128, 1), mode='constant', preserve_range=True)

        # Save images
        X[0, ..., 0] = x_img.squeeze() / 255
        X[0, ..., 1] = x_csum.squeeze()
        y = mask / 255

        return X, X_feat, y
    except Exception as e:
        raise e


# X, X_feat, Y = pre_process_me("000e218f21.png", "000e218f21.png")
# X, X_feat, Y = pre_process_me("0aabdb423e.png", "0aabdb423e.png")
X, X_feat, Y = pre_process_me("0cc1d0e4c4.png", "0cc1d0e4c4.png")
print(predict_me(X, X_feat))
