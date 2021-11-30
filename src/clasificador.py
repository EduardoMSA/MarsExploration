#------------------------------------------------------------------------------------------------------------------
#   Nav Clasification
#------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------
#   Imports
#------------------------------------------------------------------------------------------------------------------
import pickle
import numpy as np
from scipy.stats import kurtosis, skew

import richdem as rd

from skimage.transform import downscale_local_mean
from navigability_classifier import classify
from skimage.feature.texture import greycomatrix, greycoprops

#------------------------------------------------------------------------------------------------------------------
#   Configuration
#------------------------------------------------------------------------------------------------------------------

file_name = "./Data/map.IMG"   # Data file

n_img = 5                           # Number of images

subimg_size = 20                    # Image size

# Types of terrains
terrains = ('Indefinido', 'Muy poco navegable', 'Poco navegable', 
            'Navegable', 'Muy navegable')

#------------------------------------------------------------------------------------------------------------------
#   Surface map
#------------------------------------------------------------------------------------------------------------------

data_file = open(file_name, "rb")

endHeader = False;
while not endHeader:
    line = data_file.readline().rstrip().lower()

    sep_line = line.split(b'=')
       
    if len(sep_line) == 2:
        itemName = sep_line[0].rstrip().lstrip()
        itemValue = sep_line[1].rstrip().lstrip()

        if itemName == b'valid_maximum':
            maxV = float(itemValue)
        elif itemName == b'valid_minimum':
            minV = float(itemValue)
        elif itemName == b'lines':
            n_rows = int(itemValue)
        elif itemName == b'line_samples':
            n_columns = int(itemValue)
        elif itemName == b'map_scale':
            scale_str = itemValue.split()
            if len(scale_str) > 1:
                scale = float(scale_str[0])

    elif line == b'end':
        endHeader = True
        char = 0
        while char == 0 or char == 32:
            char = data_file.read(1)[0]      
        pos = data_file.seek(-1, 1)

image_size = n_rows*n_columns
data = data_file.read(4*image_size)

surface = np.frombuffer(data, dtype=np.dtype('f'))
surface = surface.reshape((n_rows, n_columns))
surface = np.array(surface)
surface = surface.astype('float64')

surface = surface - minV;
surface[surface < -10000] = -1;

sub_rate = round(10/scale)            
surface = downscale_local_mean(surface, (sub_rate, sub_rate))
surface[surface<0] = -1

new_scale = scale*sub_rate
new_n_rows = surface.shape[0]
new_n_columns = surface.shape[1]

inverted_surface = surface * (-1.0) + surface.max()
inverted_surface[surface<0] = -1

rda1 = rd.rdarray(surface, no_data=-1)
rda2 = rd.rdarray(inverted_surface, no_data=-1)

slope = rd.TerrainAttribute(rda1, attrib='slope_riserun')
slope[surface<0] = -1;

depression = rd.FillDepressions(rda1, epsilon=True, in_place=False) - rda1
depression[surface<0] = -1;

rise = rd.FillDepressions(rda2, epsilon=True, in_place=False) - rda2
rise[surface<0] = -1;

images = np.zeros([(new_n_rows//20)+1,(new_n_columns//20)+1])
print(images)
clf = classify()

for i in range(0,new_n_rows,20):

    for j in range(0,new_n_columns,20):

        subimg_row = i
        subimg_column = j
        print('{} - {}'.format(subimg_row,subimg_column))
        surface_section = surface[subimg_row:(subimg_row+subimg_size), subimg_column:(subimg_column+subimg_size)]
        slope_section = slope[subimg_row:(subimg_row+subimg_size), subimg_column:(subimg_column+subimg_size)]
        depression_section = depression[subimg_row:(subimg_row+subimg_size), subimg_column:(subimg_column+subimg_size)]
        rise_section = rise[subimg_row:(subimg_row+subimg_size), subimg_column:(subimg_column+subimg_size)]

        features = np.zeros([17])

        # Slope
        features[2] = slope_section.max()
        features[3] = slope_section.mean()
        features[4] = slope_section.var()
        features[5] = skew(slope_section.flatten())
        features[6] = kurtosis(slope_section.flatten())

        # Depression
        features[7] = depression_section.max()
        features[8] = depression_section.mean()
        features[9] = depression_section.var()
        features[10] = skew(depression_section.flatten())
        features[11] = kurtosis(depression_section.flatten())

        # Rise
        features[12] = rise_section.max()
        features[13] = rise_section.mean()
        features[14] = rise_section.var()
        features[15] = skew(rise_section.flatten())
        features[16] = kurtosis(rise_section.flatten())

        # Data
        surf = (surface_section-surface_section.min()).astype(int)
        glcm = greycomatrix(surf, distances=[5], angles=[0], levels=1024,
                            symmetric=True, normed=True)
        features[0] = greycoprops(glcm, 'dissimilarity')[0,0]
        features[1] = greycoprops(glcm, 'correlation')[0,0]

        print(features)

        label = 0

        if (subimg_row + subimg_size) < new_n_rows and (subimg_column + subimg_size) < new_n_columns:        
            if surface_section.min() > 0:
                label = int(clf.predict([features])[0])
                
        print(label)

        images[subimg_row//20][subimg_column//20] = label

outputFile = open('./Data/map.obj', 'wb')
pickle.dump(images, outputFile)
outputFile.close()
    

#------------------------------------------------------------------------------------------------------------------
#   End of file
#------------------------------------------------------------------------------------------------------------------

