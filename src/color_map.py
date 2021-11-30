import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import pickle
import numpy as np 
from rover import PredictPath

file_name = "map"
inputFile = open('./Data/' + file_name + '.obj', 'rb')
data = pickle.load(inputFile)

map_data = np.load('./Data/map.npy')

# Create figure and axes
fig, (ax1, ax2) = plt.subplots(1,2)

ax1.set_title('Mapa')
ax1.set_xlabel('x (m)')
ax1.set_ylabel('y (m)')

# Display the image
ax2.imshow(map_data, cmap='hot', interpolation='nearest', aspect='auto')
ax1.imshow(map_data, cmap='hot', interpolation='nearest', aspect='auto')

origin = 4800,3000
destination = 5000, 10000

rover = PredictPath(origin,destination)

route = rover.result.path()

for i in route:
    rectangle = patches.Rectangle((i[1][1]*20, i[1][0]*20), 20, 20, fc='#0020ff',alpha=0.8)
    ax2.add_artist(rectangle)

for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        # print("{}/ {} /{}".format(i,j,data[i][j]))
        # Create a Rectangle patch
        if data[i][j] == 1:
            rectangle = plt.Rectangle((j*20,i*20), 20, 20, fc='#870000',alpha=0.5)
            ax2.add_artist(rectangle)
        elif data[i][j] == 2:
            rectangle = patches.Rectangle((j*20,i*20), 20, 20, fc='#ff0000',alpha=0.5)
            ax2.add_artist(rectangle)
        elif data[i][j] == 3:
            rectangle = plt.Rectangle((j*20,i*20), 20, 20, fc='#4aff00',alpha=0.5)
            ax2.add_artist(rectangle)
        elif data[i][j] == 4:
            rectangle = patches.Rectangle((j*20,i*20), 20, 20, fc='#268200',alpha=0.5)
            ax2.add_artist(rectangle)
        else:
            pass
    
plt.show()