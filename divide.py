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
def randomly_divide(path, dir_name, images_num, date_list):
    train_path = f'./division/{dir_name}/train'
    validation_path = f'./division/{dir_name}/validation'
    test_path = f'./division/{dir_name}/test'
    # clear(train_path, validation_path, test_path)

    images = []
    if len(date_list) == 0: # all
        images = glob.glob(f"./{path}/*")
    else: # partially use randomly_divide
        for i in range(len(date_list)):
            img = glob.glob(f'./{path}/{date_list[i]}*')
            images.extend(img)
    random.shuffle(images)
    test_num = images_num / 5 # 1/5
    validation_num = images_num / 5 # 1/5
    train_num = images_num - test_num - validation_num # 3/5
    counter = 0

    for i in range(len(images)):
        counter += 1
        if counter <= test_num:
           shutil.copy(images[i], test_path)
        elif counter > test_num and counter <= test_num + validation_num:
           shutil.copy(images[i], validation_path)
        else:
           shutil.copy(images[i], train_path)

# episode division
def episode_divide(df, path, dir_name, wolf_total, good_total, episode_total):
    train_path = f'./division/{dir_name}/train'
    validation_path = f'./division/{dir_name}/validation'
    test_path = f'./division/{dir_name}/test'
    clear(train_path, validation_path, test_path)

    # count how many images that test and val need (the rest are train's)
    test_wolf_num = val_wolf_num = wolf_total / 5
    test_good_num = val_good_num = good_total / 5

    # pick which episodes and save
    test_wolf_list, remaining_df = pick_ep(df, test_wolf_num, 'wolf', int(episode_total/5/2))
    test_good_list, remaining_df = pick_ep(remaining_df, test_good_num, 'good', int(episode_total/5/2))
    val_wolf_list, remaining_df = pick_ep(remaining_df, val_wolf_num, 'wolf', int(episode_total/5/2))
    val_good_list, remaining_df = pick_ep(remaining_df, val_good_num, 'good', int(episode_total/5/2))
    save(test_wolf_list, test_path, path)
    save(test_good_list, test_path, path)
    save(val_wolf_list, validation_path, path)
    save(val_good_list, validation_path, path)

    # the rest are train's
    train_list = []
    for index, row in remaining_df.iterrows():
        train_list.append(row['date'])
    save(train_list, train_path, path)


def pick_ep(df, target_num, role, pick_ep_num):
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
    while(abs(distance) > 30):
        pick_num = 0
        get_eps = random.randint(pick_ep_num-2, pick_ep_num+2)
        pick_list = random.sample(list(role_dict.items()), k=get_eps) # [('0918', 76), ('0206', 49), ('0320', 19), ('1206', 46)...]
        for i in pick_list:
            pick_num = pick_num + int(i[1])
        print(pick_num)
        distance = target_num - pick_num

    # return remaining dataframe
    pick_date_list = list(dict(pick_list).keys()) # pick date ['0918', '0206', '0320', '1206', ...]
    for date in pick_date_list:
        df = df[df['date'] != date]
    return pick_date_list, df

def save(pick_list, save_path, from_path):
    for date in pick_list:
        episode_images = glob.glob(f'./{from_path}/{date}*.jpg')
        for img in episode_images:
            shutil.copy(img, save_path)

def proportionally_divide(percent, df, path, dir_path, total, episode_total):
    ep_percent = percent
    rd_percent = 10 - percent

    # episode
    ep_wolf_num = int(total * (ep_percent / 10) / 2)
    ep_good_num = int(total * (ep_percent / 10) / 2)
    ep_wolf_list, remaining_df = pick_ep(df, ep_wolf_num, 'wolf', int(episode_total * (ep_percent / 10) / 2))
    ep_good_list, remaining_df = pick_ep(remaining_df, ep_good_num, 'good', int(episode_total * (ep_percent / 10) / 2))

    # build episode dataframe to episode_divide
    pick_df = pd.DataFrame()
    for date in ep_wolf_list:
        pick_df = pick_df.append(df[df['date'] == date], ignore_index=True)
    for date in ep_good_list:
        pick_df = pick_df.append(df[df['date'] == date], ignore_index=True)
    wolf_df = pick_df[pick_df['role'] == 'wolf']
    wolf = wolf_df['num'].sum()
    god_df = pick_df[pick_df['role'] == 'god']
    god = god_df['num'].sum()
    civil_df = pick_df[pick_df['role'] == 'civilian']
    civil = civil_df['num'].sum()
    episode_divide(pick_df, path, dir_path, wolf, god+civil, episode_total-remaining_df.shape[0])

    # random
    rd_date_list = remaining_df['date'].tolist()
    rd_total = remaining_df['num'].sum()
    randomly_divide(path, dir_path, rd_total, rd_date_list)

if __name__ == '__main__':
    path = 'crop09'
    dir_path = 'test'
    date_list = []

    # open dataframe in pickle
    pkl_path = os.path.join(os.path.dirname(__file__), 'details.pkl')
    with open(pkl_path, 'rb') as file:
        df = pickle.load(file)
    wolf, god, civil, total = count_role(path, df)
    episode_total = df.shape[0]

    if argv[1] == 'rd':
        randomly_divide(path, dir_path, total, date_list)
    elif argv[1] == 'ep':
        episode_divide(df, path, dir_path, wolf, god+civil, episode_total)
    elif argv[1] == 'pp':
        proportionally_divide(5, df, path, dir_path, total, episode_total)

