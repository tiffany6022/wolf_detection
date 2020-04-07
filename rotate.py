from PIL import Image
import os
import shutil

def rotate(data):
    save_dir = './division/rotate'
    from_dir = './division/random2000'
    shutil.rmtree(f'{save_dir}/{data}')
    os.mkdir(f'{save_dir}/{data}')

    imgs = os.listdir(f"{from_dir}/{data}")

    for i in imgs:
        img_path = f"{from_dir}/{data}/{i}"
        save_path = f"{save_dir}/{data}/{i}"
        img = Image.open(img_path)
        img2 = img.rotate(180)
        img2.save(save_path)

if "__main__" == __name__:
    rotate('train')
    rotate('test')
    rotate('validation')
