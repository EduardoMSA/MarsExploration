import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pickle
import numpy as np 

def plotMaps(path):

    file_name = "map"
    inputFile = open('./Data/' + file_name + '.obj', 'rb')
    data = pickle.load(inputFile)

    map_data = np.load('./Data/map.npy')

    # Create figure and axes
    figure, axis = plt.subplots(2, 2)

    axis[0, 0].set_title(' Map ')
    axis[0, 0].set_xlabel('x*10 (m)')
    axis[0, 0].set_ylabel('y*10 (m)')
    axis[0, 0].imshow(map_data, cmap='hot', interpolation='nearest', aspect='auto')

    axis[0, 1].set_title(' Navigability Map ')
    axis[0, 1].set_xlabel('x*10 (m)')
    axis[0, 1].set_ylabel('y*10 (m)')
    axis[0, 1].imshow(map_data, cmap='hot', interpolation='nearest', aspect='auto')

    axis[1, 0].set_title(' Navigability Route ')
    axis[1, 0].set_xlabel('x*10 (m)')
    axis[1, 0].set_ylabel('y*10 (m)')
    axis[1, 0].imshow(map_data, cmap='hot', interpolation='nearest', aspect='auto')

    axis[1, 1].set_title(' Navigability Route Map ')
    axis[1, 1].set_xlabel('x*10 (m)')
    axis[1, 1].set_ylabel('y*10 (m)')
    axis[1, 1].imshow(map_data, cmap='hot', interpolation='nearest', aspect='auto')

    

    route = path
    if route:
        for i in route:
            rectangle = patches.Rectangle((i[1][1]*20, i[1][0]*20), 20, 20, fc='#0020ff',alpha=0.8)
            rectangle1 = patches.Rectangle((i[1][1]*20, i[1][0]*20), 20, 20, fc='#0020ff',alpha=0.8)
            axis[1, 0].add_artist(rectangle)
            axis[1, 1].add_artist(rectangle1)
    else:
        print('No Route')

    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            # print("{}/ {} /{}".format(i,j,data[i][j]))
            # Create a Rectangle patch
            if data[i][j] == 1:
                rectangle = plt.Rectangle((j*20,i*20), 20, 20, fc='#870000',alpha=0.5)
                rectangle1 = plt.Rectangle((j*20,i*20), 20, 20, fc='#870000',alpha=0.5)
                axis[0, 1].add_artist(rectangle)
                axis[1, 1].add_artist(rectangle1)
            elif data[i][j] == 2:
                rectangle = patches.Rectangle((j*20,i*20), 20, 20, fc='#ff0000',alpha=0.5)
                rectangle1 = patches.Rectangle((j*20,i*20), 20, 20, fc='#ff0000',alpha=0.5)
                axis[0, 1].add_artist(rectangle)
                axis[1, 1].add_artist(rectangle1)
            elif data[i][j] == 3:
                rectangle = plt.Rectangle((j*20,i*20), 20, 20, fc='#4aff00',alpha=0.5)
                rectangle1 = plt.Rectangle((j*20,i*20), 20, 20, fc='#4aff00',alpha=0.5)
                axis[0, 1].add_artist(rectangle)
                axis[1, 1].add_artist(rectangle1)
            elif data[i][j] == 4:
                rectangle = patches.Rectangle((j*20,i*20), 20, 20, fc='#268200',alpha=0.5)
                rectangle1 = patches.Rectangle((j*20,i*20), 20, 20, fc='#268200',alpha=0.5)
                axis[0, 1].add_artist(rectangle)
                axis[1, 1].add_artist(rectangle1)
            else:
                pass
        
    plt.show()