import os
import shutil
import glob
from upload import compare


def foldercompare(video):
    IMG_FOLDER = video
    # path_list = os.listdir(IMG_FOLDER)
    path_list = glob.glob(r'./results/*.jpg')
    # for py in path_list:
    #     print(py)

    newdir_path = os.path.join("./", "09chen")
    os.mkdir(newdir_path)

    for img2_path in path_list:
        # img2_path = os.path.join(IMG_FOLDER, img2)
        # if img2.startswith('.'):
        #     continue
        # if not os.path.isfile(img2_path):
        #     continue
        # if img1 == img2:
        #     continue
        try:
            diff = compare(img1_path, img2_path)
        except AttributeError:
            print("can't:", img2_path)
            continue
        if diff < 0.9:
            shutil.move(img2_path, newdir_path)
            print("img2:", img2_path)

    # shutil.move(img1_path, newdir_path)
    print("end:\n", video)

img1 = "081209934_person_0.jpg"
img1_path = os.path.join('./', img1) # 09chen
foldercompare('./results')
