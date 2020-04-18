import os
import random
import shutil
import pickle
import random
import glob
from sys import argv
from count import count_role
import pandas as pd


# clear files in the directory
def clear(path1, path2, path3):
    shutil.rmtree(path1)
    os.mkdir(path1)
    shutil.rmtree(path2)
    os.mkdir(path2)
    shutil.rmtree(path3)
    os.mkdir(path3)

# random division
def randomly_divide(path, total, date_list):
    train_path = './division/ep2_rd8/train'
    validation_path = './division/ep2_rd8/validation'
    test_path = './division/ep2_rd8/test'
    clear(train_path, validation_path, test_path)

    images = []
    if len(date_list) == 0: # all
        images = glob.glob(f"./{path}/*")
    else:
        for i in range(len(date_list)):
            img = glob.glob(f'./{path}/{date_list[i]}*')
            images = images + img
    random.shuffle(images)
    images_num = total
    test_num = images_num / 5 # 1/5
    validation_num = images_num / 5 # 1/5
    train_num = images_num - test_num - validation_num # 3/5
    counter = 0

    for i in range(len(images)):
        counter += 1
        # i_path = f'./{path}/' + i
        if counter <= test_num:
           shutil.copy(images[i], test_path)
        elif counter > test_num and counter <= test_num + validation_num:
           shutil.copy(images[i], validation_path)
        else:
           shutil.copy(images[i], train_path)

# episode division
def episode_divide(df, path, wolf_total, good_total, ep_total):
    train_path = './division/ep2_rd8/validation'
    validation_path = './division/ep2_rd8/validation'
    test_path = './division/ep2_rd8/test'
    # clear(train_path, validation_path, test_path)

    # count how many images that test and val need
    test_wolf = val_wolf = wolf_total / 5
    test_good = val_good = good_total / 5

    # pick which episode and save
    tw_list, df = pick_ep(df, test_wolf, 'wolf', int(ep_total/5/2))
    tg_list, df = pick_ep(df, test_good, 'good', int(ep_total/5/2))
    vw_list, df = pick_ep(df, val_wolf, 'wolf', int(ep_total/5/2))
    vg_list, df = pick_ep(df, val_good, 'good', int(ep_total/5/2))
    save(tw_list, test_path, path, 0)
    save(tg_list, test_path, path, 0)
    save(vw_list, validation_path, path, 0)
    save(vg_list, validation_path, path, 0)
    train_list = []
    for index, row in df.iterrows():
        train_list.append(row['date'])
    save(train_list, train_path, path, 1)

def pick_ep(df, num, role, pick_ep_num):
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
    while(abs(distance) > 50):
        pick_num = 0
        get_eps = random.randint(pick_ep_num-2, pick_ep_num+2)
        pick_list = random.sample(list(role_dict.items()), k=get_eps)
        for i in pick_list:
            pick_num = pick_num + int(i[1])
        print(pick_num)
        distance = num - pick_num
    for i in pick_list:
        df = df[df['date'] != i[0]]
    return pick_list, df

def save(pick_list, save_path, path, is_train):
    for i in pick_list:
        if is_train:
            date = i
        else:
            date = i[0]
        from_path = f'./{path}/{date}*.jpg'
        save_list = glob.glob(from_path)
        for j in save_list:
            shutil.copy(j, save_path)

def proportionally_divide(percent, df, ep_total, total, path):
    ep_percent = percent
    rd_percent = 10 - percent
    ep_wolf = int(total * (ep_percent / 10) / 2)
    ep_good = int(total * (ep_percent / 10) / 2)
    ew_list, remain_df = pick_ep(df, ep_wolf, 'wolf', int(ep_total/2/2))
    eg_list, remain_df = pick_ep(remain_df, ep_good, 'good', int(ep_total/2/2))

    # random
    rd_date_list = remain_df['date'].tolist()
    rd_total = remain_df['num'].sum()
    randomly_divide(path, rd_total, rd_date_list)

    # episode
    pick_df = pd.DataFrame()
    for i in ew_list:
        pick_df = pick_df.append(df[df['date'] == i[0]], ignore_index=True)
    for i in eg_list:
        pick_df = pick_df.append(df[df['date'] == i[0]], ignore_index=True)
    print(pick_df)
    wolf_df = pick_df[pick_df['role'] == 'wolf']
    wolf = wolf_df['num'].sum()
    god_df = pick_df[pick_df['role'] == 'god']
    god = god_df['num'].sum()
    civil_df = pick_df[pick_df['role'] == 'civilian']
    civil = civil_df['num'].sum()
    episode_divide(pick_df, path, wolf, god+civil, ep_total-remain_df.shape[0])

if __name__ == '__main__':
    path = 'crop09'
    wolf, god, civil, total = count_role(path)

    # open dataframe in pickle
    pkl_path = os.path.join(os.path.dirname(__file__), 'details.pkl')
    with open(pkl_path, 'rb') as file:
        df = pickle.load(file)
    ep_total = df.shape[0]
    date_list = []

    if argv[1] == 'rd':
        randomly_divide(path, total, date_list)
    elif argv[1] == 'ep':
        episode_divide(df, path, wolf, god+civil, ep_total)
    elif argv[1] == 'pp':
        proportionally_divide(5, df, ep_total, total, path)

