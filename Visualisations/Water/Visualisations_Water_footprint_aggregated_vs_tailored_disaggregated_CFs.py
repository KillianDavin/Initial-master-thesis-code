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

disag_BF_D_cba_avg_approach = pd.read_csv(
    'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Biodiversity Footprint/EXIO3/Average approach/BF_D_cba_2010_LCIA_disaggregted_All_Y_categories_average_approach.csv', index_col= [0], header= [0, 1], dtype = object)
disag_BF_D_cba_avg_approach = disag_BF_D_cba_avg_approach.astype(float)
disag_BF_D_cba_med_approach = pd.read_csv(
    'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Biodiversity Footprint/EXIO3/Median approach/BF_D_cba_2010_LCIA_disaggregted_All_Y_categories_median_approach.csv', index_col= [0], header= [0, 1], dtype= object)
disag_BF_D_cba_med_approach = disag_BF_D_cba_med_approach.astype(float)
disag_BF_D_cba_con_approach = pd.read_csv(
    'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Biodiversity Footprint/EXIO3/Continental_proxy/BF_D_cba_2010_LCIA_disaggregted_All_Y_categories_continental_proxy_approach.csv', index_col= [0], header= [0, 1], dtype= object)
disag_BF_D_cba_con_approach = disag_BF_D_cba_con_approach.astype(float)

### Cleaning and prepping tables for visualisation ###
Water_disag_BF_D_cba_avg_approach = disag_BF_D_cba_avg_approach.iloc[13:116]
Water_disag_BF_D_cba_med_approach = disag_BF_D_cba_avg_approach.iloc[13:116]
Water_disag_BF_D_cba_con_approach = disag_BF_D_cba_con_approach.iloc[13:116]

### Aggregating consumption categories ###
Water_disag_BF_D_cba_avg_approach = Water_disag_BF_D_cba_avg_approach.groupby(axis=1,level =0, sort= False).sum()
Water_disag_BF_D_cba_med_approach = Water_disag_BF_D_cba_med_approach.groupby(axis=1,level =0, sort= False).sum()
Water_disag_BF_D_cba_con_approach = Water_disag_BF_D_cba_con_approach.groupby(axis=1,level =0, sort= False).sum()

### Aggregating Water consumption stressor categories for overall view ###

Water_disag_BF_D_cba_avg_approach.loc['Total water impacts',:] = Water_disag_BF_D_cba_avg_approach.sum(0)
Water_disag_BF_D_cba_med_approach.loc['Total water impacts',:] = Water_disag_BF_D_cba_med_approach.sum(0)
Water_disag_BF_D_cba_con_approach.loc['Total water impacts',:] = Water_disag_BF_D_cba_con_approach.sum(0)

### Transposing for visualisations ###

Water_disag_BF_D_cba_avg_approach = Water_disag_BF_D_cba_avg_approach.T
Water_disag_BF_D_cba_med_approach = Water_disag_BF_D_cba_med_approach.T
Water_disag_BF_D_cba_con_approach = Water_disag_BF_D_cba_con_approach.T
Water_disag_BF_D_cba_con_approach['Countries'] = Water_disag_BF_D_cba_con_approach.index.values
Water_disag_BF_D_cba_med_approach['Countries'] = Water_disag_BF_D_cba_med_approach.index.values
Water_disag_BF_D_cba_avg_approach['Countries'] = Water_disag_BF_D_cba_avg_approach.index.values
### Now read in aggregated MRIO results using pre ordained Exiobase & LC-IMPACT Water categories ###

Agg_BF_D_cba_avg_approach = pd.read_csv(
    'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Autumn Project 2021/Biodiversity Footprint/BF_D_cba_2010_LCIA_All_Y_categories_average_approach.csv', index_col= [0], header= [0, 1], dtype = object)
Agg_BF_D_cba_avg_approach = Agg_BF_D_cba_avg_approach.astype(float)
Agg_BF_D_cba_med_approach = pd.read_csv(
    'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Autumn Project 2021/Biodiversity Footprint/BF_D_cba_2010_LCIA_All_Y_categories_median_approach.csv', index_col= [0], header= [0, 1], dtype= object)
Agg_BF_D_cba_med_approach = Agg_BF_D_cba_med_approach.astype(float)
Agg_BF_D_cba_con_approach = pd.read_csv(
    'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Autumn Project 2021/Biodiversity Footprint/BF_D_cba_2010_LCIA_All_Y_categories_continental_proxy_approach.csv', index_col= [0], header= [0, 1], dtype= object)
Agg_BF_D_cba_con_approach = Agg_BF_D_cba_con_approach.astype(float)

### Isolating Water Impacts ###

Water_Agg_BF_D_cba_avg_approach = Agg_BF_D_cba_avg_approach.iloc[13:116,:]
Water_Agg_BF_D_cba_med_approach = Agg_BF_D_cba_med_approach.iloc[13:116,:]
Water_Agg_BF_D_cba_con_approach = Agg_BF_D_cba_con_approach.iloc[13:116,:]

### Aggregating consumption categories ###

Water_Agg_BF_D_cba_avg_approach = Water_Agg_BF_D_cba_avg_approach.groupby(axis=1,level =0, sort= False).sum()
Water_Agg_BF_D_cba_med_approach = Water_Agg_BF_D_cba_med_approach.groupby(axis=1,level =0, sort= False).sum()
Water_Agg_BF_D_cba_con_approach = Water_Agg_BF_D_cba_con_approach.groupby(axis=1,level =0, sort= False).sum()

Water_Agg_BF_D_cba_avg_approach.loc['Total water impacts',:] = Water_Agg_BF_D_cba_avg_approach.sum(0).values
Water_Agg_BF_D_cba_med_approach.loc['Total water impacts',:] = Water_Agg_BF_D_cba_med_approach.sum(0).values
Water_Agg_BF_D_cba_con_approach.loc['Total water impacts',:] = Water_Agg_BF_D_cba_con_approach.sum(0).values
Water_Agg_BF_D_cba_avg_approach = Water_Agg_BF_D_cba_avg_approach.T
Water_Agg_BF_D_cba_med_approach = Water_Agg_BF_D_cba_med_approach.T
Water_Agg_BF_D_cba_con_approach = Water_Agg_BF_D_cba_con_approach.T

### Visualisation 1 ###

x = np.arange(0, len(Water_disag_BF_D_cba_avg_approach.index),1)

fig0, (ax0) =plt.subplots(figsize = (15, 6))
bottom0 = 0
bottom1 = 0
bottom2 = 0
width = 0.4


ax0.bar(x,Water_disag_BF_D_cba_con_approach['Total water impacts'], width = 0.4)
ax0.bar(x + width,Water_Agg_BF_D_cba_con_approach['Total water impacts'], width = 0.4)
ax0.spines['right'].set_visible(False)
ax0.spines['top'].set_visible(False)
# x y details #
#ax0.set(ylim = [0,.13]  )
ax0.set_ylabel('PDF.yr of species', fontsize = 8)
ax0.set_xticks(x)
ax0.set_xticklabels(Water_disag_BF_D_cba_con_approach['Countries'], rotation = 90, fontsize = 8)
ax0.set_xlim(-0.8, len(Water_disag_BF_D_cba_con_approach.index))
#ax1.set_yticklabels(fontsize=8)
# grid lines
ax0.set_axisbelow(True)
ax0.yaxis.grid(color='gray', linestyle='dashed', alpha=0.2)

plt.legend(['Water Impacts - Disaggregated', 'Water Impacts - Aggregated' ],loc='upper left', ncol = 1, fontsize = 'medium', title = 'Water category', title_fontsize = 'medium')
plt.tight_layout()
plt.show()

## Visual 2 - EU-27 aggregated vs Disaggregated (continental approach) ###

fig1, (ax1) =plt.subplots(figsize = (15, 6))
bottom0 = 0
bottom1 = 0
bottom2 = 0
width = 0.4
Water_disag_BF_D_cba_con_approach = Water_disag_BF_D_cba_con_approach.iloc[0:27,:]
Water_Agg_BF_D_cba_con_approach = Water_Agg_BF_D_cba_con_approach.iloc[0:27,:]
Water_disag_BF_D_cba_con_approach = Water_disag_BF_D_cba_con_approach.sort_values(['Total water impacts'], ascending = False)
Water_Agg_BF_D_cba_con_approach = Water_Agg_BF_D_cba_con_approach.reindex(Water_disag_BF_D_cba_con_approach.index)
x = np.arange(0, len(Water_Agg_BF_D_cba_con_approach.index),1)


ax1.bar(x,Water_disag_BF_D_cba_con_approach['Total water impacts'], width = 0.4)
ax1.bar(x + width,Water_Agg_BF_D_cba_con_approach['Total water impacts'], width = 0.4)



ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
# x y details #
#ax0.set(ylim = [0,.13]  )
ax1.set_ylabel('PDF.yr of species', fontsize = 8)
ax1.set_xticks(x)
ax1.set_xticklabels(Water_disag_BF_D_cba_con_approach['Countries'], rotation = 90, fontsize = 8)
ax1.set_xlim(-0.8, len(Water_disag_BF_D_cba_con_approach.index))
#ax1.set_yticklabels(fontsize=8)
# grid lines
ax1.set_axisbelow(True)
ax1.yaxis.grid(color='gray', linestyle='dashed', alpha=0.2)

plt.legend(['Water Impacts - Disaggregated', 'Water Impacts - Aggregated'  ],loc='upper right', ncol = 1, fontsize = 'medium', title = 'Water category', title_fontsize = 'medium')
plt.tight_layout()
plt.show()