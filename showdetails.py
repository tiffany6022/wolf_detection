import pickle

with open('details.pkl', 'rb') as file:
    a_dict =pickle.load(file)

print(a_dict)
