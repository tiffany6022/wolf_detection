import os
from sys import argv
import json
import pickle

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

# Count how many photos in each episode
def count_eps_images(path):
    video = {}
    images = os.listdir(path)
    for img in images:
        if not video.__contains__(img[:4]):
            video[img[:4]] = 1
        else:
            video[img[:4]] = int(video[img[:4]]) + 1

    return video

# Count how many photos each role has
def count_role(path, df):
    total = 0
    wolf = 0
    civil = 0
    god = 0
    images = os.listdir(path)
    for img_name in images:
        total += 1
        date_mask = df['date'] == img_name[:4]
        if df[date_mask]['role'].isin(['wolf']).bool():
            wolf += 1
        elif df[date_mask]['role'].isin(['god']).bool():
            god += 1
        elif df[date_mask]['role'].isin(['civilian']).bool():
            civil += 1

    return wolf, god, civil, total

# # count all images role in pickle
# def count_pickle_role():
#     pkl_path = os.path.join(os.path.dirname(__file__), 'details.pkl')
#     with open(pkl_path, 'rb') as file:
#         df = pickle.load(file)
#     wolf = df[( df["role"] == "wolf" )]['num'].sum()
#     god = df[( df["role"] == "god" )]['num'].sum()
#     civil = df[( df["role"] == "civilian" )]['num'].sum()
#     total = df['num'].sum()
#     print(f"wolf:{wolf} god:{god} civil:{civil}")
#     print(f"Wolf Probability:{wolf/total}")

# in order to varify that I didn't divide wrong proportion
def count_proportion(dir_path, df):

    # record random videos
    random_date = []
    train_eps_images = count_eps_images(dir_path + 'train') # dict
    test_eps_images = count_eps_images(dir_path + 'test')
    val_eps_images = count_eps_images(dir_path + 'validation')

    # print(list(train_eps_images.keys()))......question1
    random_date.extend(intersection(train_eps_images, test_eps_images))
    random_date.extend(intersection(train_eps_images, val_eps_images))
    random_date.extend(intersection(test_eps_images, val_eps_images))
    random_date = list(dict.fromkeys(random_date)) # delete duplicate date
    print(f"random: {random_date}")

    # calculate ep?_rd? proportion (train, test, validation)
    print("train, test, validation:")
    wolf_list = df[df['role'] == 'wolf']['date'].tolist()
    for dataset_eps_images in [train_eps_images, test_eps_images, val_eps_images]:
        rd_num = ep_num = rd_num_wolf = 0
        for date,num in dataset_eps_images.items():
            if date in random_date:
                rd_num = rd_num + num
                if date in wolf_list:
                    rd_num_wolf = rd_num_wolf + num
            else: ep_num = ep_num + num

        print(f"rd: {rd_num/(rd_num+ep_num)}")
        print(f"rd_wolf {rd_num_wolf/(rd_num+ep_num)}")

    # for k in test_eps_images.keys():
    #     if k in random_date: continue
    #     if train_eps_images.__contains__(k): random_date.append(k)
    # for k in train_eps_images.keys():
    #     if k in random_date: continue
    #     if val_eps_images.__contains__(k): random_date.append(k)
    # for k in val_eps_images.keys():
    #     if k in random_date: continue
    #     if test_eps_images.__contains__(k): random_date.append(k)

    # train_rd = train_ep = train_rd_wolf = 0
    # test_rd = test_ep = test_rd_wolf  = 0
    # val_rd = val_ep = val_rd_wolf  = 0

    # for k,v in train_eps_images.items():
    #     if k in random_date:
    #         train_rd = train_rd + v
    #         if k in wolf_list:
    #             train_rd_wolf = train_rd_wolf + v
    #     else: train_ep = train_ep + v
    # for k,v in test_eps_images.items():
    #     if k in random_date:
    #         test_rd = test_rd + v
    #         if k in wolf_list:
    #             test_rd_wolf = test_rd_wolf + v
    #     else: test_ep = test_ep + v
    # for k,v in val_eps_images.items():
    #     if k in random_date:
    #         val_rd = val_rd + v
    #         if k in wolf_list:
    #             val_rd_wolf = val_rd_wolf + v
    #     else: val_ep = val_ep + v
    # print(f"train(rd): {train_rd/(train_rd+train_ep)}")
    # print(f"test(rd): {test_rd/(test_rd+test_ep)}")
    # print(f"val(rd): {val_rd/(val_rd+val_ep)}")
    # print(f"train_wolf(rd) {train_rd_wolf/(train_rd+train_ep)}")
    # print(f"test_wolf(rd) {test_rd_wolf/(test_rd+test_ep)}")
    # print(f"val_wolf(rd) {val_rd_wolf/(val_rd+val_ep)}")


if __name__ == '__main__':

    pkl_path = os.path.join(os.path.dirname(__file__), 'details.pkl')
    with open(pkl_path, 'rb') as file:
        df = pickle.load(file)

    if len(argv) == 3:
        function = argv[1]
        path = argv[2]
    else:
        function = 'role'
        path = 'crop09'

    if function == 'ep':
        video = count_eps_images(path)
        print(json.dumps(video, indent = 4))
    elif function == 'role':
        wolf, god, civil, total = count_role(path, df)
        print(f"wolf:{wolf} god:{god} civil:{civil}")
        print(f"Wolf Probability:{wolf/total}")
    elif function == 'pp':
        count_proportion(path, df)

