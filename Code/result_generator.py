import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import imageio
from model_predict import predict_me
from pre import pre_process_me


class Generate_Result():
    root_path = ""
    thres = []

    def __init__(self, list_of_images, thres):

        self.list_of_images = list_of_images
        self.thres = thres
        self.train_mask = pd.read_csv('D:\\Datasets\\tgs-salt-identification-challenge\\train.csv')
        file_list = list(train_mask['id'].values)

    def gen_res():
        f, axarr = plt.subplots(len(self.list_of_images), 2 + len(thres))
        i, j = 0
        for index in self.list_of_images:
            j = 0
            file_id = self.file_list[index]
            image, mask = self._getImageMask(file_id)
            axarr[i][j].imshow(image)
            axarr[i][j].grid()
            axarr[i][j].set_title('Image')
            j += 1
            axarr[i][j].grid()
            axarr[i][j].set_title('Ground Truth')
            axarr[i][j].imshow(mask)
            j += 1
            X, X_feat = pre_process_me(file_id + ".png", uploads=False)
            for t in thres:
                salt_prop, mask_graph, _ = predict_me(X, X_feat, "0cc1d0e4c4.png", t)
                axarr[i][j].imshow(mask_graph)
                axarr[i][j].grid()
                axarr[i][j].set_title('Generated Result with Threshold of ' + str(t) + '%')
                j += 1
            i += 1
        f.show()
        f.savefig('result' + str(np.random.randint(0, 1000)) + '.png')

    def _getImageMask(file_id):

        image_folder = os.path.join(Generate_Result.root_path, "images")
        image_path = image_folder + "\\" + file_id + ".png"
        mask_folder = os.path.join(self.root_path, "masks")
        mask_path = mask_folder + "\\" + file_id + ".png"
        image = np.array(imageio.imread(image_path), dtype=np.uint8)
        mask = np.array(imageio.imread(mask_path), dtype=np.uint8)
        return image, mask
