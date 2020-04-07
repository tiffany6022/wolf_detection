import os
from sys import argv
import json
import pickle

# Count how many photos in each episode
def count_ep(path):
    video = {}
    images = os.listdir(path)
    for img in images:
        if not video.__contains__(img[:4]):
            video[img[:4]] = 1
        else:
            video[img[:4]] = int(video[img[:4]]) + 1

    return video

# Count how many photos each role has
def count_role(path):
    total = 0
    wolf = 0
    civil = 0
    god = 0
    images = os.listdir(path)
    for img_name in images:
        total += 1
        pkl_path = os.path.join(os.path.dirname(__file__), 'details.pkl')
        with open(pkl_path, 'rb') as file:
            df = pickle.load(file)
        date_mask = df['date'] == img_name[:4]
        if df[date_mask]['role'].isin(['wolf']).bool():
            wolf += 1
        elif df[date_mask]['role'].isin(['god']).bool():
            god += 1
        elif df[date_mask]['role'].isin(['civilian']).bool():
            civil += 1

        # old-version
        # if img_name[:4] == '0524' or img_name[:4] == '0531' or img_name[:4] == '0628' or img_name[:4] == '0719' or img_name[:4] == '0807'\
        # or img_name[:4] == '0812' or img_name[:4] == '0815' or img_name[:4] == '0816' or img_name[:4] == '0925' or img_name[:4] == '1007'\
        # or img_name[:4] == '1213' or img_name[:4] == '0101' or img_name[:4] == '0113' or img_name[:4] == '0114' or img_name[:4] == '0120'\
        # or img_name[:4] == '0121' or img_name[:4] == '0210' or img_name[:4] == '0213' or img_name[:4] == '0220' or img_name[:4] == '0225'\
        # or img_name[:4] == '1115' or img_name[:4] == '0930' or img_name[:4] == '0916' or img_name[:4] == '0805' or img_name[:4] == '0731'\
        # or img_name[:4] == '0228' or img_name[:4] == '0722' or img_name[:4] == '0517' or img_name[:4] == '0115':
        #     wolf += 1
        # elif img_name[:4] == '1206' or img_name[:4] == '0701' or img_name[:4] == '0918' or img_name[:4] == '1014' or img_name[:4] == '1118':
        #     god += 1
        # else:
        #     civil += 1

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

if __name__ == '__main__':
    if len(argv) == 3:
        function = argv[1]
        path = argv[2]
    else:
        function = 'role'
        path = 'crop09'

    if function == 'ep':
        video = count_ep(path)
        print(json.dumps(video, indent = 4))
    elif function == 'role':
        wolf, god, civil, total = count_role(path)
        print(f"wolf:{wolf} god:{god} civil:{civil}")
        print(f"Wolf Probability:{wolf/total}")

