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
Dissag_BF_D_pba_con_approach.rename(index = {'Annual crops': 'Fodder crops'}, inplace= True)

### Cleaning and prepping tables for visualisation ###

### Land stress tables ###
Land_Dissag_BF_D_pba_con_approach = Dissag_BF_D_pba_con_approach.iloc[0:13,:]

### Aggregating consumption categories ###
Land_Dissag_BF_D_pba_con_approach = Land_Dissag_BF_D_pba_con_approach.groupby(axis=1,level =0, sort= False).sum()

### Aggregating different crop categories to Annual, Permanent, Pasture, Urban & Forestry ###

Land_Dissag_BF_D_pba_con_approach.loc['Annual crops',:] = Land_Dissag_BF_D_pba_con_approach.loc[['Fodder crops','Wheat', 'Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice', 'Sugar', 'Plant-based fibers'], :].sum(0).values

### Total Impacts ###

Land_Dissag_BF_D_pba_con_approach.loc['Total Impacts',:] = Land_Dissag_BF_D_pba_con_approach.loc[['Annual crops','Vegetables, fruit, nuts', 'Pasture'], :].sum(0).values

print(Land_Dissag_BF_D_pba_con_approach)
### Transposing tables for pandas visualisation

Land_Dissag_BF_D_pba_con_approach = Land_Dissag_BF_D_pba_con_approach.T
Land_Dissag_BF_D_pba_con_approach['Countries'] = Land_Dissag_BF_D_pba_con_approach.index.values


### Now read in aggregated MRIO results using pre ordained Exiobase & LC-IMPACT land categories ###

Agg_BF_D_pba_con_approach = pd.read_csv(
    'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Autumn Project 2021/Biodiversity Footprint/Dissagregated_BF_D_pba_2010_LCIA_Y_categories_agrifood_final_demand_continental_proxy_approach.csv', index_col= [0], header= [0, 1], dtype= object)
Agg_BF_D_pba_con_approach = Agg_BF_D_pba_con_approach.astype(float)
Agg_BF_D_pba_con_approach.rename(index = {'Permanent Crops': 'Vegetables, fruit, nuts'}, inplace= True)
print(Agg_BF_D_pba_con_approach)
### Isolating Agri-food Land Impacts ###

Land_Agg_BF_D_pba_con_approach = Agg_BF_D_pba_con_approach.iloc[0:10,:]
Land_Agg_BF_D_pba_con_approach = Land_Agg_BF_D_pba_con_approach.groupby(axis = 1, level = 0, sort = False ).sum()


### Aggregating consumption categories ###

Land_Agg_BF_D_pba_con_approach.loc['Total Impacts',:] = Land_Agg_BF_D_pba_con_approach.sum(0).values
Land_Agg_BF_D_pba_con_approach = Land_Agg_BF_D_pba_con_approach.T
print(Land_Agg_BF_D_pba_con_approach)
'''
## Visual - Aggregated vs Disaggregated (continental approach) ###

fig5, (ax5) =plt.subplots(figsize = (15, 6))
#sns.set_style("whitegrid")
bottom0 = 0
bottom1 = 0
bottom2 = 0
width = 0.4

barplot_colours = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#bcbd22','#17becf']
#Land_Dissag_BF_D_pba_con_approach = Land_Dissag_BF_D_pba_con_approach.iloc[0:27,:]
#Land_Agg_BF_D_pba_con_approach = Land_Agg_BF_D_pba_con_approach.iloc[0:27,:]
Land_Dissag_BF_D_pba_con_approach = Land_Dissag_BF_D_pba_con_approach.sort_values(['Total Impacts'], ascending = False)
Land_Agg_BF_D_pba_con_approach = Land_Agg_BF_D_pba_con_approach.reindex(Land_Dissag_BF_D_pba_con_approach.index)
x = np.arange(0, len(Land_Agg_BF_D_pba_con_approach.index),1)
n = 0
for land_type in ('Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice', 'Plant-based fibers', 'Sugar', 'Wheat', 'Vegetables, fruit, nuts'):

    #sns.barplot(x = x, y = Land_Dissag_BF_D_pba_con_approach[land_type], palette = 'tab10' )
    ax5.bar(x,Land_Dissag_BF_D_pba_con_approach[land_type], width = 0.4, bottom = bottom0, color = barplot_colours[n])
    bottom0 += Land_Dissag_BF_D_pba_con_approach[land_type]
    n += 1

ax5.bar(x + width,Land_Agg_BF_D_pba_con_approach['Annual crops'], width = 0.4, color = barplot_colours[n])


ax5.spines['right'].set_visible(False)
ax5.spines['top'].set_visible(False)
# x y details #
#ax0.set(ylim = [0,.13]  )
ax5.set_ylabel('PDF.yr of species', fontsize = 8)
ax5.set_xticks(x)
ax5.set_xticklabels(Land_Dissag_BF_D_pba_con_approach['Countries'], rotation = 90, fontsize = 8)
ax5.set_xlim(-0.8, len(Land_Dissag_BF_D_pba_con_approach.index))
#ax1.set_yticklabels(fontsize=8)
# grid lines
ax5.set_axisbelow(True)
ax5.yaxis.grid(color='gray', linestyle='dashed', alpha=0.2)

plt.legend(['Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice', 'Plant-based fibers', 'Sugar', 'Wheat','Vegetables, fruit, nuts', 'Annual crops - Aggregated'],loc='upper right', ncol = 1, fontsize = 'medium', title = 'Land category', title_fontsize = 'medium')
plt.tight_layout()
plt.show()
'''
## Visual 2 - Difference in % between aggregated and disaggregated Footprints

Footprint_disparity_df = pd.DataFrame()
Footprint_disparity_df['difference'] = pd.DataFrame((Land_Dissag_BF_D_pba_con_approach['Total Impacts'] - Land_Agg_BF_D_pba_con_approach['Total Impacts'])*100/ Land_Agg_BF_D_pba_con_approach['Total Impacts'])
Footprint_disparity_df['ADMIN'] = Footprint_disparity_df.index.values
print(Footprint_disparity_df)
Footprint_disparity_df.to_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/Visualisations/Land/Chloropeth_df.csv')
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
ax2.set_xticklabels(Footprint_disparity_df['ADMIN'], rotation = 90, fontsize = 8)
ax2.set_ylim(-80, 80)
ax2.set_xlim(-0.8, len(Land_Dissag_BF_D_pba_con_approach.index))
ax2 = sns.barplot(Footprint_disparity_df['ADMIN'],Footprint_disparity_df['difference'], palette = "Spectral" )
plt.hlines(y = 0, xmin = -0.8, xmax = len(Footprint_disparity_df.index), linestyles='-', lw=0.6, colors = 'black')
plt.show()




#######################################################################################################################################
''' 100 % stacked bar chart for relative contributions for each country for the 8 agric-food categories'''

print(Land_Dissag_BF_D_pba_con_approach.columns)

Relative_contribution_df = Land_Dissag_BF_D_pba_con_approach[['Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice',
       'Plant-based fibers', 'Sugar', 'Vegetables, fruit, nuts', 'Wheat','Fodder crops', 'Pasture', 'Total Impacts']]
#Relative_contribution_df = pd.DataFrame(Relative_contribution_df['Total Impacts'])
#Relative_contribution_df['ADMIN'] = list(Relative_contribution_df.index.values)
#print(Relative_contribution_df)
#Relative_contribution_df.to_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/Visualisations/Land/Chloropeth_df_footprint.csv')

for column in ['Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice',
       'Plant-based fibers', 'Sugar', 'Vegetables, fruit, nuts', 'Wheat','Fodder crops', 'Pasture', 'Total Impacts']:
    Relative_contribution_df[column] = Relative_contribution_df[column] / Relative_contribution_df['Total Impacts']

Relative_contribution_df = Relative_contribution_df[['Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice',
       'Plant-based fibers', 'Sugar', 'Vegetables, fruit, nuts', 'Wheat','Fodder crops', 'Pasture']]*100
Country_list = list(Relative_contribution_df.index.values)
print(Relative_contribution_df)
fig6, (ax6) =plt.subplots(figsize = (15, 6))
#sns.set_style("whitegrid")
bottom0 = 0
bottom1 = 0
bottom2 = 0
width = 0.4
x = np.arange(0, len(Relative_contribution_df.index),1)
n = 0
barplot_colours = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f','#bcbd22','#17becf']
for crop_category in [ 'Wheat','Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice',
       'Plant-based fibers', 'Sugar', 'Vegetables, fruit, nuts','Fodder crops', 'Pasture']:

    ax6.bar(x, Relative_contribution_df[crop_category], width=0.5, bottom=bottom0, color=barplot_colours[n])
    bottom0 += Relative_contribution_df[crop_category]
    n += 1
ax6.spines['right'].set_visible(False)
ax6.spines['top'].set_visible(False)
# x y details #
#ax0.set(ylim = [0,.13]  )
ax6.set_ylabel('% Relative contribution', fontsize = 10)
ax6.set_xticks(x)
ax6.set_xticklabels(Country_list, rotation = 90, fontsize = 10)
ax6.set_xlim(-0.8, len(Relative_contribution_df.index))
#ax1.set_yticklabels(fontsize=8)
# grid lines
ax6.set_axisbelow(True)
ax6.yaxis.grid(color='gray', linestyle='dashed', alpha=0.2)

plt.legend([ 'Wheat','Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice',
       'Plant-based fibers', 'Sugar', 'Vegetables, fruit, nuts','Fodder crops', 'Pasture'],loc='upper center', ncol = 5, fontsize = 'medium', title = 'Land category', title_fontsize = 'small',bbox_to_anchor=(0.5, -0.4))
plt.suptitle('Relative contribution of crop categories to agriculture and food production biodiversity impacts', fontdict= { 'family' : 'sans serif', 'size': 14} )
plt.tight_layout()
plt.show()



##################################################################################################################################################################################################################################################

### Total Impacts diasag vs aggregated results
'''
Agg_DF_Relative_contribution_df = Land_Agg_BF_D_pba_con_approach
Relative_contribution_df = Land_Dissag_BF_D_pba_con_approach[['Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice',
       'Plant-based fibers', 'Sugar', 'Vegetables, fruit, nuts', 'Wheat','Fodder crops', 'Pasture']]
Agg_DF_Relative_contribution_df = Agg_DF_Relative_contribution_df[['Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice',
       'Plant-based fibers', 'Sugar', 'Vegetables, fruit, nuts', 'Wheat','Fodder crops', 'Pasture']]
Country_list = list(Agg_DF_Relative_contribution_df.index.values)
print(Agg_DF_Relative_contribution_df)
fig7, (ax7) =plt.subplots(figsize = (15, 6))
#sns.set_style("whitegrid")
bottom0 = 0
bottom1 = 0
bottom2 = 0
width = 0.4
x = np.arange(0, len(Agg_DF_Relative_contribution_df.index),1)
n = 0
barplot_colours = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f','#bcbd22','#17becf']
for crop_category in ['Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice',
       'Plant-based fibers', 'Sugar', 'Vegetables, fruit, nuts', 'Wheat','Fodder crops', 'Pasture']:

    ax7.bar(x, Agg_DF_Relative_contribution_df[crop_category], width=0.35, bottom=bottom0, color=barplot_colours[n], label = crop_category)
    ax7.bar(x + width, Relative_contribution_df[crop_category], width = 0.35, bottom = bottom1, color = barplot_colours[n], label = crop_category)
    bottom0 += Agg_DF_Relative_contribution_df[crop_category]
    bottom1 += Relative_contribution_df[crop_category]
    n += 1
ax7.spines['right'].set_visible(False)
ax7.spines['top'].set_visible(False)
# x y details #
#ax0.set(ylim = [0,.13]  )
ax7.set_ylabel('% relative contribution', fontsize = 8)
ax7.set_xticks(x + 0.2)
ax7.set_xticklabels(Country_list, rotation = 90, fontsize = 8)
ax7.set_xlim(-0.8, len(Agg_DF_Relative_contribution_df.index))
#ax1.set_yticklabels(fontsize=8)
# grid lines
ax7.set_axisbelow(True)
ax7.yaxis.grid(color='gray', linestyle='dashed', alpha=0.2)

handles, labels = plt.gca().get_legend_handles_labels()
print(handles)
print(labels)
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(),['Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice',
       'Plant-based fibers', 'Sugar', 'Vegetables, fruit, nuts', 'Wheat','Fodder crops', 'Pasture'],loc='upper center', ncol = 5, fontsize = 'medium', title = 'Land category', title_fontsize = 'small',bbox_to_anchor=(0.5, -0.4))
plt.suptitle('Relative contribution of crop categories to agriculture and food production biodiversity impacts', fontdict= { 'family' : 'sans serif', 'size': 14} )
plt.tight_layout()
plt.show()
'''
##################################################################################################################################################################################################################################################

### % Relative contribution for countries with largest increase in footprints ###

Agg_DF_Relative_contribution_df = Land_Agg_BF_D_pba_con_approach



Agg_DF_Relative_contribution_df = Agg_DF_Relative_contribution_df[['Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice',
       'Plant-based fibers', 'Sugar', 'Vegetables, fruit, nuts', 'Wheat','Fodder crops', 'Pasture', 'Total Impacts']]

for column in ['Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice',
       'Plant-based fibers', 'Sugar', 'Vegetables, fruit, nuts', 'Wheat','Fodder crops', 'Pasture', 'Total Impacts']:

    Agg_DF_Relative_contribution_df[column] = Agg_DF_Relative_contribution_df[column] / Agg_DF_Relative_contribution_df['Total Impacts']

Agg_DF_Relative_contribution_df = Agg_DF_Relative_contribution_df[['Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice',
       'Plant-based fibers', 'Sugar', 'Vegetables, fruit, nuts', 'Wheat','Fodder crops', 'Pasture']]*100

Agg_DF_Relative_contribution_df = Agg_DF_Relative_contribution_df.loc[['Russia', 'Canada','Sweden','Norway', 'RoW_Asia_and_Pacific','Taiwan'],:]
Relative_contribution_df = Relative_contribution_df.loc[['Russia', 'Canada', 'Sweden','Norway','RoW_Asia_and_Pacific','Taiwan'],:]
Country_list = list(Agg_DF_Relative_contribution_df.index.values)
print(Agg_DF_Relative_contribution_df)
fig8, (ax8) =plt.subplots(figsize = (14, 8))
#sns.set_style("whitegrid")
bottom0 = 0
bottom1 = 0
bottom2 = 0
width = 0.4
x = np.arange(0, len(Agg_DF_Relative_contribution_df.index),1)
n = 0
barplot_colours = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f','#bcbd22','#17becf']
for crop_category in [ 'Wheat','Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice',
       'Plant-based fibers', 'Sugar', 'Vegetables, fruit, nuts','Fodder crops', 'Pasture']:

    ax8.bar(x, Agg_DF_Relative_contribution_df[crop_category], width=0.4, bottom=bottom0, color=barplot_colours[n], label = crop_category, edgecolor='black', linewidth= 0.8)
    ax8.bar(x + width, Relative_contribution_df[crop_category], width = 0.4, bottom = bottom1, color = barplot_colours[n], label = crop_category, edgecolor='black', linewidth = 0.8)
    bottom0 += Agg_DF_Relative_contribution_df[crop_category]
    bottom1 += Relative_contribution_df[crop_category]
    n += 1
ax8.spines['right'].set_visible(False)
ax8.spines['top'].set_visible(False)
# x y details #
#ax0.set(ylim = [0,.13]  )
ax8.set_ylabel('% Relative contribution', fontsize = 10)
ax8.set_xticks(x + 0.2)
ax8.set_xticklabels(Country_list, fontsize = 10)
ax8.set_xlim(-0.4, len(Agg_DF_Relative_contribution_df.index))
#ax1.set_yticklabels(fontsize=8)
# grid lines
ax8.set_axisbelow(True)
ax8.yaxis.grid(color='gray', linestyle='dashed', alpha=0.2)
ax8.annotate('Bar 1: Biodiversity footprints (Aggregated LC-Impact) ',xy=(-0.4,-10),xytext=(-0.6,-10), fontfamily = 'sans serif',               #Adds another annotation for the text that you want
            fontsize = 8, fontstyle = 'italic', fontweight = 'bold',annotation_clip=False)
ax8.annotate('Bar 2: Biodiversity footprints (Disaggregated LC-Impact)',xy=(-0.4,-20),xytext=(-0.6,-14), fontfamily = 'sans serif',               #Adds another annotation for the text that you want
            fontsize = 8, fontstyle = 'italic', fontweight = 'bold',annotation_clip=False)
handles, labels = plt.gca().get_legend_handles_labels()
print(handles)
print(labels)
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(),[ 'Wheat','Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice',
       'Plant-based fibers', 'Sugar', 'Vegetables, fruit, nuts','Fodder crops', 'Pasture'],loc='upper center', ncol = 5, fontsize = 'medium', title = 'Crop category', title_fontsize = 'medium',bbox_to_anchor=(0.5, -0.15))
plt.suptitle('Relative contribution of crop categories to agriculture and food production land biodiversity impacts', fontdict= { 'family' : 'sans serif', 'size': 14} )
plt.tight_layout()
plt.show()

###############################################################################################################################################################################################################################################################

### % Relative contribution for countries with largest increase in footprints ###

Agg_DF_Relative_contribution_df = Land_Agg_BF_D_pba_con_approach



Agg_DF_Relative_contribution_df = Agg_DF_Relative_contribution_df[['Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice',
       'Plant-based fibers', 'Sugar', 'Vegetables, fruit, nuts', 'Wheat','Fodder crops', 'Pasture', 'Total Impacts']]

for column in ['Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice',
       'Plant-based fibers', 'Sugar', 'Vegetables, fruit, nuts', 'Wheat','Fodder crops', 'Pasture', 'Total Impacts']:

    Agg_DF_Relative_contribution_df[column] = Agg_DF_Relative_contribution_df[column] / Agg_DF_Relative_contribution_df['Total Impacts']

Agg_DF_Relative_contribution_df = Agg_DF_Relative_contribution_df[['Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice',
       'Plant-based fibers', 'Sugar', 'Vegetables, fruit, nuts', 'Wheat','Fodder crops', 'Pasture']]*100

Agg_DF_Relative_contribution_df = Agg_DF_Relative_contribution_df.loc[['Romania','Austria', 'Slovakia', 'Switzerland', 'France','India'],:]
Relative_contribution_df = Land_Dissag_BF_D_pba_con_approach[['Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice',
       'Plant-based fibers', 'Sugar', 'Vegetables, fruit, nuts', 'Wheat','Fodder crops', 'Pasture', 'Total Impacts']]

for column in ['Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice',
       'Plant-based fibers', 'Sugar', 'Vegetables, fruit, nuts', 'Wheat','Fodder crops', 'Pasture', 'Total Impacts']:
    Relative_contribution_df[column] = Relative_contribution_df[column] / Relative_contribution_df['Total Impacts']

Relative_contribution_df = Relative_contribution_df[['Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice',
       'Plant-based fibers', 'Sugar', 'Vegetables, fruit, nuts', 'Wheat','Fodder crops', 'Pasture']]*100
Relative_contribution_df = Relative_contribution_df.loc[['Romania','Austria', 'Slovakia', 'Switzerland', 'France','India'],:]
Country_list = list(Agg_DF_Relative_contribution_df.index.values)
print(Agg_DF_Relative_contribution_df)
fig8, (ax8) =plt.subplots(figsize = (14, 8))
#sns.set_style("whitegrid")
bottom0 = 0
bottom1 = 0
bottom2 = 0
width = 0.4
x = np.arange(0, len(Agg_DF_Relative_contribution_df.index),1)
n = 0
barplot_colours = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f','#bcbd22','#17becf']
for crop_category in [ 'Wheat','Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice',
       'Plant-based fibers', 'Sugar', 'Vegetables, fruit, nuts','Fodder crops', 'Pasture']:

    ax8.bar(x, Agg_DF_Relative_contribution_df[crop_category], width=0.4, bottom=bottom0, color=barplot_colours[n], label = crop_category, edgecolor='black', linewidth= 0.8)
    ax8.bar(x + width, Relative_contribution_df[crop_category], width = 0.4, bottom = bottom1, color = barplot_colours[n], label = crop_category, edgecolor='black', linewidth = 0.8)
    bottom0 += Agg_DF_Relative_contribution_df[crop_category]
    bottom1 += Relative_contribution_df[crop_category]
    n += 1
ax8.spines['right'].set_visible(False)
ax8.spines['top'].set_visible(False)
# x y details #
#ax0.set(ylim = [0,.13]  )
ax8.set_ylabel('% Relative contribution', fontsize = 10)
ax8.set_xticks(x + 0.2)
ax8.set_xticklabels(Country_list, fontsize = 8)
ax8.set_xlim(-0.4, len(Agg_DF_Relative_contribution_df.index))
#ax1.set_yticklabels(fontsize=8)
# grid lines
ax8.set_axisbelow(True)
ax8.yaxis.grid(color='gray', linestyle='dashed', alpha=0.2)
ax8.annotate('Bar 1: Biodiversity footprints (Aggregated LC-Impact) ',xy=(-0.4,-10),xytext=(-0.6,-10), fontfamily = 'sans serif',               #Adds another annotation for the text that you want
            fontsize = 8, fontstyle = 'italic', fontweight = 'bold',annotation_clip=False)
ax8.annotate('Bar 2: Biodiversity footprints (Disaggregated LC-Impact)',xy=(-0.4,-20),xytext=(-0.6,-14), fontfamily = 'sans serif',               #Adds another annotation for the text that you want
            fontsize = 8, fontstyle = 'italic', fontweight = 'bold',annotation_clip=False)
handles, labels = plt.gca().get_legend_handles_labels()
print(handles)
print(labels)
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(),[ 'Wheat','Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice',
       'Plant-based fibers', 'Sugar', 'Vegetables, fruit, nuts','Fodder crops', 'Pasture'],loc='upper center', ncol = 5, fontsize = 'medium', title = 'Crop category', title_fontsize = 'medium',bbox_to_anchor=(0.5, -0.15))
plt.suptitle('Relative contribution of crop categories to agriculture and food production land biodiversity impacts', fontdict= { 'family' : 'sans serif', 'size': 14} )
plt.tight_layout()
plt.show()