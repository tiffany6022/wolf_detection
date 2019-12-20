import os
import shutil
from facenet.upload import compare


def foldercompare(video):
    IMG_FOLDER = video
    path_list = os.listdir(IMG_FOLDER)

    newdir_path = os.path.join(IMG_FOLDER, "09chen")
    os.mkdir(newdir_path)

    for img2 in path_list:
        img2_path = os.path.join(IMG_FOLDER, img2)
        if img2.startswith('.'):
            continue
        if not os.path.isfile(img2_path):
            continue
        if not img1 == img2:
            continue
        try:
            diff = compare(img1_path, img2_path)
        except KeyboardInterrupt:
            os._exit()
        except:
            print("can't:", img2)
            continue
        if diff < 0.9:
            shutil.move(img2_path, newdir_path)
            print("img2:", img2)

    shutil.move(img1_path, newdir_path)
    print("end:\n", video)

img1 = "081209934_person_0.jpg"
img1_path = os.path.join('./', img1) # 09chen
foldercompare('./results')
