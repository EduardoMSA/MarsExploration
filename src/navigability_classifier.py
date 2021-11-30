import pickle
import numpy as np
from scipy.stats import kurtosis, skew
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_validate
from skimage.feature.texture import greycomatrix, greycoprops

def classify():
    file_name = "navigability"
    inputFile = open('./Data/' + file_name + '.obj', 'rb')
    data = pickle.load(inputFile)
    n_img = len(data)

    feature_names = ["Max slope", "Mean slope", "Slope variance", "Slope skewness", "Slope kurtosis",
                    "Max depression","Mean depression","Depression variance","Depression skewness","Depression kurtosis",
                    "Max rise", "Mean rise","Rise variance","Rise skewness", "Rise kurtosis",
                    "GLCM - Disimilaridad", "GLCM - Correlación"
                    ]

    n_features = len(feature_names)

    features = np.zeros([n_img,n_features])
    original_labels = np.zeros([n_img])

    for i in range(n_img):

        # 1 -> Muy poco navegable y poco navegable 
        # 2 -> Muy navegable y navegable

        label = data[i][0]
        original_labels[i] = label

        # Slope
        slope = data[i][3]
        features[i,2] = slope.max()
        features[i,3] = slope.mean()
        features[i,4] = slope.var()
        features[i,5] = skew(slope.flatten())
        features[i,6] = kurtosis(slope.flatten())

        # Depression
        depression = data[i][4]
        features[i,7] = depression.max()
        features[i,8] = depression.mean()
        features[i,9] = depression.var()
        features[i,10] = skew(depression.flatten())
        features[i,11] = kurtosis(depression.flatten())

        # Rise
        rise = data[i][5]
        features[i,12] = rise.max()
        features[i,13] = rise.mean()
        features[i,14] = rise.var()
        features[i,15] = skew(rise.flatten())
        features[i,16] = kurtosis(rise.flatten())

        # Data
        surface = (data[i][2]-data[i][2].min()).astype(int)
        glcm = greycomatrix(surface, distances=[5], angles=[0], levels=1024,
                            symmetric=True, normed=True)
        features[i, 0] = greycoprops(glcm, 'dissimilarity')[0,0]
        features[i, 1] = greycoprops(glcm, 'correlation')[0,0]

    x = features
    y = original_labels

    clf = KNeighborsClassifier(n_neighbors=5)
    print(x)
    print(x.shape)
    clf.fit(x, y)
    return clf

# data = [[ 3.59,0.69253314,2.55609441,0.93706393,0.09084556,1.58375285,
#   3.45249579,0.,0.,0.,0.,-3.,
#   0.,0.,0.,0.,-3.,]]

# print(classify().predict(data))

# print(y)

# kf = StratifiedKFold(n_splits=5, shuffle = True)
# # clf = svm.SVC(kernel = 'linear')
# # clf = svm.SVC(kernel = 'rbf')
# # clf = DecisionTreeClassifier(random_state=0)
# # clf = MLPClassifier(hidden_layer_sizes=(10), random_state=1, max_iter=10000)


# acc = 0
# recall = np.array([0., 0.])
# precision = np.array([0., 0.])

# for train_index, test_index in kf.split(x, y):

#     # Training phase
#     x_train = x[train_index, :]
#     y_train = y[train_index]
#     clf.fit(x_train, y_train)

#     # Test phase
#     x_test = x[test_index, :]
#     y_test = y[test_index]    
#     y_pred = clf.predict(x_test)

#     # Calculate confusion matrix and model performance
#     cm = confusion_matrix(y_test, y_pred)
#     print('Confusion matrix\n', cm)

#     acc += (cm[0,0]+cm[1,1])/len(y_test)

#     recall[0] += cm[0,0]/(cm[0,0] + cm[0,1])
#     recall[1] += cm[1,1]/(cm[1,0] + cm[1,1])

#     precision[0] += cm[0,0]/(cm[0,0] + cm[1,0])
#     precision[1] += cm[1,1]/(cm[0,1] + cm[1,1])

# # Print results
# acc = acc/5
# print('Acc: ', acc)

# precision = precision/5
# print('Precision: ', precision)

# recall = recall/5
# print('Recall: ', recall)
