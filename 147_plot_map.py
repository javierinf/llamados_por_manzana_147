# Import libraries
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.colors import ListedColormap
import numpy as np
import pandas as pd
import geopandas as gpd
import pickle



#load data from picled files, originally csv and shp
file = open('map_df.pickle', 'rb')
map_df = pickle.load(file)
file.close()
map_df['new_geo'] = map_df['geometry']



file = open('sites_df.pickle', 'rb')
sites_df = pickle.load(file)
file.close()



#spatial join
pointInPoly = gpd.sjoin(sites_df, map_df, how = 'left' ,op='within') 


pointInPoly['SITEID'] = pd.to_numeric(pointInPoly['SITEID'])
pointInPoly = pointInPoly [['SM','SITEID', 'new_geo']]
pointInPoly['geometry'] = pointInPoly['new_geo']
pointInPoly.dropna(inplace = True)
SM = pointInPoly.groupby('SM').sum()

#join

joined = pd.merge(SM,map_df, left_index= True,right_on = 'SM',how = 'left') 
df = joined[["SITEID",'geometry']]

gfd = gpd.GeoDataFrame(df,geometry = df.geometry)

gfd = gfd[gfd['SITEID']<2000] #outliers
gfd['SITEID'] = np.log(gfd['SITEID']) #escala


variable = 'SITEID'
fig, ax = plt.subplots(1, figsize=(10, 6))
cmap = mpl.colors.LinearSegmentedColormap.from_list(
        'Custom cmap', ["darkGrey", "green", "yellow"], 20)
gfd.plot(column=variable,cmap =cmap , linewidth=0.01, ax=ax, edgecolor='0.5',legend=False)
ax.axis('off')
ax.set_title('Llamados 147', fontdict={'fontsize': '25', 'fontweight' : '3'})
ax.annotate('Source: data.buenosaires.gob.ar',xy=(0.1, .08), xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=10, color='#555555')
norm = plt.Normalize(vmin=np.exp(gfd.SITEID.min()), vmax=np.exp(gfd.SITEID.max()))
cbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
ax_cbar = fig.colorbar(cbar, ax=ax)
ax_cbar.set_label('Cant. Llamados')

plt.show()


