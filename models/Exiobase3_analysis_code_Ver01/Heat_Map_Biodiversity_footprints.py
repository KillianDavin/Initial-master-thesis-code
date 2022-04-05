import numpy as np
import plotly
import plotly.io as pio
import pymrio
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn

import seaborn as sn
import plotly as px
Aggregated_LC_impact_approach = pd.read_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Biodiversity Footprint/EXIO3/BF_D_cba_2010_LCIA_aggregated_Y_household.csv', dtype= object, header=[0, 1], index_col= [0])
Disaggregated_LC_impact_approach = pd.read_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Biodiversity Footprint/EXIO3/BF_D_cba_2010_LCIA_new_Y_household.csv',dtype= object, header=[0, 1], index_col=[0])
Disaggregated_LC_impact_approach = Disaggregated_LC_impact_approach.astype(float)
Aggregated_LC_impact_approach = Aggregated_LC_impact_approach.astype(float)
#Land_CF_tables.set_index('Land Type', inplace = True)

print(Aggregated_LC_impact_approach)
print(Disaggregated_LC_impact_approach)

new_df = pd.DataFrame()
Annual_crops = ['Cereal grains Nec','Crops Nec', 'Oil seeds', 'Paddy rice', 'Plant-based fibers', 'Sugar', 'Wheat', 'Annual crops' ]
Permanent_crops = ['Vegetables, fruit, nuts']
for crop_type in (Annual_crops, Permanent_crops):
    y = pd.DataFrame(Disaggregated_LC_impact_approach.loc[crop_type,:]).sum(0)
    Y = pd.DataFrame(y).T
    new_df = new_df.append(pd.DataFrame(Y))
new_df.set_axis(['Annual crops', 'Permanent crops'], inplace= True)
Disaggregated_LC_impact_approach = Disaggregated_LC_impact_approach.iloc[9:,:]
print(Disaggregated_LC_impact_approach)
new_df = new_df.append(Disaggregated_LC_impact_approach)
print(new_df)
Disaggregated_LC_impact_approach = pd.DataFrame(new_df)
print(list(set(Aggregated_LC_impact_approach.index.values) - set(Disaggregated_LC_impact_approach.index.values)))
print(list(set(Disaggregated_LC_impact_approach.index.values) - set(Aggregated_LC_impact_approach.index.values)))
print(Aggregated_LC_impact_approach.shape)
print(Disaggregated_LC_impact_approach.shape)
Climate_change_df = pd.DataFrame(Aggregated_LC_impact_approach.iloc[6:25,:].sum(0)).T
Climate_change_df_2 = pd.DataFrame(Disaggregated_LC_impact_approach.iloc[109:128,:].sum(0)).T
Climate_change_df.set_axis(['Climate change'], inplace= True)
Climate_change_df_2.set_axis(['Climate change'], inplace= True)
Water_consumption_df = pd.DataFrame(Aggregated_LC_impact_approach.iloc[25:128,:].sum(0)).T
Water_consumption_df_2 = pd.DataFrame(Disaggregated_LC_impact_approach.iloc[6:109].sum(0)).T
Water_consumption_df.set_axis(['Water consumption'], inplace= True)
Water_consumption_df_2.set_axis(['Water consumption'], inplace= True)
Freshwater_eutrophication_df = pd.DataFrame(Aggregated_LC_impact_approach.iloc[128:132,:].sum(0)).T
Freshwater_eutrophication_df_2 = pd.DataFrame(Disaggregated_LC_impact_approach.iloc[128:132,:].sum(0)).T
Freshwater_eutrophication_df.set_axis(['Freshwater eutrophication'], inplace= True)
Freshwater_eutrophication_df_2.set_axis(['Freshwater eutrophication'], inplace= True)
Marine_eutrophication_df = pd.DataFrame(Aggregated_LC_impact_approach.iloc[132:134,:].sum(0)).T
Marine_eutrophication_df_2 = pd.DataFrame(Disaggregated_LC_impact_approach.iloc[132:134,:].sum(0)).T
Marine_eutrophication_df.set_axis(['Marine eutrophication'], inplace= True)
Marine_eutrophication_df_2.set_axis(['Marine eutrophication'], inplace= True)


Aggregated_LC_impact_dataframe = Aggregated_LC_impact_approach.iloc[0:6,:]
Disaggregated_LC_impact_dataframe = Disaggregated_LC_impact_approach.iloc[0:6,:]
for impact_category in (Water_consumption_df, Climate_change_df, Freshwater_eutrophication_df, Marine_eutrophication_df):
    Aggregated_LC_impact_dataframe = Aggregated_LC_impact_dataframe.append(impact_category)
for impact_category in (Water_consumption_df_2, Climate_change_df_2, Freshwater_eutrophication_df_2, Marine_eutrophication_df_2):
    Disaggregated_LC_impact_dataframe = Disaggregated_LC_impact_dataframe.append(impact_category)
print(Aggregated_LC_impact_dataframe)
print(Disaggregated_LC_impact_dataframe)
Heat_map_table = (Disaggregated_LC_impact_dataframe - Aggregated_LC_impact_dataframe)
Heat_map_table = pd.DataFrame(Heat_map_table)
Heat_map_table = Heat_map_table.groupby(level = 0, axis = 1, sort = False).sum(1)

Land_Use_df = pd.DataFrame(Aggregated_LC_impact_approach.iloc[0:6,:].sum(0)).T
Land_Use_df_2 = pd.DataFrame(Disaggregated_LC_impact_approach.iloc[0:6,:].sum(0)).T

Land_Use_df.set_axis(['Land Use (Total)'], inplace= True)
Land_Use_df_2.set_axis(['Land Use (Total)'], inplace= True)
Land_Use_analysis_df = Aggregated_LC_impact_dataframe.iloc[0:2,:]
Land_Use_analysis_df_2 = Disaggregated_LC_impact_dataframe.iloc[0:2,:]
Land_Use_analysis_df = Land_Use_analysis_df.append(Land_Use_df)
Land_Use_analysis_df = pd.DataFrame(Land_Use_analysis_df.groupby(level = 0, axis = 1, sort = False).sum(1))
Land_Use_analysis_df_2 = Land_Use_analysis_df_2.append(Land_Use_df_2)
Land_Use_analysis_df_2 = pd.DataFrame(Land_Use_analysis_df_2.groupby(level = 0, axis = 1, sort = False).sum(1))
Heat_map_table = pd.DataFrame(((Land_Use_analysis_df_2 - Land_Use_analysis_df)/(Land_Use_analysis_df) ) * 100)
print(Heat_map_table)


print(Heat_map_table.shape)
Heat_map_table.to_csv('C:/Users/Cillian/OneDrive - NTNU/Documents/NTNU project documents/Results/Characterisation Factors/Land Impacts/Biodiversity_impacts_land_use_difference_household_consumption.csv')
sn.set(font_scale = 1)
fig, ax = plt.subplots(figsize = (14,9))
sn.heatmap(Heat_map_table,cmap ='viridis',
           linewidth=0.3, cbar_kws={'label': 'PDF.yr'}, vmin = -20, vmax = 20)
title = 'Impacts of tailored CF selection '
plt.title(title, loc= 'left',fontdict= {'fontsize':14})
plt.ylabel('Impact categories', fontdict= {'fontsize':12})
plt.xlabel('Countries & ROW regions',  fontdict= {'fontsize':12})
plt.tight_layout

plt.show() 

import matplotlib.pyplot as plt
import seaborn as sns

#set seaborn plotting aesthetics
sns.set(style='white')
Heat_map_table1 = pd.DataFrame(Heat_map_table.iloc[0:2,:].T)
Heat_map_table1.plot(kind = 'bar', stacked = True)
plt.show()

Heat_map_table2 = pd.DataFrame(Heat_map_table.iloc[2,:].T)
Heat_map_table2.plot(kind = 'bar', stacked = True)
plt.show()

Water_consumption_df = pd.DataFrame(Water_consumption_df).groupby(level = 0, axis = 1, sort = False).sum(1)
Water_consumption_df_2 = pd.DataFrame(Water_consumption_df_2).groupby(level = 0, axis = 1, sort = False).sum(1)
Heat_map_table3 = pd.DataFrame(((Water_consumption_df_2 - Water_consumption_df)/ Water_consumption_df_2)*100)
print(Heat_map_table3)
Heat_map_table3.to_csv('C:/Users/Cillian/OneDrive - NTNU/Documents/NTNU project documents/Results/Characterisation Factors/Water Impacts/Biodiversity_impacts_water_stress_difference_household_consumption.csv')

Heat_map_table3 = pd.DataFrame(Heat_map_table3.T)
Heat_map_table3.plot(kind = 'bar', stacked = True)
plt.show()

Land_CFs = pd.read_csv('C:/Users/Cillian/OneDrive - NTNU/Documents/NTNU project documents/ArcGIS_shapefiles_MT2022/GIS_layers_output/Final_sheets_for_Exiobase/land_characterization_factors_with_ROW_regions_ver02.csv', header=[0], index_col=[0])
print(Land_CFs)
Water_CFs = pd.read_csv('C:/Users/Cillian/OneDrive - NTNU/Documents/NTNU project documents/ArcGIS_shapefiles_MT2022/GIS_layers_output/Final_sheets_for_Exiobase/Watershed_aggregated_national_and_ROW_level_characterisation_factors_ver01.csv', header=[0], index_col=[0])
Exiobase_countries = list(Water_consumption_df.columns.values)
Land_CFs = Land_CFs[Exiobase_countries]
print(Land_CFs)
LC_impact_CFs = pd.read_csv('C:/Users/Cillian/OneDrive - NTNU/Documents/NTNU project documents/CF sheets/Land_characterisation_thesis/Full_CF_table_median_approach.csv', header = [0], index_col= [1])

print(LC_impact_CFs)
iso3_to_full_names_dict = {'AT': 'Austria', 'BE':'Belgium', 'BG':'Bulgaria','CZ':'Czech Republic', 'CY':'Cyprus', 'DE':'Germany', 'DK':'Denmark', 'EE':'Estonia',
                            'ES':'Spain','FR':'France','FI':'Finland','GR':'Greece', 'HU':'Hungary', 'HR':'Croatia', 'IE':'Ireland','IT':'Italy' ,'LT':'Lithuania', 'LV':'Latvia', 'LU': 'Luxembourg',
                           'MT':'Malta', 'NL': 'Netherlands', 'PL': 'Poland', 'PT': 'Portugal', 'SE':'Sweden', 'SK':'Slovakia', 'SI':'Slovenia','RO': 'Romania',
                           'GB': 'Great Britain', 'US':'United States', 'CN':'China', 'CA': 'Canada', 'JP': 'Japan', 'IN': 'India', 'ID': 'Indonesia',
                           'KR': 'South Korea', 'RU': 'Russia', 'NO': 'Norway', 'CH': 'Switzerland', 'TW':'Taiwan','TR':'Turkey','ZA':'South Africa', 'BR': 'Brazil',
                           'MX':'Mexico', 'AU': 'Australia', 'WA': 'RoW_Asia_and_Pacific', 'WF': 'RoW_Africa', 'WL': 'RoW_America', 'WM':'RoW_Middle_East', 'WE':'RoW_Europe'}

LC_impact_CFs.rename(columns = iso3_to_full_names_dict, inplace = True)
LC_impact_CFs = pd.DataFrame(LC_impact_CFs.iloc[:,2:])
LC_impact_CFs = LC_impact_CFs.astype(float)
LC_impact_CFs_land = LC_impact_CFs.iloc[0:2,:]
print(LC_impact_CFs_land)

Water_CFs = Water_CFs[Exiobase_countries]

Land_CFs = Land_CFs.append(LC_impact_CFs_land )
Land_CFS = pd.DataFrame(Land_CFs.T)
print(Land_CFS)


seaborn.boxplot(data = Land_CFS)
plt.show()


Land_CFs.to_csv('C:/Users/Cillian/OneDrive - NTNU/Documents/NTNU project documents/Results/Characterisation Factors/Land Impacts/Characterisation_factor_land_use_difference_verxx.csv')

print(Land_CFs)
print(Land_CFs.iloc[8,:])
print(Land_CFs.iloc[9,:])
for row in range(0,7):
    Land_CFs.iloc[row,:] = (Land_CFs.iloc[[row],:].values - Land_CFs.iloc[[8],:].values) * 100 / (Land_CFs.iloc[[8],:].values)
Land_CFs.iloc[7,:] = (Land_CFs.iloc[[7],:].values - Land_CFs.iloc[[9],:].values) * 100 / Land_CFs.iloc[[9],:].values
print(Land_CFs)
Land_CFs = pd.DataFrame(Land_CFs.iloc[0:8])
Land_CFs.to_csv('C:/Users/Cillian/OneDrive - NTNU/Documents/NTNU project documents/Results/Characterisation Factors/Land Impacts/Characterisation_factor_land_use_difference_ver00.csv')

'''
print(list(Water_CFs.columns))
print(LC_impact_CFs.loc['Water consumption - core '])
Water_CFs.loc['watershed_CF_factor'] = LC_impact_CFs.loc['Water consumption - core '].values
print(Water_CFs)
Water_CFs.iloc[1:,:] = (Water_CFs.iloc[1:,:] - Water_CFs.iloc[0,:]) * 100 / (Water_CFs.iloc[0,:])
Water_CFs = Water_CFs.iloc[1:,:]
Water_CFs.to_csv('C:/Users/Cillian/OneDrive - NTNU/Documents/NTNU project documents/Results/Characterisation Factors/Water Impacts/Characterisation_factor_water_stress_difference_ver00.csv')

print(Water_CFs) 
'''
'''
print(column_list)
for country in column_list:
    Heat_map_table[country] = np.log10(Heat_map_table[country])
Heat_map_table = Heat_map_table.astype(float)
Heat_map_table.sort_index(axis=0, level=1, inplace=True)
print(Heat_map_table)

sn.set(font_scale = 0.8)
fig1, ax2 = plt.subplots(figsize = (15,10))
sn.set(font_scale = 1.2)
htmp = sn.heatmap(Heat_map_table,cmap ='viridis',vmin= -5, vmax= -.8,
           linewidth=0.3, cbar_kws={"shrink": 1, 'label': 'PDF.yr (log10)'})
title = 'Impacts of CF factor selection for 4 ROW regions on consumption based footprints /n of all countries/regions'
htmp.figure.axes[-1].yaxis.label.set_size(12)
plt.title(title, loc= 'left',  fontdict= {'fontsize':16})
plt.ylabel('Characterisation Factor selection approach', fontdict= {'fontsize':14})
plt.xlabel('Consumption footprint per impact pathway per region (PDF of species)', fontdict= {'fontsize':14})

htmp.set_xticklabels(htmp.get_xmajorticklabels(), fontsize = 14)
htmp.set_yticklabels(htmp.get_ymajorticklabels(), fontsize = 14)
plt.tight_layout

plt.show()
'''
'''
Heat_map_table_2.sort_index(axis=0, level=1, inplace=True)
Heat_map_table_2 = Heat_map_table_2.iloc[[8,9,10,11,16,17,18,19],:]
Heat_map_table_2 = Heat_map_table_2.T
print(Heat_map_table_2)
Heat_map_table_2['Avr. CF','L.Occ'] = (Heat_map_table_2['Avr. CF','L.Occ'] - Heat_map_table_2['Med. CF','L.Occ'])*100/Heat_map_table_2['Med. CF','L.Occ']
Heat_map_table_2['High. CF','L.Occ'] = (Heat_map_table_2['High. CF','L.Occ'] - Heat_map_table_2['Med. CF','L.Occ'])*100/Heat_map_table_2['Med. CF','L.Occ']
Heat_map_table_2['Low. CF','L.Occ'] = (Heat_map_table_2['Low. CF','L.Occ'] - Heat_map_table_2['Med. CF','L.Occ'])*100/Heat_map_table_2['Med. CF','L.Occ']
Heat_map_table_2['Avr. CF','W.Con'] = (Heat_map_table_2['Avr. CF','W.Con'] - Heat_map_table_2['Med. CF','W.Con'])*100/Heat_map_table_2['Med. CF','W.Con']
Heat_map_table_2['High. CF','W.Con'] = (Heat_map_table_2['High. CF','W.Con'] - Heat_map_table_2['Med. CF','W.Con'])*100/Heat_map_table_2['Med. CF','W.Con']
Heat_map_table_2['Low. CF','W.Con'] = (Heat_map_table_2['Low. CF','W.Con'] - Heat_map_table_2['Med. CF','W.Con'])*100/Heat_map_table_2['Med. CF','W.Con']
Heat_map_table_2 = Heat_map_table_2.T
Heat_map_table_2 = Heat_map_table_2.iloc[[0,1,2,4,5,6],:]

print(Heat_map_table_2)

fig2, ax3 = plt.subplots(figsize = (12,7))

#plt.rcParams["axes.labelsize"] = 7
rdgn = sn.diverging_palette(h_neg=130, h_pos=10, s=99, l=55, sep=3, as_cmap=True)
res = sn.heatmap(Heat_map_table_2,
           linewidth=0.3, cbar_kws={"shrink": 1, 'label': '% relative change'}, cmap = rdgn, vmin = -200,center =0.00, vmax = 800)
#sn.color_palette("vlag", as_cmap=True)
res.figure.axes[-1].yaxis.label.set_size(16)
title = 'Impacts of CF factor selection for 4 ROW regions on consumption based footprints of all/ncountries/regions relative to median CF footprints'
plt.title(title, loc= 'left', fontdict= {'fontsize':16})
plt.ylabel('Characterisation Factor selection approach', fontdict= {'fontsize':14})
plt.xlabel('Country/Region', fontdict= {'fontsize':14})
sn.set(font_scale = 1.4)
res.set_xticklabels(res.get_xmajorticklabels(), fontsize = 14)
res.set_yticklabels(res.get_ymajorticklabels(), fontsize = 14)
cbar = res.collections[0].colorbar
cbar.ax.tick_params(labelsize=14)
#ax3.set_xticklabels(column_list,Fontsize = 7)
#ax3.set_yticklabels(Heat_map_table_2.index.to_list(), Fontsize = 7)
plt.tight_layout

plt.show() '''