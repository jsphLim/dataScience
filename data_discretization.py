import pandas as pd

inputfile='discretization.xlsx'
data = pd.read_excel(inputfile)
data = data[u'肝气郁结证型系数'].copy()
k=4

d1 = pd.cut(data,k,labels=range(k))

w = [1.0*i/k for i in range(k+1)]
w = data.describe(percentiles = w)[4:4+k+1]
w[0] = w[0]*(1-1e-10)
d2 = pd.cut(data,w,labels=range(k))

from sklearn.cluster import KMeans

kmodel = KMeans(n_clusters=k,n_jobs=4)

kmodel.fit(data.reshape((len(data),1)))
c = pd.DataFrame(kmodel.cluster_centers_).sort(0)

w = pd.rolling_mean(c,2).iloc[1:]

w = [0] +list(w[0])+[data.max()]
d3 = pd.cut(data,w,labels=range(k))

def cluster_plot(d,k):
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] =False

    plt.figure(figsize=(8,3))
    for j in range(0,k):
        plt.plot(data[d==j],[j for i in d[d==j]],'o')

    plt.ylim(-0.5,k-0.5)
    return plt

cluster_plot(d1,k).show()
cluster_plot(d2,k).show()
cluster_plot(d3,k).show()
