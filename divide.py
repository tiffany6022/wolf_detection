import os
import random
import shutil

path = './crop09'
# path = './09face'
images = os.listdir(path)

train_path = './division_crop/train'
validation_path = './division_crop/validation'
test_path = './division_crop/test'
# train_path = './division_ep/train'
# validation_path = './division_ep/validation'
# test_path = './division_ep/test'

# clear files in the directory
shutil.rmtree(train_path)
os.mkdir(train_path)
shutil.rmtree(validation_path)
os.mkdir(validation_path)
shutil.rmtree(test_path)
os.mkdir(test_path)

# random division
random.shuffle(images)
images_num = 1252
test_num = images_num / 5 # 1/5
validation_num = images_num / 5 # 1/5
train_num = images_num - test_num - validation_num # 3/5
counter = 0

for i in images:
    counter += 1
    # i_path = './09face/' + i
    i_path = './crop09/' + i
    if counter <= test_num:
       shutil.copy(i_path, test_path)
    elif counter > test_num and counter <= test_num + validation_num:
       shutil.copy(i_path, validation_path)
    else:
       shutil.copy(i_path, train_path)

'''
# episode division
for i in images:
    i_path = './09face/' + i
    if i[:4] == '1211' or i[:4] == '0203' or i[:4] == '0122' or i[:4] == '1213' or i[:4] == '0523' or i[:4] == '0531':
        shutil.copy(i_path, test_path)
    elif i[:4] == '0114' or i[:4] == '0815' or i[:4] == '0816' or i[:4] == '0911' or i[:4] == '0926' or i[:4] == '1029':
        shutil.copy(i_path, validation_path)
    elif i[:4] == '0210' or i[:4] == '0120' or i[:4] == '0101' or i[:4] == '0524' or i[:4] == '0628' or i[:4] == '0719'\
    or i[:4] == '0701' or i[:4] == '0729' or i[:4] == '0807' or i[:4] == '0812' or i[:4] == '0918' or i[:4] == '0925'\
    or i[:4] == '1007' or i[:4] == '1008' or i[:4] == '1014' or i[:4] == '1118' or i[:4] == '1206' or i[:4] == '1204':
        shutil.copy(i_path, train_path)
'''
