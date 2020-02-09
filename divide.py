import os
import random
import shutil

path = './09face'
images = os.listdir(path)
random.shuffle(images)

train_path = './division/train'
validation_path = './division/validation'
test_path = './division/test'
# clear files in the directory
shutil.rmtree(train_path)
os.mkdir(train_path)
shutil.rmtree(validation_path)
os.mkdir(validation_path)
shutil.rmtree(test_path)
os.mkdir(test_path)

images_num = 828
test_num = images_num / 5 # 1/5
validation_num = images_num / 5 # 1/5
train_num = images_num - test_num - validation_num # 3/5
counter = 0

for i in images:
    counter += 1
    i_path = './09face/' + i
    if counter <= test_num:
       shutil.copy(i_path, test_path)
    elif counter > test_num and counter <= test_num + validation_num:
       shutil.copy(i_path, validation_path)
    else:
       shutil.copy(i_path, train_path)
