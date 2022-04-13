import numpy as np
import plotly
import plotly.io as pio
import pymrio
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

Land_CFs = pd.read_csv('C:/Users/Cillian/OneDrive - NTNU/Documents/NTNU project documents/ArcGIS_shapefiles_MT2022/GIS_layers_output/Final_sheets_for_Exiobase/land_characterization_factors_with_ROW_regions_ver02.csv', header=[0], index_col=[0])

Water_CFs = pd.read_csv('C:/Users/Cillian/OneDrive - NTNU/Documents/NTNU project documents/ArcGIS_shapefiles_MT2022/GIS_layers_output/Final_sheets_for_Exiobase/Watershed_aggregated_national_and_ROW_level_characterisation_factors_ver03.csv', header=[0], index_col=[0])

### Cleaning different characterisation excel files ####


LC_impact_CF_median = pd.read_csv('C:/Users/Cillian/OneDrive - NTNU/Documents/NTNU project documents/CF sheets/Land_characterisation_thesis/Full_CF_table_median_approach.csv', header = [0], index_col= [1])

LC_impact_CF_average = pd.read_csv('C:/Users/Cillian/OneDrive - NTNU/Documents/NTNU project documents/CF sheets/Land_characterisation_thesis/Full_CF_table_average_approach.csv', header = [0], index_col= [1])
iso3_to_full_names_dict = {'AT': 'Austria', 'BE':'Belgium', 'BG':'Bulgaria','CZ':'Czech Republic', 'CY':'Cyprus', 'DE':'Germany', 'DK':'Denmark', 'EE':'Estonia',
                            'ES':'Spain','FR':'France','FI':'Finland','GR':'Greece', 'HU':'Hungary', 'HR':'Croatia', 'IE':'Ireland','IT':'Italy' ,'LT':'Lithuania', 'LV':'Latvia', 'LU': 'Luxembourg',
                           'MT':'Malta', 'NL': 'Netherlands', 'PL': 'Poland', 'PT': 'Portugal', 'SE':'Sweden', 'SK':'Slovakia', 'SI':'Slovenia','RO': 'Romania',
                           'GB': 'Great Britain', 'US':'United States', 'CN':'China', 'CA': 'Canada', 'JP': 'Japan', 'IN': 'India', 'ID': 'Indonesia',
                           'KR': 'South Korea', 'RU': 'Russia', 'NO': 'Norway', 'CH': 'Switzerland', 'TW':'Taiwan','TR':'Turkey','ZA':'South Africa', 'BR': 'Brazil',
                           'MX':'Mexico', 'AU': 'Australia', 'WA': 'RoW_Asia_and_Pacific', 'WF': 'RoW_Africa', 'WL': 'RoW_America', 'WM':'RoW_Middle_East', 'WE':'RoW_Europe'}

LC_impact_CF_median = pd.DataFrame(LC_impact_CF_median.iloc[:,2:])
LC_impact_CF_median.rename(columns = iso3_to_full_names_dict, inplace = True)
LC_impact_CF_median_land = pd.DataFrame(LC_impact_CF_median.iloc[0:2,:]) #seggregating annual and permanent crop land impacts
LC_impact_CF_median_land.rename( index = {'Annual crops': 'Annual crops (median approach)', 'Permanent crops ': 'Permanent crops (median approach)'}, inplace =True)
LC_impact_CF_average = pd.DataFrame(LC_impact_CF_average.iloc[:,2:])
LC_impact_CF_average.rename(columns = iso3_to_full_names_dict, inplace = True)
LC_impact_CF_average_land = pd.DataFrame(LC_impact_CF_average.iloc[0:2,:]) #seggregating annual and permanent crop land impacts
LC_impact_CF_average_land.rename( index = {'Annual crops': 'Annual crops (average approach)', 'Permanent crops ': 'Permanent crops (average approach)'}, inplace = True)
countries_in_analysis = list(LC_impact_CF_median_land.columns)

Land_CFs = Land_CFs[countries_in_analysis]
Land_CFs = Land_CFs.append(LC_impact_CF_median_land)
Land_CFs = Land_CFs.append(LC_impact_CF_average_land)
Land_CFs = pd.DataFrame(Land_CFs.T)
print(Land_CFs)

Country_level_effects_df_average = pd.DataFrame()
Country_level_effects_df_median = pd.DataFrame()

for crop_type in ('Paddy rice', 'Wheat', 'Cereal grains Nec', 'Sugar', 'Oil seeds', 'Plant-based fibers', 'Crops Nec'):
    Country_level_effects_df_average[crop_type] = (Land_CFs[crop_type].values - Land_CFs['Annual crops (average approach)'].values) * 100 / (Land_CFs['Annual crops (average approach)'].values)
crop_type = 'Vegetables, fruit, nuts'
Country_level_effects_df_average[crop_type] = (Land_CFs[crop_type].values - Land_CFs['Permanent crops (average approach)'].values) * 100 / (Land_CFs['Permanent crops (average approach)'].values)
Country_level_effects_df_median[crop_type] = (Land_CFs[crop_type].values - Land_CFs['Permanent crops (median approach)'].values) * 100 / (Land_CFs['Permanent crops (median approach)'].values)

for crop_type in ('Paddy rice', 'Wheat', 'Cereal grains Nec', 'Sugar', 'Oil seeds', 'Plant-based fibers', 'Crops Nec'):
    Country_level_effects_df_median[crop_type] = (Land_CFs[crop_type].values - Land_CFs['Annual crops (median approach)'].values) * 100 / (Land_CFs['Annual crops (median approach)'].values)
Country_level_effects_df_median.set_axis(Land_CFs.index.values, axis = 0, inplace= True)
Country_level_effects_df_average.set_axis(Land_CFs.index.values, axis = 0, inplace = True)
Country_level_effects_df_median.to_csv('C:/Users/Cillian/OneDrive - NTNU/Documents/NTNU project documents/Results/Characterisation Factors/Land Impacts/Characterisation_factor_land_use_difference_median_approach_ver00.csv')
Country_level_effects_df_average.to_csv('C:/Users/Cillian/OneDrive - NTNU/Documents/NTNU project documents/Results/Characterisation Factors/Land Impacts/Characterisation_factor_land_use_difference_average_approach_ver00.csv')
#####################################################################################################

Water_CFs = Water_CFs[countries_in_analysis]
Water_CFs = pd.DataFrame(Water_CFs.iloc[1:10])
Water_CFs = Water_CFs.astype(float)
Water_CFs = pd.DataFrame(Water_CFs).T

#Water_CFs.astype(float)

Water_CFs['Water consumption (median approach)'] = LC_impact_CF_median.loc['Water consumption - core '].values
Water_CFs['Water Consumption (average approach)'] = LC_impact_CF_average.loc['Water consumption - core '].values

#print(Water_CFs['Water Consumption Blue - Agriculture - wheat'])

fig = plt.figure()
#print(Water_CFs[['Water Consumption Blue - Agriculture - wheat', 'Water Consumption (average approach)']])
#print(Water_CFs.loc['Austria', 'Water Consumption Blue - Agriculture - wheat'])
ax = sns.boxplot(data = Water_CFs, orient = 'h')
ax.set_xscale('symlog')
ax.set_xlim(0, 10e-14)
plt.show()
#Water_CFs = np.log10(Water_CFs.values)

Annual_crop_CFs = Land_CFs[['Paddy rice', 'Wheat', 'Cereal grains Nec', 'Sugar', 'Oil seeds', 'Plant-based fibers', 'Crops Nec', 'Annual crops (median approach)', 'Annual crops (average approach)']]

Permanent_crops_CFs = Land_CFs[['Vegetables, fruit, nuts', 'Permanent crops (median approach)', 'Permanent crops (average approach)']]

fig, axes = plt.subplots(2, 1, sharex = True, gridspec_kw={'height_ratios': [3, 1]})
fig.suptitle('Distribution of disaggregated land related biodiversity impact characetrisation factors for agricultural crop land ', fontsize=  14)

my_pal = {"Paddy rice": "g", "Wheat": "g", "Cereal grains Nec":"g", "Sugar":"g", "Oil seeds": "g", 'Plant-based fibers': 'g', 'Crops Nec': 'g', 'Annual crops (median approach)': 'r', 'Annual crops (average approach)': 'r' }
my_pal2 = {'Vegetables, fruit, nuts': 'm', 'Permanent crops (median approach)': 'b', 'Permanent crops (average approach)': 'b'}
sns.set(font_scale = 0.8)
sns.set_context("paper")
sns.set_style("whitegrid")
ax1 = sns.boxplot(data = Annual_crop_CFs, width = 0.8, palette = my_pal, orient = "h", ax = axes[0])
ax1.grid(b=True, which='major', color='black', linewidth=0.075)
ax1.grid(b=True, which='minor', color='black', linewidth=0.075)
ax1.set_title('Annual crops', loc ='center', fontdict = {'fontsize' : 10})
#ax1.spines[['top', 'right', 'bottom']].set_visible(False)
ax2 = sns.boxplot(data = Permanent_crops_CFs, width = 0.8, palette = my_pal2, orient = "h", ax = axes[1])
ax2.grid(b=True, which='major', color='black', linewidth=0.075)
ax2.grid(b=True, which='minor', color='black', linewidth=0.075)
ax2.set_xlabel('PDF.yr of species / m2', fontsize = 10)
ax2.set_title('Permanent crops', loc ='center', fontdict = {'fontsize' : 10})
plt.tight_layout

plt.show()

#########
