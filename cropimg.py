from PIL import Image
import os


imgs = os.listdir("./09face")

for i in imgs:
    img_path = "./09face/" + i
    save_path = "./crop09/" + i
    img = Image.open(img_path)
    w, h = img.size
    img2 = img.crop((0, 45, w, h))
    img2.save(save_path)
