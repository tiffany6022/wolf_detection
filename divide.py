import os
import random
import shutil
import pickle
import random
import glob
from sys import argv
from count import count_role


# clear files in the directory
def clear(path1, path2, path3):
    shutil.rmtree(path1)
    os.mkdir(path1)
    shutil.rmtree(path2)
    os.mkdir(path2)
    shutil.rmtree(path3)
    os.mkdir(path3)

# random division
def randomly_divide(path, total):
    train_path = './division/random2000/train'
    validation_path = './division/random2000/validation'
    test_path = './division/random2000/test'
    clear(train_path, validation_path, test_path)

    images = os.listdir(path)
    random.shuffle(images)
    images_num = total
    test_num = images_num / 5 # 1/5
    validation_num = images_num / 5 # 1/5
    train_num = images_num - test_num - validation_num # 3/5
    counter = 0

    for i in images:
        counter += 1
        i_path = f'./{path}/' + i
        if counter <= test_num:
           shutil.copy(i_path, test_path)
        elif counter > test_num and counter <= test_num + validation_num:
           shutil.copy(i_path, validation_path)
        else:
           shutil.copy(i_path, train_path)

# episode division
def episode_divide(path, wolf_total, good_total):
    train_path = './division/episode2000/train'
    validation_path = './division/episode2000/validation'
    test_path = './division/episode2000/test'
    clear(train_path, validation_path, test_path)

    # count how many images that test and val need
    test_wolf = val_wolf = wolf_total / 5
    test_good = val_good = good_total / 5

    # open dataframe in pickle
    pkl_path = os.path.join(os.path.dirname(__file__), 'details.pkl')
    with open(pkl_path, 'rb') as file:
        df = pickle.load(file)

    # pick which episode and save
    tw_list, df = pick_ep(df, test_wolf, 'wolf')
    tg_list, df = pick_ep(df, test_good, 'good')
    vw_list, df = pick_ep(df, val_wolf, 'wolf')
    vg_list, df = pick_ep(df, val_good, 'good')
    save(tw_list, test_path)
    save(tg_list, test_path)
    save(vw_list, validation_path)
    save(vg_list, validation_path)
    train_list = []
    for index, row in df.iterrows():
        train_list.append(row['date'])
    save(train_list, train_path)

def pick_ep(df, num, role):
    # pick this role's dataframe and save in dict
    if role == 'wolf':
        role_df = df[df['role'] == 'wolf']
    elif role == 'good':
        mask_god = df['role'] == 'god'
        mask_civil = df['role'] == 'civilian'
        role_df = df[(mask_god | mask_civil)]
    role_dict = {}
    for index, row in role_df.iterrows():
        role_dict[row['date']] = row['num']

    # random add episode number to fit test or val needs
    pick_list = []
    distance = 100
    while(abs(distance) > 5):
        pick_num = 0
        get_eps = random.randint(3,7)
        pick_list = random.sample(list(role_dict.items()), k=get_eps)
        for i in pick_list:
            pick_num = pick_num + int(i[1])
        print(pick_num)
        distance = num - pick_num
    for i in pick_list:
        df = df[df['date'] != i[0]]
    return pick_list, df

def save(pick_list, save_path):
    for i in pick_list:
        if pick_list == 'train_list':
            date = i
        else:
            date = i[0]
        from_path = f'./{path}/{date}*.jpg'
        save_list = glob.glob(from_path)
        for j in save_list:
            shutil.copy(j, save_path)

# old-version
# for i in images:
#     i_path = './crop09/' + i
#     if i[:4] == '1211' or i[:4] == '0203' or i[:4] == '0122' or i[:4] == '1213' or i[:4] == '0523' or i[:4] == '0531':
#         shutil.copy(i_path, test_path)
#     elif i[:4] == '0114' or i[:4] == '0815' or i[:4] == '0816' or i[:4] == '0911' or i[:4] == '0926' or i[:4] == '1029':
#         shutil.copy(i_path, validation_path)
#     elif i[:4] == '0210' or i[:4] == '0120' or i[:4] == '0101' or i[:4] == '0524' or i[:4] == '0628' or i[:4] == '0719'\
#     or i[:4] == '0701' or i[:4] == '0729' or i[:4] == '0807' or i[:4] == '0812' or i[:4] == '0918' or i[:4] == '0925'\
#     or i[:4] == '1007' or i[:4] == '1008' or i[:4] == '1014' or i[:4] == '1118' or i[:4] == '1206' or i[:4] == '1204':
#         shutil.copy(i_path, train_path)
#

if __name__ == '__main__':
    path = 'crop09'
    wolf, god, civil, total = count_role(path)

    if argv[1] == 'random':
        randomly_divide(path, total)
    elif argv[1] == 'episode':
        episode_divide(path, wolf, god+civil)

