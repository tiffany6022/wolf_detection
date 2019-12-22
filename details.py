import pickle
import os
import glob

dicts = []
path_list = glob.glob(r'./09face/*.jpg')
for img_path in path_list:
    name = os.path.basename(img_path)
    date = name[:4]
    if date == "0523" or date == "0729" or date == "0911" or date == "0926" or date == "1008" or date == "1029":
        img_id = "civilian"
    elif date == "0701" or date == "0918" or date == "1014" or date == "1118":
        img_id = "god"
    else:
        img_id = "wolf"
    if date == "0524" or date == "0729" or date == "0812" or date == "0911" or date == "0925":
        result = "lose"
    else:
        result = "win"
    dict09 = {'photo': name, 'date': date, 'id': img_id, 'result': result}
    dicts.append(dict09)
    print(dict09)

# pickle a variable to a file
file = open('details.pkl', 'wb')
pickle.dump(dicts, file)
file.close()

'''
with open('details.pkl', 'rb') as file:
    a_dict =pickle.load(file)

print(a_dict)
'''
