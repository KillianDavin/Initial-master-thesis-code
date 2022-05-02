import pandas as pd
import numpy as np
import plotly
import plotly.io as pio
import pymrio
import matplotlib.pyplot as plt
import seaborn
import matplotlib.pyplot as plt
######

''' This script is.....'''

#####

### First read in diassagregated LCIA approach with tailored CF factors ###

### All Final demand categories ###

Dissag_BF_D_cba_avg_approach = pd.read_csv(
    'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Biodiversity Footprint/EXIO3/Average approach/BF_D_cba_2010_LCIA_disaggregted_All_Y_categories_average_approach.csv', index_col= [0], header= [0, 1], dtype = object)
Dissag_BF_D_cba_avg_approach = Dissag_BF_D_cba_avg_approach.astype(float)
Dissag_BF_D_cba_med_approach = pd.read_csv(
    'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Biodiversity Footprint/EXIO3/Median approach/BF_D_cba_2010_LCIA_disaggregted_All_Y_categories_median_approach.csv', index_col= [0], header= [0, 1], dtype= object)
Dissag_BF_D_cba_med_approach = Dissag_BF_D_cba_med_approach.astype(float)
Dissag_BF_D_cba_con_approach = pd.read_csv(
    'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Biodiversity Footprint/EXIO3/Continental_proxy/BF_D_cba_2010_LCIA_disaggregted_All_Y_categories_continental_proxy_approach.csv', index_col= [0], header= [0, 1], dtype= object)
Dissag_BF_D_cba_con_approach = Dissag_BF_D_cba_con_approach.astype(float)

### Cleaning and prepping tables for visualisation ###

### Land stress tables ###
Land_Dissag_BF_D_cba_avg_approach = Dissag_BF_D_cba_avg_approach.iloc[0:13,:]
Land_Dissag_BF_D_cba_med_approach = Dissag_BF_D_cba_med_approach.iloc[0:13,:]
Land_Dissag_BF_D_cba_con_approach = Dissag_BF_D_cba_con_approach.iloc[0:13,:]

### Aggregating consumption categories ###
Land_Dissag_BF_D_cba_avg_approach = Land_Dissag_BF_D_cba_avg_approach.groupby(axis=1,level =0, sort= False).sum()
Land_Dissag_BF_D_cba_med_approach = Land_Dissag_BF_D_cba_med_approach.groupby(axis=1,level =0, sort= False).sum()
Land_Dissag_BF_D_cba_con_approach = Land_Dissag_BF_D_cba_con_approach.groupby(axis=1,level =0, sort= False).sum()

### Aggregating different crop categories to Annual, Permanent, Pasture, Urban & Forestry ###
Land_Dissag_BF_D_cba_avg_approach.loc['Annual crops',:] = Land_Dissag_BF_D_cba_avg_approach.loc['Annual crops',:].values + Land_Dissag_BF_D_cba_avg_approach.loc[['Wheat', 'Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice', 'Sugar', 'Plant-based fibers'], :].sum(0).values
Land_Dissag_BF_D_cba_med_approach.loc['Annual crops',:] = Land_Dissag_BF_D_cba_med_approach.loc['Annual crops',:].values + Land_Dissag_BF_D_cba_med_approach.loc[['Wheat', 'Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice', 'Sugar', 'Plant-based fibers'], :].sum(0).values
Land_Dissag_BF_D_cba_con_approach.loc['Annual crops',:] = Land_Dissag_BF_D_cba_con_approach.loc['Annual crops',:].values + Land_Dissag_BF_D_cba_con_approach.loc[['Wheat', 'Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice', 'Sugar', 'Plant-based fibers'], :].sum(0).values
### Total Impacts ###
Land_Dissag_BF_D_cba_avg_approach.loc['Total Impacts',:] = Land_Dissag_BF_D_cba_avg_approach.loc[['Annual crops','Vegetables, fruit, nuts', 'Pasture', 'Urban', 'Extensive forestry', 'Intensive forestry'], :].sum(0).values
Land_Dissag_BF_D_cba_med_approach.loc['Total Impacts',:] = Land_Dissag_BF_D_cba_med_approach.loc[['Annual crops','Vegetables, fruit, nuts', 'Pasture', 'Urban', 'Extensive forestry', 'Intensive forestry'], :].sum(0).values
Land_Dissag_BF_D_cba_con_approach.loc['Total Impacts',:] = Land_Dissag_BF_D_cba_con_approach.loc[['Annual crops','Vegetables, fruit, nuts', 'Pasture', 'Urban', 'Extensive forestry', 'Intensive forestry'], :].sum(0).values
### Transposing tables for pandas visualisation
Land_Dissag_BF_D_cba_avg_approach = Land_Dissag_BF_D_cba_avg_approach.T
Land_Dissag_BF_D_cba_avg_approach['Countries'] = Land_Dissag_BF_D_cba_avg_approach.index.values
Land_Dissag_BF_D_cba_med_approach = Land_Dissag_BF_D_cba_med_approach.T
Land_Dissag_BF_D_cba_med_approach['Countries'] = Land_Dissag_BF_D_cba_med_approach.index.values
Land_Dissag_BF_D_cba_con_approach = Land_Dissag_BF_D_cba_con_approach.T
Land_Dissag_BF_D_cba_con_approach['Countries'] = Land_Dissag_BF_D_cba_con_approach.index.values

### Visualisations ###
x = np.arange(0, len(Land_Dissag_BF_D_cba_avg_approach.index),1)

## Visual 1 - Bar chart comparing differenet ROW approaches for tailored LCIA approach ###

fig0, (ax0) =plt.subplots(figsize = (15, 6))
bottom0 = 0
bottom1 = 0
bottom2 = 0
width = 0.3
for land_type in ('Annual crops', 'Vegetables, fruit, nuts'):

    ax0.bar(x,Land_Dissag_BF_D_cba_avg_approach[land_type], width = 0.3, bottom = bottom0)
    ax0.bar(x + width,Land_Dissag_BF_D_cba_med_approach[land_type], width = 0.3, bottom = bottom1)
    ax0.bar(x + (2*width),Land_Dissag_BF_D_cba_con_approach[land_type], width = 0.3, bottom = bottom2 )
    bottom0 += Land_Dissag_BF_D_cba_avg_approach[land_type]
    bottom1 += Land_Dissag_BF_D_cba_med_approach[land_type]
    bottom2 += Land_Dissag_BF_D_cba_con_approach[land_type]
ax0.spines['right'].set_visible(False)
ax0.spines['top'].set_visible(False)
# x y details #
#ax0.set(ylim = [0,.13]  )
ax0.set_ylabel('PDF.yr of species', fontsize = 8)
ax0.set_xticks(x)
ax0.set_xticklabels(Land_Dissag_BF_D_cba_avg_approach['Countries'], rotation = 90, fontsize = 8)
ax0.set_xlim(-0.8, len(Land_Dissag_BF_D_cba_avg_approach.index))
#ax1.set_yticklabels(fontsize=8)
# grid lines
ax0.set_axisbelow(True)
ax0.yaxis.grid(color='gray', linestyle='dashed', alpha=0.2)

plt.legend(['Annual crops - avg', 'Annual crops - med', 'Annual crops - prox', 'Permanent crops - avg','Permanent crops - med', 'Permanent crops - prox' ],loc='upper left', ncol = 1, fontsize = 'medium', title = 'Land category', title_fontsize = 'medium')
plt.tight_layout()
plt.show()

### Visual 2 - Total Biodiversity impacts of 3 LCIA approaches for ROW ###

fig1, (ax1) =plt.subplots(figsize = (15, 6))
width = 0.3
ax1.bar(x,Land_Dissag_BF_D_cba_avg_approach['Total Impacts'], width = 0.3)
ax1.bar(x + width,Land_Dissag_BF_D_cba_med_approach['Total Impacts'], width = 0.3)
ax1.bar(x + (2*width),Land_Dissag_BF_D_cba_con_approach['Total Impacts'], width = 0.3)

ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
# x y details #
#ax0.set(ylim = [0,.13]  )
ax1.set_ylabel('PDF.yr of species', fontsize = 8)
ax1.set_xticks(x + (2*width)/2)
ax1.set_xticklabels(Land_Dissag_BF_D_cba_avg_approach['Countries'], rotation = 90, fontsize = 8)
ax1.set_xlim(-0.8, len(Land_Dissag_BF_D_cba_avg_approach.index))
#ax1.set_yticklabels(fontsize=8)
# grid lines
ax1.set_axisbelow(True)
ax1.yaxis.grid(color='gray', linestyle='dashed', alpha=0.2)

plt.legend(['Average approach', 'Median approach', 'Continental proxy'],loc='upper left', ncol = 1, fontsize = 'medium', title = 'Land category', title_fontsize = 'medium')
plt.tight_layout()
plt.show()

