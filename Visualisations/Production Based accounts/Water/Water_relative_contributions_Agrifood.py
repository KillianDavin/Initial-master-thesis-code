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

### Water stress tables ###
Water_Dissag_BF_D_pba_con_approach = Dissag_BF_D_pba_con_approach.iloc[13:116,:]

### Aggregating consumption categories ###
Water_Dissag_BF_D_pba_con_approach = Water_Dissag_BF_D_pba_con_approach.groupby(axis=1,level =0, sort= False).sum()

### Total Impacts ###

Water_Dissag_BF_D_pba_con_approach.loc['Total Impacts',:] = Water_Dissag_BF_D_pba_con_approach.sum(0)

### Aggregating different crop categories to Manufacturing, Electricity ###

Water_Dissag_BF_D_pba_con_approach.loc['Water Consumption Blue - Manufacturing',:] = Water_Dissag_BF_D_pba_con_approach.iloc[25:78, :].sum(0).values
Water_Dissag_BF_D_pba_con_approach.loc['Water Consumption Blue - Electricity',:] = Water_Dissag_BF_D_pba_con_approach.iloc[78:102, :].sum(0).values
Water_Dissag_BF_D_pba_con_approach.loc['Water Consumption Blue - Livestock', :] = Water_Dissag_BF_D_pba_con_approach.iloc[13:25,:].sum(0).values

### Transposing tables for pandas visualisation
New_df = Water_Dissag_BF_D_pba_con_approach.iloc[0:13,:]
New_df = New_df.append(Water_Dissag_BF_D_pba_con_approach.loc['Water Consumption Blue - Manufacturing',:])
New_df = New_df.append(Water_Dissag_BF_D_pba_con_approach.loc['Water Consumption Blue - Electricity',:])
New_df = New_df.append(Water_Dissag_BF_D_pba_con_approach.loc['Water Consumption Blue - Livestock', :])
New_df = New_df.append(Water_Dissag_BF_D_pba_con_approach.loc['Total Impacts',:])
Water_Dissag_BF_D_pba_con_approach = New_df
Water_Dissag_BF_D_pba_con_approach = Water_Dissag_BF_D_pba_con_approach.T
Water_Dissag_BF_D_pba_con_approach['Water Consumption Blue - Agriculture - Vegetables, fruit, nuts'] = Water_Dissag_BF_D_pba_con_approach[['Water Consumption Blue - Agriculture - vegetables','Water Consumption Blue - Agriculture - fruits', 'Water Consumption Blue - Agriculture - nuts', 'Water Consumption Blue - Agriculture - pulses', 'Water Consumption Blue - Agriculture - roots and tubers']].sum(1).values

Water_Dissag_BF_D_pba_con_approach['Countries'] = Water_Dissag_BF_D_pba_con_approach.index.values
Water_Dissag_BF_D_pba_con_approach.to_csv('Water_disagg_check.csv')
print(Water_Dissag_BF_D_pba_con_approach)


### Now read in aggregated MRIO results using pre ordained Exiobase & LC-IMPACT Water categories ###

Agg_BF_D_pba_con_approach = pd.read_csv(
    'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Autumn Project 2021/Biodiversity Footprint/Dissagregated_BF_D_pba_2010_LCIA_Y_categories_agrifood_final_demand_continental_proxy_approach.csv', index_col= [0], header= [0, 1], dtype= object)
Agg_BF_D_pba_con_approach = Agg_BF_D_pba_con_approach.astype(float)

### Isolating Agri-food Water Impacts ###

Water_Agg_BF_D_pba_con_approach = Agg_BF_D_pba_con_approach.iloc[32:135,:]
Water_Agg_BF_D_pba_con_approach = Water_Agg_BF_D_pba_con_approach.groupby(axis = 1, level = 0, sort = False ).sum()

### Aggregating consumption categories ###

Water_Agg_BF_D_pba_con_approach.loc['Total Impacts',:] = Water_Agg_BF_D_pba_con_approach.sum(0).values
### Aggregating different crop categories to Manufacturing, Electricity ###

Water_Agg_BF_D_pba_con_approach.loc['Water Consumption Blue - Manufacturing',:] = Water_Agg_BF_D_pba_con_approach.iloc[25:78, :].sum(0).values
Water_Agg_BF_D_pba_con_approach.loc['Water Consumption Blue - Electricity',:] = Water_Agg_BF_D_pba_con_approach.iloc[78:102, :].sum(0).values
Water_Agg_BF_D_pba_con_approach.loc['Water Consumption Blue - Livestock', :] = Water_Agg_BF_D_pba_con_approach.iloc[13:25,:].sum(0).values

### Transposing tables for pandas visualisation
New_df = Water_Agg_BF_D_pba_con_approach.iloc[0:13,:]
New_df = New_df.append(Water_Agg_BF_D_pba_con_approach.loc['Water Consumption Blue - Manufacturing',:])
New_df = New_df.append(Water_Agg_BF_D_pba_con_approach.loc['Water Consumption Blue - Electricity',:])
New_df = New_df.append(Water_Agg_BF_D_pba_con_approach.loc['Water Consumption Blue - Livestock', :])
New_df = New_df.append(Water_Agg_BF_D_pba_con_approach.loc['Total Impacts',:])
Water_Agg_BF_D_pba_con_approach = New_df
Water_Agg_BF_D_pba_con_approach = Water_Agg_BF_D_pba_con_approach.T
Water_Agg_BF_D_pba_con_approach['Water Consumption Blue - Agriculture - Vegetables, fruit, nuts'] = Water_Agg_BF_D_pba_con_approach[['Water Consumption Blue - Agriculture - vegetables','Water Consumption Blue - Agriculture - fruits', 'Water Consumption Blue - Agriculture - nuts', 'Water Consumption Blue - Agriculture - pulses', 'Water Consumption Blue - Agriculture - roots and tubers']].sum(1).values

Water_Agg_BF_D_pba_con_approach['Countries'] = Water_Agg_BF_D_pba_con_approach.index.values

print(Water_Agg_BF_D_pba_con_approach)
Water_Agg_BF_D_pba_con_approach.to_csv('Water_agg_check.csv')
'''
## Visual - Aggregated vs Disaggregated (continental approach) ###

fig5, (ax5) =plt.subplots(figsize = (15, 6))
#sns.set_style("whitegrid")
bottom0 = 0
bottom1 = 0
bottom2 = 0
width = 0.4

barplot_colours = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#bcbd22','#17becf']
#Water_Dissag_BF_D_pba_con_approach = Water_Dissag_BF_D_pba_con_approach.iloc[0:27,:]
#Water_Agg_BF_D_pba_con_approach = Water_Agg_BF_D_pba_con_approach.iloc[0:27,:]
Water_Dissag_BF_D_pba_con_approach = Water_Dissag_BF_D_pba_con_approach.sort_values(['Total Impacts'], ascending = False)
Water_Agg_BF_D_pba_con_approach = Water_Agg_BF_D_pba_con_approach.reindex(Water_Dissag_BF_D_pba_con_approach.index)
x = np.arange(0, len(Water_Agg_BF_D_pba_con_approach.index),1)
n = 0
for Water_type in ('Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice', 'Plant-based fibers', 'Sugar', 'Wheat', 'Vegetables, fruit, nuts'):

    #sns.barplot(x = x, y = Water_Dissag_BF_D_pba_con_approach[Water_type], palette = 'tab10' )
    ax5.bar(x,Water_Dissag_BF_D_pba_con_approach[Water_type], width = 0.4, bottom = bottom0, color = barplot_colours[n])
    bottom0 += Water_Dissag_BF_D_pba_con_approach[Water_type]
    n += 1

ax5.bar(x + width,Water_Agg_BF_D_pba_con_approach['Annual crops'], width = 0.4, color = barplot_colours[n])


ax5.spines['right'].set_visible(False)
ax5.spines['top'].set_visible(False)
# x y details #
#ax0.set(ylim = [0,.13]  )
ax5.set_ylabel('PDF.yr of species', fontsize = 8)
ax5.set_xticks(x)
ax5.set_xticklabels(Water_Dissag_BF_D_pba_con_approach['Countries'], rotation = 90, fontsize = 8)
ax5.set_xlim(-0.8, len(Water_Dissag_BF_D_pba_con_approach.index))
#ax1.set_yticklabels(fontsize=8)
# grid lines
ax5.set_axisbelow(True)
ax5.yaxis.grid(color='gray', linestyle='dashed', alpha=0.2)

plt.legend(['Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice', 'Plant-based fibers', 'Sugar', 'Wheat','Vegetables, fruit, nuts', 'Annual crops - Aggregated'],loc='upper right', ncol = 1, fontsize = 'medium', title = 'Water category', title_fontsize = 'medium')
plt.tight_layout()
plt.show()
'''
## Visual 2 - Difference in % between aggregated and disaggregated Footprints

Footprint_disparity_df = pd.DataFrame()
Footprint_disparity_df['difference'] = pd.DataFrame((Water_Dissag_BF_D_pba_con_approach['Total Impacts'] - Water_Agg_BF_D_pba_con_approach['Total Impacts'])*100/ Water_Agg_BF_D_pba_con_approach['Total Impacts'])
Footprint_disparity_df['ADMIN'] = Footprint_disparity_df.index.values
print(Footprint_disparity_df)
Footprint_disparity_df.to_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/Visualisations/Water/Chloropeth_df.csv')
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
ax2.set_ylim(-200, 200)
ax2.set_xlim(-0.4, len(Water_Dissag_BF_D_pba_con_approach.index))
ax2 = sns.barplot(Footprint_disparity_df['ADMIN'],Footprint_disparity_df['difference'], palette = "Spectral" )
plt.hlines(y = 0, xmin = -0.8, xmax = len(Footprint_disparity_df.index), linestyles='-', lw=0.6, colors = 'black')
#plt.show()




#######################################################################################################################################
''' 100 % stacked bar chart for relative contributions for each country for the 9 agric-food categories + livestock +manufcturing + electricity'''

print(Water_Dissag_BF_D_pba_con_approach.columns)

Relative_contribution_df = Water_Dissag_BF_D_pba_con_approach[['Water Consumption Blue - Agriculture - other cereals', 'Water Consumption Blue - Agriculture - other crops', 'Water Consumption Blue - Agriculture - oil crops', 'Water Consumption Blue - Agriculture - rice',
       'Water Consumption Blue - Agriculture - fibres', 'Water Consumption Blue - Agriculture - sugar crops', 'Water Consumption Blue - Agriculture - Vegetables, fruit, nuts', 'Water Consumption Blue - Agriculture - wheat','Water Consumption Blue - Agriculture - fodder crops',
       'Water Consumption Blue - Livestock','Water Consumption Blue - Manufacturing','Water Consumption Blue - Electricity', 'Total Impacts']]
#Relative_contribution_df = pd.DataFrame(Relative_contribution_df['Total Impacts'])
#Relative_contribution_df['ADMIN'] = list(Relative_contribution_df.index.values)
#print(Relative_contribution_df)
#Relative_contribution_df.to_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/Visualisations/Water/Chloropeth_df_footprint.csv')

for column in ['Water Consumption Blue - Agriculture - other cereals', 'Water Consumption Blue - Agriculture - other crops', 'Water Consumption Blue - Agriculture - oil crops', 'Water Consumption Blue - Agriculture - rice',
       'Water Consumption Blue - Agriculture - fibres', 'Water Consumption Blue - Agriculture - sugar crops', 'Water Consumption Blue - Agriculture - Vegetables, fruit, nuts', 'Water Consumption Blue - Agriculture - wheat','Water Consumption Blue - Agriculture - fodder crops',
       'Water Consumption Blue - Livestock','Water Consumption Blue - Manufacturing','Water Consumption Blue - Electricity', 'Total Impacts']:
    Relative_contribution_df[column] = Relative_contribution_df[column] / Relative_contribution_df['Total Impacts']

Relative_contribution_df = Relative_contribution_df[['Water Consumption Blue - Agriculture - other cereals', 'Water Consumption Blue - Agriculture - other crops', 'Water Consumption Blue - Agriculture - oil crops', 'Water Consumption Blue - Agriculture - rice',
       'Water Consumption Blue - Agriculture - fibres', 'Water Consumption Blue - Agriculture - sugar crops', 'Water Consumption Blue - Agriculture - Vegetables, fruit, nuts', 'Water Consumption Blue - Agriculture - wheat','Water Consumption Blue - Agriculture - fodder crops',
       'Water Consumption Blue - Livestock','Water Consumption Blue - Manufacturing','Water Consumption Blue - Electricity']]*100
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
barplot_colours = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f','#bcbd22','#17becf', '#BCD2EE','#CD8500']
for crop_category in [ 'Water Consumption Blue - Agriculture - wheat','Water Consumption Blue - Agriculture - other cereals', 'Water Consumption Blue - Agriculture - other crops', 'Water Consumption Blue - Agriculture - oil crops', 'Water Consumption Blue - Agriculture - rice',
       'Water Consumption Blue - Agriculture - fibres', 'Water Consumption Blue - Agriculture - sugar crops', 'Water Consumption Blue - Agriculture - Vegetables, fruit, nuts','Water Consumption Blue - Agriculture - fodder crops',
       'Water Consumption Blue - Livestock','Water Consumption Blue - Manufacturing','Water Consumption Blue - Electricity']:

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
ax6.set_xlim(-0.4, len(Relative_contribution_df.index))
#ax1.set_yticklabels(fontsize=8)
# grid lines
ax6.set_axisbelow(True)
ax6.yaxis.grid(color='gray', linestyle='dashed', alpha=0.2)

plt.legend([ 'Wheat','Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice',
       'Plant-based fibers', 'Sugar', 'Vegetables, fruit, nuts','Fodder crops', 'Livestock', 'Manufacturing','Electricity'],loc='upper center', ncol = 5, fontsize = 'medium', title = 'Water category', title_fontsize = 'small',bbox_to_anchor=(0.5, -0.4))
plt.suptitle('Relative contribution of crop categories to agriculture and food production blue water biodiversity impacts', fontdict= { 'family' : 'sans serif', 'size': 14} )
plt.tight_layout()
#plt.show()



##################################################################################################################################################################################################################################################

### Total Impacts of various water crop categories globally
# Total aggregeated category impacts

'''

'''
##################################################################################################################################################################################################################################################

### % Relative contribution for countries with largest increase in footprints ###

Agg_DF_Relative_contribution_df = Water_Agg_BF_D_pba_con_approach



Agg_DF_Relative_contribution_df = Agg_DF_Relative_contribution_df[['Water Consumption Blue - Agriculture - other cereals', 'Water Consumption Blue - Agriculture - other crops', 'Water Consumption Blue - Agriculture - oil crops', 'Water Consumption Blue - Agriculture - rice',
       'Water Consumption Blue - Agriculture - fibres', 'Water Consumption Blue - Agriculture - sugar crops', 'Water Consumption Blue - Agriculture - Vegetables, fruit, nuts', 'Water Consumption Blue - Agriculture - wheat','Water Consumption Blue - Agriculture - fodder crops',
       'Water Consumption Blue - Livestock','Water Consumption Blue - Manufacturing','Water Consumption Blue - Electricity', 'Total Impacts']]

for column in ['Water Consumption Blue - Agriculture - other cereals', 'Water Consumption Blue - Agriculture - other crops', 'Water Consumption Blue - Agriculture - oil crops', 'Water Consumption Blue - Agriculture - rice',
       'Water Consumption Blue - Agriculture - fibres', 'Water Consumption Blue - Agriculture - sugar crops', 'Water Consumption Blue - Agriculture - Vegetables, fruit, nuts', 'Water Consumption Blue - Agriculture - wheat','Water Consumption Blue - Agriculture - fodder crops',
       'Water Consumption Blue - Livestock','Water Consumption Blue - Manufacturing','Water Consumption Blue - Electricity', 'Total Impacts']:

    Agg_DF_Relative_contribution_df[column] = Agg_DF_Relative_contribution_df[column] / Agg_DF_Relative_contribution_df['Total Impacts']

Agg_DF_Relative_contribution_df = Agg_DF_Relative_contribution_df[['Water Consumption Blue - Agriculture - other cereals', 'Water Consumption Blue - Agriculture - other crops', 'Water Consumption Blue - Agriculture - oil crops', 'Water Consumption Blue - Agriculture - rice',
       'Water Consumption Blue - Agriculture - fibres', 'Water Consumption Blue - Agriculture - sugar crops', 'Water Consumption Blue - Agriculture - Vegetables, fruit, nuts', 'Water Consumption Blue - Agriculture - wheat','Water Consumption Blue - Agriculture - fodder crops',
       'Water Consumption Blue - Livestock','Water Consumption Blue - Manufacturing','Water Consumption Blue - Electricity']]*100

Agg_DF_Relative_contribution_df = Agg_DF_Relative_contribution_df.loc[['Russia', 'United States', 'RoW_Asia_and_Pacific', 'RoW_America', 'RoW_Africa'],:]
Relative_contribution_df = Relative_contribution_df.loc[['Russia', 'United States', 'RoW_Asia_and_Pacific', 'RoW_America', 'RoW_Africa'],:]
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
barplot_colours = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f','#bcbd22','#17becf', '#BCD2EE','#CD8500']
for crop_category in [ 'Water Consumption Blue - Agriculture - wheat','Water Consumption Blue - Agriculture - other cereals', 'Water Consumption Blue - Agriculture - other crops', 'Water Consumption Blue - Agriculture - oil crops', 'Water Consumption Blue - Agriculture - rice',
       'Water Consumption Blue - Agriculture - fibres', 'Water Consumption Blue - Agriculture - sugar crops', 'Water Consumption Blue - Agriculture - Vegetables, fruit, nuts','Water Consumption Blue - Agriculture - fodder crops',
       'Water Consumption Blue - Livestock','Water Consumption Blue - Manufacturing','Water Consumption Blue - Electricity']:

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

handles, labels = plt.gca().get_legend_handles_labels()
print(handles)
print(labels)
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(),['Wheat','Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice',
       'Plant-based fibers', 'Sugar', 'Vegetables, fruit, nuts','Fodder crops', 'Livestock', 'Manufacturing','Electricity'],loc='upper center', ncol = 5, fontsize = 'medium', title = 'Water category', title_fontsize = 'small',bbox_to_anchor=(0.5, -0.15))
plt.suptitle('Relative contribution of crop categories to agriculture and food production blue water biodiversity impacts', fontdict= { 'family' : 'sans serif', 'size': 14} )
plt.tight_layout()
#plt.show()

###############################################################################################################################################################################################################################################################

### % Relative contribution for countries with largest decrease in footprints ###

Agg_DF_Relative_contribution_df = Water_Agg_BF_D_pba_con_approach
Total_Water_agg_impacts = pd.DataFrame(Water_Agg_BF_D_pba_con_approach)
print(list(Total_Water_agg_impacts.index))
Total_Water_agg_impacts = Total_Water_agg_impacts.drop('United States', axis = 0)
print(list(Total_Water_agg_impacts.index))
Total_Water_agg_impacts = pd.DataFrame(Total_Water_agg_impacts.sum(0))
Total_Water_dis_impacts = pd.DataFrame(Water_Dissag_BF_D_pba_con_approach)
Total_Water_dis_impacts = Total_Water_dis_impacts.drop('United States', axis = 0)
Total_Water_dis_impacts = pd.DataFrame(Total_Water_dis_impacts.sum(0))
Total_Water_dis_impacts = pd.DataFrame(Total_Water_dis_impacts.T)
Total_Water_agg_impacts = pd.DataFrame(Total_Water_agg_impacts.T)
Contribution_total_Water_dis_impacts = pd.DataFrame()
Contribution_total_Water_agg_impacts = pd.DataFrame()
print(Total_Water_dis_impacts.columns)
for column in ['Water Consumption Blue - Agriculture - other cereals', 'Water Consumption Blue - Agriculture - other crops', 'Water Consumption Blue - Agriculture - oil crops', 'Water Consumption Blue - Agriculture - rice',
       'Water Consumption Blue - Agriculture - fibres', 'Water Consumption Blue - Agriculture - sugar crops', 'Water Consumption Blue - Agriculture - Vegetables, fruit, nuts', 'Water Consumption Blue - Agriculture - wheat','Water Consumption Blue - Agriculture - fodder crops',
       'Water Consumption Blue - Livestock','Water Consumption Blue - Manufacturing','Water Consumption Blue - Electricity', 'Total Impacts']:

    Contribution_total_Water_dis_impacts[column] = Total_Water_dis_impacts[column] * 100 / Total_Water_dis_impacts['Total Impacts']
    Contribution_total_Water_agg_impacts[column] = Total_Water_agg_impacts[column] * 100 / Total_Water_agg_impacts['Total Impacts']
print(Total_Water_dis_impacts.columns)
Contribution_total_Water_dis_impacts = Contribution_total_Water_dis_impacts[['Water Consumption Blue - Agriculture - other cereals', 'Water Consumption Blue - Agriculture - other crops', 'Water Consumption Blue - Agriculture - oil crops', 'Water Consumption Blue - Agriculture - rice',
       'Water Consumption Blue - Agriculture - fibres', 'Water Consumption Blue - Agriculture - sugar crops', 'Water Consumption Blue - Agriculture - Vegetables, fruit, nuts', 'Water Consumption Blue - Agriculture - wheat','Water Consumption Blue - Agriculture - fodder crops',
       'Water Consumption Blue - Livestock','Water Consumption Blue - Manufacturing','Water Consumption Blue - Electricity']]

Contribution_total_Water_agg_impacts = Contribution_total_Water_agg_impacts[['Water Consumption Blue - Agriculture - other cereals', 'Water Consumption Blue - Agriculture - other crops', 'Water Consumption Blue - Agriculture - oil crops', 'Water Consumption Blue - Agriculture - rice',
       'Water Consumption Blue - Agriculture - fibres', 'Water Consumption Blue - Agriculture - sugar crops', 'Water Consumption Blue - Agriculture - Vegetables, fruit, nuts', 'Water Consumption Blue - Agriculture - wheat','Water Consumption Blue - Agriculture - fodder crops',
       'Water Consumption Blue - Livestock','Water Consumption Blue - Manufacturing','Water Consumption Blue - Electricity']]

fig,(ax10,ax11) =plt.subplots( ncols=2, figsize = (15, 6),sharey= False)
#sns.set_style("whitegrid")
bottom0 = 0
bottom1 = 0
bottom2 = 0
width = .5
x = np.arange(0,len(Contribution_total_Water_dis_impacts.index),1)
n = 0
barplot_colours = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f','#bcbd22','#17becf', '#BCD2EE','#CD8500']
for crop_category in [ 'Water Consumption Blue - Agriculture - wheat','Water Consumption Blue - Agriculture - other cereals', 'Water Consumption Blue - Agriculture - other crops', 'Water Consumption Blue - Agriculture - oil crops', 'Water Consumption Blue - Agriculture - rice',
       'Water Consumption Blue - Agriculture - fibres', 'Water Consumption Blue - Agriculture - sugar crops', 'Water Consumption Blue - Agriculture - Vegetables, fruit, nuts','Water Consumption Blue - Agriculture - fodder crops',
       'Water Consumption Blue - Livestock','Water Consumption Blue - Manufacturing','Water Consumption Blue - Electricity']:

    ax10.bar(x, Contribution_total_Water_agg_impacts[crop_category], width=0.4, bottom=bottom0, color=barplot_colours[n], label = crop_category, edgecolor='black', linewidth= 0.8)
    ax10.bar(x + width, Contribution_total_Water_dis_impacts[crop_category], width = 0.4, bottom = bottom1, color = barplot_colours[n], label = crop_category, edgecolor='black', linewidth = 0.8)
    bottom0 += Contribution_total_Water_agg_impacts[crop_category]
    bottom1 += Contribution_total_Water_dis_impacts[crop_category]
    n += 1
ax10.spines['right'].set_visible(False)
ax10.spines['top'].set_visible(False)
ax10.set_ylabel('% Relative contribution', fontsize = 10)
ax10.axes.xaxis.set_visible(False)
ax10.set_xticks(x)
#ax10.set_xticklabels(['Aggregated','Disaggregated'], fontsize = 8)
ax10.set_xlim(-0.32, len(Contribution_total_Water_dis_impacts.index))
ax10.set_axisbelow(True)
ax10.yaxis.grid(color='gray', linestyle='dashed', alpha=0.2)
ax10.annotate('Disaggregated CFs', xy=(1, 1.2),  xycoords='data',
            xytext=(0.575, 1.02), textcoords='axes fraction'
            )
ax10.annotate('Aggregated CFs', xy=(1, 1.2),  xycoords='data',
            xytext=(0.205, 1.02), textcoords='axes fraction'
            )

handles, labels = ax10.get_legend_handles_labels()
print(handles)
print(labels)
by_label = dict(zip(labels, handles))
print(by_label)
ax10.legend(by_label.values(),[ 'Wheat','Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice',
       'Plant-based fibers', 'Sugar', 'Vegetables, fruit, nuts','Fodder crops', 'Livestock', 'Manufacturing','Electricity'],loc='upper center', ncol = 4, fontsize = 'small', title = 'Crop categories', title_fontsize = 'small',bbox_to_anchor=(0.45, -0.03))
plt.suptitle('Relative contribution of crop categories to agriculture and food production biodiversity impacts', fontdict= { 'family' : 'sans serif', 'size': 14}, y = 0.995, x = 0.5)

Total_Water_dis_impacts = pd.DataFrame(Total_Water_dis_impacts.T)

Total_Water_dis_impacts['Total Impacts'] = Total_Water_dis_impacts.iloc[:,0].values
Total_Water_dis_impacts = Total_Water_dis_impacts.drop(labels= ['Countries', 'Total Impacts', 'Water Consumption Blue - Agriculture - vegetables', 'Water Consumption Blue - Agriculture - fruits',
                                                                'Water Consumption Blue - Agriculture - nuts', 'Water Consumption Blue - Agriculture - pulses', 'Water Consumption Blue - Agriculture - roots and tubers'], axis=0)
Total_Water_agg_impacts = pd.DataFrame(Total_Water_agg_impacts.T)
Total_Water_agg_impacts['Total Impacts'] = Total_Water_agg_impacts.iloc[:,0].values
Total_Water_agg_impacts = Total_Water_agg_impacts.drop(labels= ['Countries', 'Total Impacts', 'Water Consumption Blue - Agriculture - vegetables', 'Water Consumption Blue - Agriculture - fruits',

                                                               'Water Consumption Blue - Agriculture - nuts', 'Water Consumption Blue - Agriculture - pulses', 'Water Consumption Blue - Agriculture - roots and tubers'], axis=0)

width = .3
x = np.arange(0,len(Total_Water_dis_impacts.index),1)
n = 0
'''
for crop_category in [ 'Water Consumption Blue - Agriculture - wheat','Water Consumption Blue - Agriculture - other cereals', 'Water Consumption Blue - Agriculture - other crops', 'Water Consumption Blue - Agriculture - oil crops', 'Water Consumption Blue - Agriculture - rice',
       'Water Consumption Blue - Agriculture - fibres', 'Water Consumption Blue - Agriculture - sugar crops', 'Water Consumption Blue - Agriculture - Vegetables, fruit, nuts','Water Consumption Blue - Agriculture - fodder crops',
       'Water Consumption Blue - Livestock','Water Consumption Blue - Manufacturing','Water Consumption Blue - Electricity']:
'''
print(list(Total_Water_dis_impacts.columns.values))
print(Total_Water_dis_impacts)
ax11.bar(x, Total_Water_agg_impacts['Total Impacts'], width=0.3, color= 'g', label = crop_category, edgecolor='black', linewidth= 0.8)
ax11.bar(x + width, Total_Water_dis_impacts['Total Impacts'], width = 0.3, color = 'r', label = crop_category, edgecolor='black', linewidth = 0.8)



ax11.spines['right'].set_visible(False)
ax11.spines['top'].set_visible(False)
ax11.set_ylabel('PDF', fontsize = 10)
ax11.set_xticks(x)
ax11.set_xticklabels(['Wheat', 'Rice', 'Other cereals', 'Oil crops', 'Sugar', 'Plant-based fibers', 'Crops Nec', 'Fodder crops', 'Manufacturing', 'Electricity', 'Livestock',  'Veg, fruit & nuts'], fontsize = 8, rotation = 90)
ax11.set_xlim(-0.32, len(Total_Water_dis_impacts.index))
ax11.set_axisbelow(True)
ax11.legend(['Aggregated CFs', 'Disaggregated CFs'],loc='upper right', ncol = 1, fontsize = 'small', title = 'CF approach', title_fontsize = 'small')


plt.tight_layout()
plt.show()





########################################################################################################################################

Agg_DF_Relative_contribution_df = Agg_DF_Relative_contribution_df[['Water Consumption Blue - Agriculture - other cereals', 'Water Consumption Blue - Agriculture - other crops', 'Water Consumption Blue - Agriculture - oil crops', 'Water Consumption Blue - Agriculture - rice',
       'Water Consumption Blue - Agriculture - fibres', 'Water Consumption Blue - Agriculture - sugar crops', 'Water Consumption Blue - Agriculture - Vegetables, fruit, nuts', 'Water Consumption Blue - Agriculture - wheat','Water Consumption Blue - Agriculture - fodder crops',
       'Water Consumption Blue - Livestock','Water Consumption Blue - Manufacturing','Water Consumption Blue - Electricity', 'Total Impacts']]

for column in ['Water Consumption Blue - Agriculture - other cereals', 'Water Consumption Blue - Agriculture - other crops', 'Water Consumption Blue - Agriculture - oil crops', 'Water Consumption Blue - Agriculture - rice',
       'Water Consumption Blue - Agriculture - fibres', 'Water Consumption Blue - Agriculture - sugar crops', 'Water Consumption Blue - Agriculture - Vegetables, fruit, nuts', 'Water Consumption Blue - Agriculture - wheat','Water Consumption Blue - Agriculture - fodder crops',
       'Water Consumption Blue - Livestock','Water Consumption Blue - Manufacturing','Water Consumption Blue - Electricity', 'Total Impacts']:

    Agg_DF_Relative_contribution_df[column] = Agg_DF_Relative_contribution_df[column] / Agg_DF_Relative_contribution_df['Total Impacts']

Agg_DF_Relative_contribution_df = Agg_DF_Relative_contribution_df[['Water Consumption Blue - Agriculture - other cereals', 'Water Consumption Blue - Agriculture - other crops', 'Water Consumption Blue - Agriculture - oil crops', 'Water Consumption Blue - Agriculture - rice',
       'Water Consumption Blue - Agriculture - fibres', 'Water Consumption Blue - Agriculture - sugar crops', 'Water Consumption Blue - Agriculture - Vegetables, fruit, nuts', 'Water Consumption Blue - Agriculture - wheat','Water Consumption Blue - Agriculture - fodder crops',
       'Water Consumption Blue - Livestock','Water Consumption Blue - Manufacturing','Water Consumption Blue - Electricity', 'Total Impacts']]*100

Agg_DF_Relative_contribution_df = Agg_DF_Relative_contribution_df.loc[['RoW_Europe', 'Australia', 'Indonesia', 'South Africa', 'Canada', 'Brazil'],:]
Relative_contribution_df = Water_Dissag_BF_D_pba_con_approach[['Water Consumption Blue - Agriculture - other cereals', 'Water Consumption Blue - Agriculture - other crops', 'Water Consumption Blue - Agriculture - oil crops', 'Water Consumption Blue - Agriculture - rice',
       'Water Consumption Blue - Agriculture - fibres', 'Water Consumption Blue - Agriculture - sugar crops', 'Water Consumption Blue - Agriculture - Vegetables, fruit, nuts', 'Water Consumption Blue - Agriculture - wheat','Water Consumption Blue - Agriculture - fodder crops',
       'Water Consumption Blue - Livestock','Water Consumption Blue - Manufacturing','Water Consumption Blue - Electricity', 'Total Impacts']]

for column in ['Water Consumption Blue - Agriculture - other cereals', 'Water Consumption Blue - Agriculture - other crops', 'Water Consumption Blue - Agriculture - oil crops', 'Water Consumption Blue - Agriculture - rice',
       'Water Consumption Blue - Agriculture - fibres', 'Water Consumption Blue - Agriculture - sugar crops', 'Water Consumption Blue - Agriculture - Vegetables, fruit, nuts', 'Water Consumption Blue - Agriculture - wheat','Water Consumption Blue - Agriculture - fodder crops',
       'Water Consumption Blue - Livestock','Water Consumption Blue - Manufacturing','Water Consumption Blue - Electricity', 'Total Impacts']:
    Relative_contribution_df[column] = Relative_contribution_df[column] / Relative_contribution_df['Total Impacts']

Relative_contribution_df = Relative_contribution_df[['Water Consumption Blue - Agriculture - other cereals', 'Water Consumption Blue - Agriculture - other crops', 'Water Consumption Blue - Agriculture - oil crops', 'Water Consumption Blue - Agriculture - rice',
       'Water Consumption Blue - Agriculture - fibres', 'Water Consumption Blue - Agriculture - sugar crops', 'Water Consumption Blue - Agriculture - Vegetables, fruit, nuts', 'Water Consumption Blue - Agriculture - wheat','Water Consumption Blue - Agriculture - fodder crops',
       'Water Consumption Blue - Livestock','Water Consumption Blue - Manufacturing','Water Consumption Blue - Electricity']]*100
Relative_contribution_df = Relative_contribution_df.loc[['RoW_Europe', 'Australia', 'Indonesia', 'South Africa', 'Canada', 'Brazil'],:]
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
barplot_colours = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f','#bcbd22','#17becf', '#BCD2EE','#CD8500']
for crop_category in [ 'Water Consumption Blue - Agriculture - wheat','Water Consumption Blue - Agriculture - other cereals', 'Water Consumption Blue - Agriculture - other crops', 'Water Consumption Blue - Agriculture - oil crops', 'Water Consumption Blue - Agriculture - rice',
       'Water Consumption Blue - Agriculture - fibres', 'Water Consumption Blue - Agriculture - sugar crops', 'Water Consumption Blue - Agriculture - Vegetables, fruit, nuts','Water Consumption Blue - Agriculture - fodder crops',
       'Water Consumption Blue - Livestock','Water Consumption Blue - Manufacturing','Water Consumption Blue - Electricity']:

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

handles, labels = plt.gca().get_legend_handles_labels()
print(handles)
print(labels)
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(),['Wheat','Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice',
       'Plant-based fibers', 'Sugar', 'Vegetables, fruit, nuts', 'Fodder crops', 'Livestock', 'Manufacturing','Electricity'],loc='upper center', ncol = 5, fontsize = 'medium', title = 'Water category', title_fontsize = 'small',bbox_to_anchor=(0.5, -0.15))
plt.suptitle('Relative contribution of crop categories to agriculture and food production biodiversity impacts', fontdict= { 'family' : 'sans serif', 'size': 14} )
plt.tight_layout()
plt.show()