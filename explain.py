from tensorflow.keras.models import load_model
from lime import lime_image
from skimage.segmentation import slic, mark_boundaries
from keras.preprocessing import image
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np
import random
import os


# two functions that lime image explainer requires
def predict(input):

    # Input: image tensor
    # Returns a predict function which returns the probabilities of labels ((7,) numpy array)
    # ex: return model(data).numpy()
    return model.predict(input)

def segmentation(input):
    # 利用 skimage 提供的 segmentation 將圖片分成 100 塊
    return slic(input, n_segments=100, compactness=1, sigma=1)


def explain(input, img, y, pred_class, imgclass, img_name):
    # Initiate explainer instance
    explainer = lime_image.LimeImageExplainer()
    # Get the explaination of an image
    explaination = explainer.explain_instance(
                                    image=img,
                                    classifier_fn=predict,
                                    segmentation_fn=segmentation
                                )

    # Get processed image
    lime_img, mask = explaination.get_image_and_mask(
                                        label=y,
                                        positive_only=False,
                                        hide_rest=False,
                                        num_features=5,
                                        min_weight=0.0
                                    )

    # save the image
    lime_img = lime_img.astype('float32')
    lime_img = lime_img / 255
    # y:real wolf == 1; pred_class: guess is wolf == 1; imgclass: use in train or test or val
    plt.imsave(f'./explanation/crop/{y}{pred_class}_{imgclass}_{img_name[:9]}.jpg', lime_img)
    # plt.imsave(f'./explanation/random/{clas}_{y}_{img_name[:9]}_mark.jpg', mark_boundaries(lime_img, mask))
    # plt.imsave(f'test.jpg', lime_img)

    pred = model.predict(input)[0][0]
    print(pred)
    if float(pred) > 0.99 or float(pred) < 0.01:
        plt.imsave(f'./explanation/crop_verysure/{y}{pred_class}_{imgclass}_{img_name[:9]}.jpg', lime_img)


# random select 30 images
def select(path, imgclass):
    images = os.listdir(path)
    random.shuffle(images)
    count = 0
    for img_name in images:
        count += 1
        if count == 30:
            return
        print(img_name)
        y = is_a_wolf(img_name)
        img_path = path + img_name
        img = image.load_img(img_path, target_size=(115, 160))
        img = image.img_to_array(img)
        input = np.expand_dims(img, axis=0)
        input = input.astype('float32')
        input = input / 255

        pred_class = model.predict_classes(input)
        # expand_input, array_image, label, train_test_val, img_name
        explain(input, img, y, int(pred_class), imgclass, img_name)


def is_a_wolf(img_name):
    if img_name[:4] == '0524' or img_name[:4] == '0531' or img_name[:4] == '0628' or img_name[:4] == '0719' or img_name[:4] == '0807'\
    or img_name[:4] == '0812' or img_name[:4] == '0815' or img_name[:4] == '0816' or img_name[:4] == '0925' or img_name[:4] == '1007'\
    or img_name[:4] == '0114' or img_name[:4] == '1213' or img_name[:4] == '0210' or img_name[:4] == '0120' or img_name[:4] == '0101':
        return 1
    else:
        return 0


if "__main__" == __name__:
    model = load_model('saved_models/crop_7layers_relu_dropout0.6')
    model.summary()

    select('./division_crop/train/', 'train')
    select('./division_crop/validation/', 'val')
    select('./division_crop/test/', 'test')
