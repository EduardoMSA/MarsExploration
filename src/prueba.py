import pickle

file_name = "map"
inputFile = open('./Data/' + file_name + '.obj', 'rb')
data = pickle.load(inputFile)

print(data[500//20][500//20])