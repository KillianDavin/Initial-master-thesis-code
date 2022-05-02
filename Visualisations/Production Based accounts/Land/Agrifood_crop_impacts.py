import pandas as pd
import numpy as np
import plotly
import plotly.io as pio
import pymrio
import matplotlib.pyplot as plt
import seaborn
import matplotlib.pyplot as plt
import seaborn as sns
######

''' This script is.....'''

#####

### First read in diassagregated LCIA approach with tailored CF factors ###

### Agrifood Final demand categories ###


Dissag_BF_D_pba_con_approach = pd.read_csv(
    'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Biodiversity Footprint/EXIO3/Continental_proxy/BF_D_pba_2010_LCIA_disaggregated_Y_categories_agrifood_final_demand_continental_proxy_approach.csv', index_col= [0], header= [0, 1], dtype= object)
Dissag_BF_D_pba_con_approach = Dissag_BF_D_pba_con_approach.astype(float)
Dissag_BF_D_pba_con_approach.rename(index = {'Vegetables, fruit, nuts': 'Permanent Crops'}, inplace= True)

### Cleaning and prepping tables for visualisation ###

### Land stress tables ###
Land_Dissag_BF_D_pba_con_approach = Dissag_BF_D_pba_con_approach.iloc[0:13,:]

### Aggregating consumption categories ###
Land_Dissag_BF_D_pba_con_approach = Land_Dissag_BF_D_pba_con_approach.groupby(axis=1,level =0, sort= False).sum()

### Aggregating different crop categories to Annual, Permanent, Pasture, Urban & Forestry ###

Land_Dissag_BF_D_pba_con_approach.loc['Annual crops',:] = Land_Dissag_BF_D_pba_con_approach.loc['Annual crops',:].values + Land_Dissag_BF_D_pba_con_approach.loc[['Wheat', 'Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice', 'Sugar', 'Plant-based fibers'], :].sum(0).values

### Total Impacts ###

Land_Dissag_BF_D_pba_con_approach.loc['Total Impacts',:] = Land_Dissag_BF_D_pba_con_approach.loc[['Annual crops','Permanent Crops', 'Pasture', 'Urban', 'Extensive forestry', 'Intensive forestry'], :].sum(0).values

print(Land_Dissag_BF_D_pba_con_approach)
### Transposing tables for pandas visualisation

Land_Dissag_BF_D_pba_con_approach = Land_Dissag_BF_D_pba_con_approach.T
Land_Dissag_BF_D_pba_con_approach['Countries'] = Land_Dissag_BF_D_pba_con_approach.index.values


### Now read in aggregated MRIO results using pre ordained Exiobase & LC-IMPACT land categories ###

Agg_BF_D_pba_con_approach = pd.read_csv(
    'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Autumn Project 2021/Biodiversity Footprint/BF_D_pba_2010_LCIA_Y_categories_agrifood_final_demand_continental_proxy_approach.csv', index_col= [0], header= [0, 1], dtype= object)
Agg_BF_D_pba_con_approach = Agg_BF_D_pba_con_approach.astype(float)

### Isolating Land Impacts ###

Land_Agg_BF_D_pba_con_approach = Agg_BF_D_pba_con_approach.iloc[0:13,:]

### Aggregating consumption categories ###

Land_Agg_BF_D_pba_con_approach = Land_Agg_BF_D_pba_con_approach.groupby(axis=1,level =0, sort= False).sum()

Land_Agg_BF_D_pba_con_approach.loc['Total Impacts',:] = Land_Agg_BF_D_pba_con_approach.sum(0).values
Land_Agg_BF_D_pba_con_approach = Land_Agg_BF_D_pba_con_approach.T

# Visualisation 1: ROW - Continental approach (Aggregate vs Tailored CF factors)

### Visualisations ###
x = np.arange(0, len(Land_Dissag_BF_D_pba_con_approach.index),1)

## Visual 1 - Bar chart comparing differenet ROW approaches for tailored LCIA approach ###

fig0, (ax0) =plt.subplots(figsize = (15, 6))
bottom0 = 0
bottom1 = 0
bottom2 = 0
width = 0.4
for land_type in ('Annual crops', 'Permanent Crops'):

    ax0.bar(x,Land_Dissag_BF_D_pba_con_approach[land_type], width = 0.4, bottom = bottom0)
    ax0.bar(x + width,Land_Agg_BF_D_pba_con_approach[land_type], width = 0.4, bottom = bottom1)

    bottom0 += Land_Dissag_BF_D_pba_con_approach[land_type]
    bottom1 += Land_Agg_BF_D_pba_con_approach[land_type]

ax0.spines['right'].set_visible(False)
ax0.spines['top'].set_visible(False)
# x y details #
#ax0.set(ylim = [0,.13]  )
ax0.set_ylabel('PDF.yr of species', fontsize = 8)
ax0.set_xticks(x)
ax0.set_xticklabels(Land_Dissag_BF_D_pba_con_approach['Countries'], rotation = 90, fontsize = 8)
ax0.set_xlim(-0.8, len(Land_Dissag_BF_D_pba_con_approach.index))
#ax1.set_yticklabels(fontsize=8)
# grid lines
ax0.set_axisbelow(True)
ax0.yaxis.grid(color='gray', linestyle='dashed', alpha=0.2)

plt.legend(['Annual crops - dissag ', 'Annual crops - agg', 'Permanent crops - dissag','Permanent crops - agg' ],loc='upper left', ncol = 1, fontsize = 'medium', title = 'Land category', title_fontsize = 'medium')
plt.tight_layout()
plt.show()

Footprint_disparity_df = pd.DataFrame()

## Visual 2 - Crop specific plots

import pandas as pd
import numpy as np
import plotly
import plotly.io as pio
import pymrio
import matplotlib.pyplot as plt
import seaborn
import matplotlib.pyplot as plt
import seaborn as sns
######

''' This script is.....'''

#####

### First read in diassagregated LCIA approach with tailored CF factors ###

### Agrifood Final demand categories ###

Dissag_BF_D_cba_avg_approach = pd.read_csv(
    'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Biodiversity Footprint/EXIO3/Average approach/BF_D_cba_2010_LCIA_disaggregted_All_Y_categories_agrifood_final_demand_average_approach.csv', index_col= [0], header= [0, 1], dtype = object)
Dissag_BF_D_cba_avg_approach = Dissag_BF_D_cba_avg_approach.astype(float)
Dissag_BF_D_cba_avg_approach.rename(index = {'Vegetables, fruit, nuts': 'Permanent Crops'}, inplace= True)
Dissag_BF_D_cba_med_approach = pd.read_csv(
    'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Biodiversity Footprint/EXIO3/Median approach/BF_D_cba_2010_LCIA_disaggregted_All_Y_categories_agrifood_final_demand_median_approach.csv', index_col= [0], header= [0, 1], dtype= object)
Dissag_BF_D_cba_med_approach = Dissag_BF_D_cba_med_approach.astype(float)
Dissag_BF_D_cba_med_approach.rename(index = {'Vegetables, fruit, nuts': 'Permanent Crops'}, inplace= True)
Dissag_BF_D_cba_con_approach = pd.read_csv(
    'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Biodiversity Footprint/EXIO3/Continental_proxy/BF_D_cba_2010_LCIA_disaggregted_Y_categories_agrifood_final_demand_continental_proxy_approach.csv', index_col= [0], header= [0, 1], dtype= object)
Dissag_BF_D_cba_con_approach = Dissag_BF_D_cba_con_approach.astype(float)
Dissag_BF_D_cba_con_approach.rename(index = {'Vegetables, fruit, nuts': 'Permanent Crops'}, inplace= True)

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
Land_Dissag_BF_D_cba_avg_approach.loc['Total Impacts',:] = Land_Dissag_BF_D_cba_avg_approach.loc[['Annual crops','Permanent Crops', 'Pasture', 'Urban', 'Extensive forestry', 'Intensive forestry'], :].sum(0).values
Land_Dissag_BF_D_cba_med_approach.loc['Total Impacts',:] = Land_Dissag_BF_D_cba_med_approach.loc[['Annual crops','Permanent Crops', 'Pasture', 'Urban', 'Extensive forestry', 'Intensive forestry'], :].sum(0).values
Land_Dissag_BF_D_cba_con_approach.loc['Total Impacts',:] = Land_Dissag_BF_D_cba_con_approach.loc[['Annual crops','Permanent Crops', 'Pasture', 'Urban', 'Extensive forestry', 'Intensive forestry'], :].sum(0).values
### Transposing tables for pandas visualisation
Land_Dissag_BF_D_cba_avg_approach = Land_Dissag_BF_D_cba_avg_approach.T
Land_Dissag_BF_D_cba_avg_approach['Countries'] = Land_Dissag_BF_D_cba_avg_approach.index.values
Land_Dissag_BF_D_cba_med_approach = Land_Dissag_BF_D_cba_med_approach.T
Land_Dissag_BF_D_cba_med_approach['Countries'] = Land_Dissag_BF_D_cba_med_approach.index.values
Land_Dissag_BF_D_cba_con_approach = Land_Dissag_BF_D_cba_con_approach.T
Land_Dissag_BF_D_cba_con_approach['Countries'] = Land_Dissag_BF_D_cba_con_approach.index.values


### Now read in aggregated MRIO results using pre ordained Exiobase & LC-IMPACT land categories ###

Agg_BF_D_cba_avg_approach = pd.read_csv(
    'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Autumn Project 2021/Biodiversity Footprint/BF_D_cba_2010_LCIA_Y_categories_agrifood_final_demand_average_approach.csv', index_col= [0], header= [0, 1], dtype = object)
Agg_BF_D_cba_avg_approach = Agg_BF_D_cba_avg_approach.astype(float)
Agg_BF_D_cba_med_approach = pd.read_csv(
    'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Autumn Project 2021/Biodiversity Footprint/BF_D_cba_2010_LCIA_Y_categories_agrifood_final_demand_median_approach.csv', index_col= [0], header= [0, 1], dtype= object)
Agg_BF_D_cba_med_approach = Agg_BF_D_cba_med_approach.astype(float)
Agg_BF_D_cba_con_approach = pd.read_csv(
    'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Autumn Project 2021/Biodiversity Footprint/BF_D_cba_2010_LCIA_Y_categories_agrifood_final_demand_continental_proxy_approach.csv', index_col= [0], header= [0, 1], dtype= object)
Agg_BF_D_cba_con_approach = Agg_BF_D_cba_con_approach.astype(float)

### Isolating Land Impacts ###

Land_Agg_BF_D_cba_avg_approach = Agg_BF_D_cba_avg_approach.iloc[0:13,:]
Land_Agg_BF_D_cba_med_approach = Agg_BF_D_cba_med_approach.iloc[0:13,:]
Land_Agg_BF_D_cba_con_approach = Agg_BF_D_cba_con_approach.iloc[0:13,:]

### Aggregating consumption categories ###

Land_Agg_BF_D_cba_avg_approach = Land_Agg_BF_D_cba_avg_approach.groupby(axis=1,level =0, sort= False).sum()
Land_Agg_BF_D_cba_med_approach = Land_Agg_BF_D_cba_med_approach.groupby(axis=1,level =0, sort= False).sum()
Land_Agg_BF_D_cba_con_approach = Land_Agg_BF_D_cba_con_approach.groupby(axis=1,level =0, sort= False).sum()

Land_Agg_BF_D_cba_avg_approach.loc['Total Impacts',:] = Land_Agg_BF_D_cba_avg_approach.sum(0).values
Land_Agg_BF_D_cba_med_approach.loc['Total Impacts',:] = Land_Agg_BF_D_cba_med_approach.sum(0).values
Land_Agg_BF_D_cba_con_approach.loc['Total Impacts',:] = Land_Agg_BF_D_cba_con_approach.sum(0).values
Land_Agg_BF_D_cba_avg_approach = Land_Agg_BF_D_cba_avg_approach.T
Land_Agg_BF_D_cba_med_approach = Land_Agg_BF_D_cba_med_approach.T
Land_Agg_BF_D_cba_con_approach = Land_Agg_BF_D_cba_con_approach.T

# Visualisation 1: ROW - Continental approach (Aggregate vs Tailored CF factors)

### Visualisations ###
x = np.arange(0, len(Land_Dissag_BF_D_cba_avg_approach.index),1)

## Visual 1 - Bar chart comparing differenet ROW approaches for tailored LCIA approach ###

fig0, (ax0) =plt.subplots(figsize = (15, 6))
bottom0 = 0
bottom1 = 0
bottom2 = 0
width = 0.4
for land_type in ('Annual crops', 'Permanent Crops'):

    ax0.bar(x,Land_Dissag_BF_D_cba_con_approach[land_type], width = 0.4, bottom = bottom0)
    ax0.bar(x + width,Land_Agg_BF_D_cba_con_approach[land_type], width = 0.4, bottom = bottom1)

    bottom0 += Land_Dissag_BF_D_cba_con_approach[land_type]
    bottom1 += Land_Agg_BF_D_cba_con_approach[land_type]

ax0.spines['right'].set_visible(False)
ax0.spines['top'].set_visible(False)
# x y details #
#ax0.set(ylim = [0,.13]  )
ax0.set_ylabel('PDF.yr of species', fontsize = 8)
ax0.set_xticks(x)
ax0.set_xticklabels(Land_Dissag_BF_D_cba_con_approach['Countries'], rotation = 90, fontsize = 8)
ax0.set_xlim(-0.8, len(Land_Dissag_BF_D_cba_con_approach.index))
#ax1.set_yticklabels(fontsize=8)
# grid lines
ax0.set_axisbelow(True)
ax0.yaxis.grid(color='gray', linestyle='dashed', alpha=0.2)

plt.legend(['Annual crops - dissag ', 'Annual crops - agg', 'Permanent crops - dissag','Permanent crops - agg' ],loc='upper left', ncol = 1, fontsize = 'medium', title = 'Land category', title_fontsize = 'medium')
plt.tight_layout()
plt.show()

Footprint_disparity_df = pd.DataFrame()



## Visual 2 - Difference in % between aggregated and disaggregated Footprints
print(Land_Dissag_BF_D_pba_con_approach['Total Impacts'])
print(Land_Agg_BF_D_pba_con_approach['Total Impacts'])
Footprint_disparity_df['difference'] = pd.DataFrame((Land_Dissag_BF_D_pba_con_approach['Total Impacts'] - Land_Agg_BF_D_pba_con_approach['Total Impacts'])*100/ Land_Agg_BF_D_pba_con_approach['Total Impacts'])
Footprint_disparity_df['Countries'] = Footprint_disparity_df.index.values
print(Footprint_disparity_df)
fig2, (ax2) =  plt.subplots(figsize = (15, 6))
Footprint_disparity_df = Footprint_disparity_df.sort_values(['difference'], ascending = False)
print(Footprint_disparity_df)
x = np.arange(0, len(Footprint_disparity_df.index),1)
ax2.bar(x,Footprint_disparity_df['difference'].values, width = 0.8)


ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
# x y details #
#ax0.set(ylim = [0,.13]  )
ax2.set_ylabel('Difference between disaggregated & aggregated CF factor footprints [%]', fontsize = 8)
ax2.set_xticks(x)
ax2.set_xticklabels(Footprint_disparity_df['Countries'], rotation = 90, fontsize = 8)
ax2.set_ylim(-80, 80)
ax2.set_xlim(-0.8, len(Land_Dissag_BF_D_pba_con_approach.index))
ax2 = sns.barplot(Footprint_disparity_df['Countries'],Footprint_disparity_df['difference'], palette = "Spectral" )
plt.hlines(y = 0, xmin = -0.8, xmax = len(Footprint_disparity_df.index), linestyles='-', lw=0.6, colors = 'black')
plt.show()
## Visual 2 - EU-27 aggregated vs Disaggregated (continental approach) ###

fig1, (ax1) =plt.subplots(figsize = (15, 6))
bottom0 = 0
bottom1 = 0
bottom2 = 0
width = 0.4
Land_Dissag_BF_D_pba_con_approach = Land_Dissag_BF_D_pba_con_approach.iloc[0:27,:]
Land_Agg_BF_D_pba_con_approach = Land_Agg_BF_D_pba_con_approach.iloc[0:27,:]
Land_Dissag_BF_D_pba_con_approach = Land_Dissag_BF_D_pba_con_approach.sort_values(['Total Impacts'], ascending = False)
Land_Agg_BF_D_pba_con_approach = Land_Agg_BF_D_pba_con_approach.reindex(Land_Dissag_BF_D_pba_con_approach.index)
x = np.arange(0, len(Land_Agg_BF_D_pba_con_approach.index),1)
for land_type in ('Annual crops', 'Permanent Crops'):

    ax1.bar(x,Land_Dissag_BF_D_pba_con_approach[land_type], width = 0.4, bottom = bottom0)
    ax1.bar(x + width,Land_Agg_BF_D_pba_con_approach[land_type], width = 0.4, bottom = bottom1)

    bottom0 += Land_Dissag_BF_D_pba_con_approach[land_type]
    bottom1 += Land_Agg_BF_D_pba_con_approach[land_type]

ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
# x y details #
#ax0.set(ylim = [0,.13]  )
ax1.set_ylabel('PDF.yr of species', fontsize = 8)
ax1.set_xticks(x)
ax1.set_xticklabels(Land_Dissag_BF_D_pba_con_approach['Countries'], rotation = 90, fontsize = 8)
ax1.set_xlim(-0.8, len(Land_Dissag_BF_D_pba_con_approach.index))
#ax1.set_yticklabels(fontsize=8)
# grid lines
ax1.set_axisbelow(True)
ax1.yaxis.grid(color='gray', linestyle='dashed', alpha=0.2)

plt.legend(['Annual crops - dissag ', 'Annual crops - agg', 'Permanent crops - dissag','Permanent crops - agg' ],loc='upper right', ncol = 1, fontsize = 'medium', title = 'Land category', title_fontsize = 'medium')
plt.tight_layout()
plt.show()
