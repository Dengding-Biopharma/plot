import math
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn.preprocessing
from matplotlib.patches import Ellipse
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans
from skimage.measure import EllipseModel
from sklearn.preprocessing import StandardScaler
def pc1(data):
    data = pd.read_excel(data)
    # data = pd.read_excel('files/ad files/peaktableNEGout_NEG_noid_replace.xlsx')
    color_exist = []
    targets = data.columns.values[1:]


    print(data)
    print(targets)


    saved_label = data['dataMatrix'].values
    print(saved_label)
    del data['dataMatrix']
    data_impute = data.values
    scaler = StandardScaler()
    data_impute = scaler.fit_transform(data_impute)
    normalized_data_impute = data_impute
    print(normalized_data_impute)

    ad_index=[]
    hc_index=[]
    for i in range(len(targets)):
        if "AD" in targets[i]:
            ad_index.append(i)
        else:
            hc_index.append(i)
    print(ad_index)
    print(hc_index)

    normalized_data_impute_ad = []
    for index in ad_index:
        normalized_data_impute_ad.append(normalized_data_impute[:,index].T)
    normalized_data_impute_ad = np.array(normalized_data_impute_ad)

    normalized_data_impute_hc =[]
    for index in hc_index:
        normalized_data_impute_hc.append(normalized_data_impute[:,index].T)
    normalized_data_impute_hc = np.array(normalized_data_impute_hc)


    print(normalized_data_impute_ad.shape)
    print(normalized_data_impute_hc.shape)




    # PCA
    pca = PCA(n_components=2)
    pca.fit(normalized_data_impute.T)
    X_new = pca.fit_transform(normalized_data_impute.T)
    print(X_new)
    print(pca.explained_variance_ratio_)

    targets = pd.DataFrame(data = targets)
    print(targets[0].values)

    df = pd.DataFrame()
    df['targets'] = targets[0].values
    df['PC1'] = X_new[:,:1]
    df = df.sort_values(by='PC1')
    print(df)

    fig = plt.figure()
    plt.scatter(df['targets'],df['PC1'],s=20,c='black')

    X_mean = np.mean(X_new[:,:1])
    X_mean_list = []
    for i in range(len(targets[0].values)):
        X_mean_list.append(X_mean)
    plt.plot(X_mean_list,linestyle = 'solid')
    plt.text(2,X_mean,'Mean',fontsize=8)

    X_std = np.std(X_new[:,:1])
    X_mean_list = []
    for i in range(len(targets[0].values)):
        X_mean_list.append(X_mean+X_std)
    plt.plot(X_mean_list,linestyle = 'dashed')
    plt.text(2,X_mean+X_std,'Mean+1*std',fontsize=8)

    X_mean_list = []
    for i in range(len(targets[0].values)):
        X_mean_list.append(X_mean+2*X_std)
    plt.plot(X_mean_list,linestyle = 'dashed')
    plt.text(2,X_mean+2*X_std,'Mean+2*std',fontsize=8)

    X_mean_list = []
    for i in range(len(targets[0].values)):
        X_mean_list.append(X_mean-X_std)
    plt.plot(X_mean_list,linestyle = 'dashed')
    plt.text(2,X_mean-X_std,'Mean-1*std',fontsize=8)


    plt.xlabel('samples')
    plt.title('PC1 for every sample')
    plt.xticks(rotation = 90)
    plt.show()


#
# principalDf = pd.DataFrame(data = X_new
#              , columns = ['principal component 1', 'principal component 2'])
# finalDf = pd.concat([principalDf, targets], axis = 1)
# print(finalDf)
#
# targets = list(targets[0])
#
# colors = color_exist
# fig = plt.figure(figsize = (20,20))
# ax = fig.add_subplot(1,1,1)
# ax.set_xlabel('Principal Component 1 {}%'.format(round(pca.explained_variance_ratio_[0]*100,2)), fontsize = 15)
# ax.set_ylabel('Principal Component 2 {}%'.format(round(pca.explained_variance_ratio_[1]*100,2)), fontsize = 15)
# ax.set_title('2 component PCA', fontsize = 20)
#
#
#
# for target, color in zip(targets,colors):
#     indicesToKeep = finalDf[0].values == target
#     ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
#                , finalDf.loc[indicesToKeep, 'principal component 2']
#                , c = color
#                , s = 50)
#
# # ax.legend('AD_Disease_group','HC_Control_group')
# ax.grid()
#
#
# plt.show()