import math
import random
import matplotlib
from scipy.stats import ttest_ind, stats

matplotlib.rc('font',family='Microsoft YaHei')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import sklearn.preprocessing
from matplotlib.patches import Ellipse
from sklearn.cross_decomposition import PLSRegression
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans
from skimage.measure import EllipseModel

# data = pd.read_excel(
#     '../files/pollen files/results/process_output_quantid_pos_camera_noid/peaktablePOSout_POS_noid_replace.xlsx')
data = pd.read_excel('../files/pollen files/results/process_output_quantid_neg_camera_noid/peaktableNEGout_NEG_noid_replace.xlsx')
print(data)

sample_labels = []

color_exist = []
targets = data.columns.values[1:]

for i in range(len(targets)):
    if 'WX_' not in targets[i] and 'QX_' not in targets[i] and 'QXRY_' not in targets[i]:
        del data[targets[i]]
targets = data.columns.values[1:]
print(targets)

# 分别比较样本1和6、
keywords1 = ['XYCH_WX_', 'XYCH_QX_', 'XYCH_QXRY_']
# 样本2和7、
keywords2 = ['GYCH_WX_', 'GYCH_QX_', 'GYCH_QXRY_']
# 样本3和8、
keywords3 = ['GWBZ_WX_', 'GWBZ_QX_', 'GWBZ_QXRY_']
# 样本4和9、
keywords4 = ['GHH_WX_', 'GHH_QX_', 'GHH_QXRY_']
# 样本5和10
keywords5 = ['GCH_WX_', 'GCH_QX_', 'GCH_QXRY_']
# 研究单个样本破壁与未破壁的变化差异
keywords6 = ['WX_', 'QX_', 'QXRY']
x_index = []
y_index = []
z_index = []
keywords = keywords6

saved_label = data['dataMatrix'].values
print(saved_label)
del data['dataMatrix']

imputer_mean_XYCH_WX = SimpleImputer(missing_values=np.nan,strategy='mean')
data_impute = imputer_mean_XYCH_WX.fit_transform(data)


sum_baseline = 10000
for i in range(data_impute.shape[1]):
    coe = sum_baseline/np.sum(data_impute[:,i])
    data_impute[:, i] = (data_impute[:, i]*coe)/sum_baseline

normalized_data_impute = data_impute
print(normalized_data_impute)

x_index = []
y_index = []
z_index = []
print(targets)

for i in range(len(targets)):
    if keywords[0] in targets[i]:
        x_index.append(i)
    elif keywords[1] in targets[i]:
        y_index.append(i)
    elif keywords[2] in targets[i]:
        z_index.append(i)

print(x_index)
print(y_index)
print(z_index)
targets = np.hstack((targets[x_index], targets[y_index], targets[z_index]))
print(targets)
print(len(targets))

normalized_data_impute_x = []
for index in x_index:
    normalized_data_impute_x.append(normalized_data_impute[:,index].T)
normalized_data_impute_x = np.array(normalized_data_impute_x)

normalized_data_impute_y =[]
for index in y_index:
    normalized_data_impute_y.append(normalized_data_impute[:,index].T)
normalized_data_impute_y = np.array(normalized_data_impute_y)

normalized_data_impute_z = []
for index in z_index:
    normalized_data_impute_z.append(normalized_data_impute[:, index].T)
normalized_data_impute_z = np.array(normalized_data_impute_z)

top_k = 20
p_list = []
for i in range(normalized_data_impute_x.shape[1]):
    f, p = stats.f_oneway(normalized_data_impute_x[:, i:i + 1], normalized_data_impute_y[:, i:i + 1],
                          normalized_data_impute_z[:, i:i + 1])
    p_list.append(p[0])
p_list = np.array(p_list)
count = 0
for p in p_list:
    if p < 0.05:
        count += 1

top_k_index = p_list.argsort()[::-1][len(p_list) - top_k:]
print(top_k_index)
print(len(top_k_index))

# X_XYCH_WX = np.array(data_impute_XYCH_WX)
# X_GYCH_WX = np.array(data_impute_GYCH_WX)
X = np.vstack((normalized_data_impute_x,normalized_data_impute_y,normalized_data_impute_z))



X_top = []
sum_list = []

for row in range(X.shape[0]):
    sum = np.sum(X[row,:])
    temp = []
    for k in top_k_index:
        percentage = (X[row, k:k + 1]/sum) * 100
        temp.append(percentage[0])

    X_top.append(temp)



X_top = np.array(X_top)

X_top = X_top.reshape(top_k,X_top.shape[0])

labels = []
for i in top_k_index:
    labels.append(saved_label[i])
print(labels)




color_exist = []
def get_random_color(color_exist):
    r = lambda: random.randint(0, 255)
    color = '#%02X%02X%02X' % (r(), r(), r())
    while color in color_exist:
        r = lambda: random.randint(0, 255)
        color = '#%02X%02X%02X' % (r(), r(), r())
    color_exist.append(color)
    return color


fig,ax = plt.subplots()
plt.xticks(rotation = 90)
ax.bar(targets,X_top[0],0.2,label=labels[0])
for i in range(1,len(X_top)):
    ax.bar(targets,X_top[i],0.2,bottom=X_top[i-1],label=labels[i],color=get_random_color(color_exist))

plt.title('Histogram of the 20 most different metabolic distribution between groups')
ax.legend(bbox_to_anchor=(1, 1),prop={'size': 8},loc='best')
plt.show()