import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import imageio
import os
from model_predict import predict_me
from pre import pre_process_me
from matplotlib.patches import Rectangle


class Generate_Result():
    root_path = "D:\\Hydrocarbon-Exploration-using-Seismic-Imaging\\data\\train"

    def __init__(self, list_of_images, thres):

        self.list_of_images = list_of_images
        self.thres = thres
        self.train_mask = pd.read_csv('D:\\Hydrocarbon-Exploration-using-Seismic-Imaging\\data\\train.csv')
        self.file_list = list(self.train_mask['id'].values)

    def gen_res(self):

        f, axarr = plt.subplots(len(self.list_of_images), 2 + len(self.thres), figsize=(10,10))
        left  = 0.125  # the left side of the subplots of the figure
        right = 0.9    # the right side of the subplots of the figure
        bottom = 0.1   # the bottom of the subplots of the figure
        top = 0.9      # the top of the subplots of the figure
        wspace = 0.4   # the amount of width reserved for space between subplots,
               # expressed as a fraction of the average axis width
        hspace = 0.2   # the amount of height reserved for space between subplots,
               # expressed as a fraction of the average axis height
        f.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)
        i, j = 0, 0
        for index in self.list_of_images:
            j = 0
            file_id = self.file_list[index]
            image, mask = self._getImageMask(file_id)
            print("HENLO")
            axarr[i][j].imshow(image)
            axarr[i][j].grid()
            axarr[i][j].set_title('Image', size=14)
            j += 1
            axarr[i][j].grid()
            axarr[i][j].set_title('Ground Truth', size=14)
            axarr[i][j].imshow(mask, cmap='gray')
            print("BOIIIII")
            j += 1
            X, X_feat = pre_process_me(file_id + ".png", uploads=False)
            for en,t in enumerate(self.thres):
                print("HELLLL")
                d={0:'A', 1:'B', 2:'C'}
                salt_prop, mask_graph, _ = predict_me(X, X_feat, "0cc1d0e4c4.png", t, gen_results=True)
                axarr[i][j].imshow(mask_graph, cmap='hot', interpolation='nearest')
                axarr[i][j].grid()
                axarr[i][j].set_title(d[en], size=14)
                j += 1
            i += 1
        
        extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
        f.legend([extra,extra,extra], ("Genrated Result for 50%: A","Genrated Result for 60%: B","Genrated Result for 70%: C"))
        #f.suptitle('Results', fontsize=20)
        extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
        # f.legend(['Title 1', d[0], 'Title 2', line2], ['', 'Line 1', '', 'Line 2'],
        #    handler_map={basestring: LegendTitle({'fontsize': 18})}, loc='lower right', bbox_to_anchor=(0.5, -0.05),&nbsp; shadow=True, ncol=2)
        f.show()
        f.savefig('result' + str(np.random.randint(0, 1000)) + '.png')

    def _getImageMask(self,file_id):

        image_folder = os.path.join(Generate_Result.root_path, "images")
        image_path = image_folder + "\\" + file_id + ".png"
        mask_folder = os.path.join(self.root_path, "masks")
        mask_path = mask_folder + "\\" + file_id + ".png"
        image = np.array(imageio.imread(image_path), dtype=np.uint8)
        mask = np.array(imageio.imread(mask_path), dtype=np.uint8)
        return image, mask

ob=Generate_Result([12,23,53,69,520],[30,50,90])
ob.gen_res()