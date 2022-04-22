from sklearn.cross_decomposition import PLSRegression
import math
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn.preprocessing
from matplotlib.patches import Ellipse
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.metrics import r2_score


data = pd.read_excel('files/peaktablePOSout_POS_noid_replace_variable.xlsx')

color_exist = []
targets = data.columns.values[1:]

for i in range(len(targets)):
    if 'AD' in targets[i]:
        targets[i] = 'AD_Disease_group'
    else:
        targets[i] = 'HC_Control_group'

for i in range(len(targets)):
    if targets[i] == 'AD_Disease_group':
        color_exist.append('r')
    else:
        color_exist.append('b')
print(data)
print(targets)

saved_label = data['dataMatrix'].values
print(saved_label)
del data['dataMatrix']
# 分别插值,根据column mean（所有sample这个variable的mean）插值
imputer_mean_ad = SimpleImputer(missing_values=np.nan,strategy='mean')
data_impute = imputer_mean_ad.fit_transform(data)
# imputer_mean_hc = SimpleImputer(missing_values=np.nan,strategy='mean')
# data_impute_hc = imputer_mean_ad.fit_transform(df_hc)
print(data_impute)
sum_baseline = 30000
for i in range(data_impute.shape[1]):
    coe = sum_baseline/np.sum(data_impute[:,i])
    data_impute[:, i] = (data_impute[:, i]*coe)/sum_baseline

normalized_data_impute = data_impute
print(normalized_data_impute)

normalized_data_impute_ad = normalized_data_impute[:,:23].T
normalized_data_impute_hc = normalized_data_impute[:,23:].T


print(normalized_data_impute_ad.shape)
print(normalized_data_impute_hc.shape)

X_ad = np.array(normalized_data_impute_ad)
X_hc = np.array(normalized_data_impute_hc)
X = np.vstack((X_ad,X_hc))
print(X)
int_targets = []
for i in targets:
    if 'AD' in i:
        int_targets.append(0)
    else:
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




colormap = {
    'AD_Disease_group': '#ff0000',  # Red
    'HC_Control_group': '#0000ff',  # Blue
}

colorlist = [colormap[c] for c in targets]
print(colorlist)

scores = pd.DataFrame(plsr.x_scores_)
scores.index = targets

ax = scores.plot(x=0, y=1, kind='scatter', s=50,
                    figsize=(6,6),c=colorlist)

ax.set_xlabel('PLS-DA axis 1')
ax.set_ylabel('PLS-DA axis 2')
ax.legend()

plt.show()