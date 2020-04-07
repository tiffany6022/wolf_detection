import pickle
import os
import glob
import pandas as pd
from count import count_ep

def build_list_videos(path):
    list_videos = []
    video = count_ep(path)
    path_list = glob.glob(r'./crop09/*.jpg')
    for img_path in path_list:
        name = os.path.basename(img_path)
        date = name[:4]

        # that day has already recorded then continue
        have_date = 0
        for v in list_videos:
            if v['date'] == date:
                have_date = 1
                break
        if have_date:
            continue

        # assign role
        if date == '0524' or date == '0531' or date == '0628' or date == '0719' or date == '0807'\
        or date == '0812' or date == '0815' or date == '0816' or date == '0925' or date == '1007'\
        or date == '1213' or date == '0101' or date == '0113' or date == '0114' or date == '0120'\
        or date == '0121' or date == '0210' or date == '0213' or date == '0220' or date == '0225'\
        or date == '1115' or date == '0930' or date == '0916' or date == '0805' or date == '0731'\
        or date == '0228' or date == '0722' or date == '0517' or date == '0115':
            img_role = "wolf"
        elif date == "0701" or date == "0918" or date == "1014" or date == "1118" or date == "1206":
            img_role = "god"
        else:
            img_role = "civilian"

        # number of images on that day
        num = video[date]
        dict09 = {'date': date, 'role': img_role, 'num': num}
        list_videos.append(dict09)

    return list_videos

if __name__ == '__main__':
    path = './crop09/'
    list_videos = build_list_videos(path)

    videos_df = pd.DataFrame(list_videos)
    videos_df.sort_values(by='date', ascending=True, inplace=True)
    videos_df.to_pickle("details.pkl")
    unpickled_df = pd.read_pickle("details.pkl")
    print(unpickled_df)

    # # pickle a variable to a file

    # file = open('details.pkl', 'wb')
    # pickle.dump(list_videos, file)
    # file.close()
    #
    # with open('details.pkl', 'rb') as file:
    #     a_dict = pickle.load(file)
    #
    # print(a_dict)

