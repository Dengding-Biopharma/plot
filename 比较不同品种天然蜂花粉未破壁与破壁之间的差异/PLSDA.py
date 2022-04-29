import math
import random
import matplotlib
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

data = pd.read_excel('../files/pollen files/results/process_output_quantid_pos_camera_noid/peaktablePOSout_POS_noid_replace.xlsx')
# data = pd.reXYCH_WX_excel('../files/pollen files/results/process_output_quantid_neg_camera_noid/peaktableNEGout_NEG_noid_replace.xlsx')
print(data)

sample_labels = []


color_exist = []
targets = data.columns.values[1:]


for i in range(len(targets)):
    if 'WX' not in targets[i]:
        del data[targets[i]]
targets = data.columns.values[1:]
print(targets)


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

# 分别比较样本1和6、
keywords1 = ['XYCH_WX_','XYCH_WXPB_']
# 样本2和7、
keywords2 = ['GYCH_WX_','GYCH_WXPB_']
# 样本3和8、
keywords3 = ['GWBZ_WX_','GWBZ_WXPB_']
# 样本4和9、
keywords4 = ['GHH_WX_','GHH_WXPB_']
# 样本5和10
keywords5 = ['GCH_WX_','GCH_WXPB_']
# 研究单个样本破壁与未破壁的变化差异
keywords6 = ['WX_','WXPB_']
x_index=[]
y_index=[]
print(targets)
keywords = keywords6
for i in range(len(targets)):
    if keywords[0] in targets[i]:
        x_index.append(i)
    elif keywords[1] in targets[i]:
        y_index.append(i)

print(x_index)
print(y_index)
targets = np.hstack((targets[x_index],targets[y_index]))
print(targets)
for i in range(len(targets)):
    if 'WX_' in targets[i]:
        targets[i] = 'WX_group'
    elif 'WXPB_' in targets[i]:
        targets[i] = 'WXPB_group'

normalized_data_impute_x = []
for index in x_index:
    normalized_data_impute_x.append(normalized_data_impute[:,index].T)
normalized_data_impute_x = np.array(normalized_data_impute_x)

normalized_data_impute_y =[]
for index in y_index:
    normalized_data_impute_y.append(normalized_data_impute[:,index].T)
normalized_data_impute_y = np.array(normalized_data_impute_y)

print(normalized_data_impute_x.shape)
print(normalized_data_impute_y.shape)

X_XYCH_WX = np.array(normalized_data_impute_x)
X_GYCH_WX = np.array(normalized_data_impute_y)
X = np.vstack((X_XYCH_WX,X_GYCH_WX))
print(X)
int_targets = []
for i in targets:
    if 'WX_' in i:
        int_targets.append(0)
    elif 'WXPB_':
        int_targets.append(1)


print(X.shape)

plsr = PLSRegression(n_components=2,scale=False)
plsr.fit(X,int_targets)

print(plsr.predict(X))
predicts = []
for predict in plsr.predict(X):
    if predict >=0.5:
        predicts.append(1)
    else:
        predicts.append(0)



scores = pd.DataFrame(plsr.x_scores_)
scores['index'] = targets

print(scores)


ax = scores.plot(x=0, y=1, kind='scatter', s=50,
                    figsize=(6,6),c='r')

groups=['WX_group','WXPB_group']

for i in range(len(groups)):
    print(groups[i])
    indicesToKeep = scores['index'].values == groups[i]

    if groups[i] == 'WX_group':
        ax_XYCH_WX = ax.scatter(scores.loc[indicesToKeep ,0],
               scores.loc[indicesToKeep, 1],
               c = 'r'
               , s = 50)
    if groups[i] == 'WXPB_group':
        ax_GYCH_WX = ax.scatter(scores.loc[indicesToKeep, 0],
                                scores.loc[indicesToKeep, 1],
                                c='b'
                                , s=50)




plt.legend(handles=[ax_XYCH_WX,ax_GYCH_WX],labels=['XYCH_WX_group','GYCH_WX_group'],loc='lower right',labelspacing=2,prop={'size': 10})
plt.title('PLS-DA for 新鲜油菜花粉和干燥油菜花粉')

plt.show()
# quit()
# print(ax)
# plt.show()
# quit()
# print(scores)
#
# y_pred = KMeans(n_clusters=2,random_state=8).fit_predict(plsr.x_scores_)
#
# print(y_pred)
# quit()
# group0 =[]
# outlier_index = []
# for i in range(len(y_pred)):
#     if y_pred[i] == 2:
#         group0.append(plsr.x_scores_[i])
#         outlier_index.append(i)
#
# group0 = np.array(group0)
#
# points_XYCH_WX = []
# points_GYCH_WX = []
# for i in range(len(scores)):
#     if i not in outlier_index:
#         if 'XYCH_WX' in scores.index[i]:
#             points_XYCH_WX.append([scores[0][i],scores[1][i]])
#         else:
#             points_GYCH_WX.append([scores[0][i],scores[1][i]])



# points_XYCH_WX = np.array(points_XYCH_WX)
# ellipse_points_XYCH_WX = EllipseModel()
# ellipse_points_XYCH_WX.estimate(points_XYCH_WX)
# XYCH_WX_x_mean,XYCH_WX_y_mean,XYCH_WX_a,XYCH_WX_b,XYCH_WX_theta = ellipse_points_XYCH_WX.params
#
# points_GYCH_WX = np.array(points_GYCH_WX)
# ellipse_points_GYCH_WX = EllipseModel()
# ellipse_points_GYCH_WX.estimate(points_GYCH_WX)
# GYCH_WX_x_mean,GYCH_WX_y_mean,GYCH_WX_a,GYCH_WX_b,GYCH_WX_theta = ellipse_points_GYCH_WX.params
#
# ellipse_XYCH_WX = Ellipse((XYCH_WX_x_mean, XYCH_WX_y_mean), 2*XYCH_WX_a, 2*XYCH_WX_b,XYCH_WX_theta,
#                         edgecolor='r', fc='None', lw=2)
# ax.add_patch(ellipse_XYCH_WX)
# ellipse_GYCH_WX = Ellipse((GYCH_WX_x_mean, GYCH_WX_y_mean), 2*GYCH_WX_a, 2*GYCH_WX_b,GYCH_WX_theta,
#                         edgecolor='b', fc='None', lw=2)
# ax.add_patch(ellipse_GYCH_WX)

# print(targets)
#
# ax.set_xlabel('PLS-DA axis 1')
# ax.set_ylabel('PLS-DA axis 2')
# ax.legend(handles=[ellipse_XYCH_WX,ellipse_GYCH_WX],labels=['XYCH_WX_group','GYCH_WX_group'])
# plt.title('PLS-DA')
# plt.show()