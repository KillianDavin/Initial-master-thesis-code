import pandas as pd
import numpy as np
import plotly
import plotly.io as pio
import pymrio
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt
######

''' This script is.....'''

#####

### First read in diassagregated LCIA approach with tailored CF factors ###

### Agrifood demand categories ###

disag_BF_D_cba_avg_approach = pd.read_csv(
    'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Biodiversity Footprint/EXIO3/Average approach/BF_D_cba_2010_LCIA_disaggregted_All_Y_categories_agrifood_final_demand_average_approach.csv', index_col= [0], header= [0, 1], dtype = object)
disag_BF_D_cba_avg_approach = disag_BF_D_cba_avg_approach.astype(float)
disag_BF_D_cba_med_approach = pd.read_csv(
    'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Biodiversity Footprint/EXIO3/Median approach/BF_D_cba_2010_LCIA_disaggregted_All_Y_categories_agrifood_final_demand_median_approach.csv', index_col= [0], header= [0, 1], dtype= object)
disag_BF_D_cba_med_approach = disag_BF_D_cba_med_approach.astype(float)
disag_BF_D_cba_con_approach = pd.read_csv(
    'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Biodiversity Footprint/EXIO3/Continental_proxy/BF_D_cba_2010_LCIA_disaggregted_Y_categories_agrifood_final_demand_continental_proxy_approach.csv', index_col= [0], header= [0, 1], dtype= object)
disag_BF_D_cba_con_approach = disag_BF_D_cba_con_approach.astype(float)

### Cleaning and prepping tables for visualisation ###
Water_disag_BF_D_cba_avg_approach = disag_BF_D_cba_avg_approach.iloc[13:116]
Water_disag_BF_D_cba_med_approach = disag_BF_D_cba_avg_approach.iloc[13:116]
Water_disag_BF_D_cba_con_approach = disag_BF_D_cba_con_approach.iloc[13:116]

### EU economy only

EU_Water_disag_BF_D_cba_avg_approach = disag_BF_D_cba_avg_approach.iloc[13:116].groupby(axis=1,level = 0, sort= False).sum()

EU_Water_disag_BF_D_cba_avg_approach = EU_Water_disag_BF_D_cba_avg_approach.iloc[:,0:27]
EU_Water_disag_BF_D_cba_med_approach = disag_BF_D_cba_avg_approach.iloc[13:116].groupby(axis=1,level = 0, sort= False).sum()
EU_Water_disag_BF_D_cba_med_approach = EU_Water_disag_BF_D_cba_avg_approach.iloc[:,0:27]
EU_Water_disag_BF_D_cba_con_approach = disag_BF_D_cba_con_approach.iloc[13:116].groupby(axis=1,level = 0, sort= False).sum()
EU_Water_disag_BF_D_cba_con_approach = EU_Water_disag_BF_D_cba_avg_approach.iloc[:,0:27]

### Now read in aggregated MRIO results using pre ordained Exiobase & LC-IMPACT Water categories ###

Agg_BF_D_cba_avg_approach = pd.read_csv(
    'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Autumn Project 2021/Biodiversity Footprint/BF_D_cba_2010_LCIA_Y_categories_agrifood_final_demand_average_approach.csv', index_col= [0], header= [0, 1], dtype = object)
Agg_BF_D_cba_avg_approach = Agg_BF_D_cba_avg_approach.astype(float)
Agg_BF_D_cba_med_approach = pd.read_csv(
    'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Autumn Project 2021/Biodiversity Footprint/BF_D_cba_2010_LCIA_Y_categories_agrifood_final_demand_median_approach.csv', index_col= [0], header= [0, 1], dtype= object)
Agg_BF_D_cba_med_approach = Agg_BF_D_cba_med_approach.astype(float)
Agg_BF_D_cba_con_approach = pd.read_csv(
    'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Autumn Project 2021/Biodiversity Footprint/BF_D_cba_2010_LCIA_Y_categories_agrifood_final_demand_continental_proxy_approach.csv', index_col= [0], header= [0, 1], dtype= object)
Agg_BF_D_cba_con_approach = Agg_BF_D_cba_con_approach.astype(float)

### Isolating Water Impacts ###

Water_Agg_BF_D_cba_avg_approach = Agg_BF_D_cba_avg_approach.iloc[25:128,:]
Water_Agg_BF_D_cba_med_approach = Agg_BF_D_cba_med_approach.iloc[25:128,:]
Water_Agg_BF_D_cba_con_approach = Agg_BF_D_cba_con_approach.iloc[25:128,:]

### EU economy only

EU_Water_Agg_BF_D_cba_avg_approach = Agg_BF_D_cba_avg_approach.iloc[25:128].groupby(axis=1,level = 0, sort= False).sum()
EU_Water_Agg_BF_D_cba_avg_approach = EU_Water_Agg_BF_D_cba_avg_approach.iloc[:,0:27]
EU_Water_Agg_BF_D_cba_med_approach = Agg_BF_D_cba_med_approach.iloc[25:128].groupby(axis=1,level = 0, sort= False).sum()
EU_Water_Agg_BF_D_cba_med_approach = EU_Water_Agg_BF_D_cba_med_approach.iloc[:,0:27]
EU_Water_Agg_BF_D_cba_con_approach = Agg_BF_D_cba_con_approach.iloc[25:128].groupby(axis=1,level = 0, sort= False).sum()
EU_Water_Agg_BF_D_cba_con_approach = EU_Water_Agg_BF_D_cba_con_approach.iloc[:,0:27]
print(EU_Water_Agg_BF_D_cba_avg_approach)
## Aggregating consumption categories ###

Total_Impacts_Water_Agg_BF_D_cba_avg_approach = Water_Agg_BF_D_cba_avg_approach.sum(1)  #summing countries
Total_Impacts_Water_Agg_BF_D_cba_avg_approach = Total_Impacts_Water_Agg_BF_D_cba_avg_approach.sum(0)  #summing consumption categories

Total_Impacts_Water_Agg_BF_D_cba_med_approach = Water_Agg_BF_D_cba_med_approach.sum(1)
Total_Impacts_Water_Agg_BF_D_cba_med_approach = Total_Impacts_Water_Agg_BF_D_cba_med_approach.sum(0)
Total_Impacts_Water_Agg_BF_D_cba_con_approach = Water_Agg_BF_D_cba_con_approach.sum(1)
Total_Impacts_Water_Agg_BF_D_cba_con_approach = Total_Impacts_Water_Agg_BF_D_cba_con_approach.sum(0)
Total_Impacts_EU_Water_Agg_BF_D_cba_avg_approach = EU_Water_Agg_BF_D_cba_avg_approach.sum(1)  #summing countries
Total_Impacts_EU_Water_Agg_BF_D_cba_avg_approach = Total_Impacts_EU_Water_Agg_BF_D_cba_avg_approach.sum(0)  #summing consumption categories
Total_Impacts_EU_Water_Agg_BF_D_cba_med_approach = EU_Water_Agg_BF_D_cba_med_approach.sum(1)
Total_Impacts_EU_Water_Agg_BF_D_cba_med_approach = Total_Impacts_EU_Water_Agg_BF_D_cba_med_approach.sum(0)
Total_Impacts_EU_Water_Agg_BF_D_cba_con_approach = EU_Water_Agg_BF_D_cba_con_approach.sum(1)
Total_Impacts_EU_Water_Agg_BF_D_cba_con_approach = Total_Impacts_EU_Water_Agg_BF_D_cba_con_approach.sum(0)


### Aggregating consumption categories ###

Total_Impacts_Water_disag_BF_D_cba_avg_approach = Water_disag_BF_D_cba_avg_approach.sum(1)  #summing countries
Total_Impacts_Water_disag_BF_D_cba_avg_approach = Total_Impacts_Water_disag_BF_D_cba_avg_approach .sum(0)  #summing consumption categories
Total_Impacts_Water_disag_BF_D_cba_med_approach = Water_disag_BF_D_cba_med_approach.sum(1)
Total_Impacts_Water_disag_BF_D_cba_med_approach = Total_Impacts_Water_disag_BF_D_cba_med_approach.sum(0)
Total_Impacts_Water_disag_BF_D_cba_con_approach = Water_disag_BF_D_cba_con_approach.sum(1)
Total_Impacts_Water_disag_BF_D_cba_con_approach = Total_Impacts_Water_disag_BF_D_cba_con_approach.sum(0)
Total_Impacts_EU_Water_disag_BF_D_cba_avg_approach = EU_Water_disag_BF_D_cba_avg_approach.sum(1)  #summing countries
Total_Impacts_EU_Water_disag_BF_D_cba_avg_approach = Total_Impacts_EU_Water_disag_BF_D_cba_avg_approach.sum(0)  #summing consumption categories
Total_Impacts_EU_Water_disag_BF_D_cba_med_approach = EU_Water_disag_BF_D_cba_med_approach.sum(1)
Total_Impacts_EU_Water_disag_BF_D_cba_med_approach = Total_Impacts_EU_Water_disag_BF_D_cba_med_approach.sum(0)
Total_Impacts_EU_Water_disag_BF_D_cba_con_approach = EU_Water_disag_BF_D_cba_con_approach.sum(1)
Total_Impacts_EU_Water_disag_BF_D_cba_con_approach = Total_Impacts_EU_Water_disag_BF_D_cba_con_approach.sum(0)

########################################################################################################################################
'''First check the total impact change in global economy  due to characterisation factor change '''

print((Total_Impacts_Water_disag_BF_D_cba_avg_approach - Total_Impacts_Water_Agg_BF_D_cba_avg_approach)) #/Total_Impacts_Water_Agg_BF_D_cba_avg_approach)
print((Total_Impacts_Water_disag_BF_D_cba_med_approach - Total_Impacts_Water_Agg_BF_D_cba_med_approach)) #/Total_Impacts_Water_Agg_BF_D_cba_med_approach)
print((Total_Impacts_Water_disag_BF_D_cba_con_approach - Total_Impacts_Water_Agg_BF_D_cba_con_approach)) #/Total_Impacts_Water_Agg_BF_D_cba_con_approach)

'''Check the total impact change in EU economy  due to characterisation factor change '''
print((Total_Impacts_EU_Water_disag_BF_D_cba_avg_approach - Total_Impacts_EU_Water_Agg_BF_D_cba_avg_approach)) #/Total_Impacts_EU_Water_Agg_BF_D_cba_avg_approach)
print((Total_Impacts_EU_Water_disag_BF_D_cba_med_approach - Total_Impacts_EU_Water_Agg_BF_D_cba_med_approach)) #/Total_Impacts_EU_Water_Agg_BF_D_cba_med_approach)
print((Total_Impacts_EU_Water_disag_BF_D_cba_con_approach - Total_Impacts_EU_Water_Agg_BF_D_cba_con_approach)) #/Total_Impacts_EU_Water_Agg_BF_D_cba_con_approach)


### Taking a look at the product categories and water consumption stressor categories ###
idx = pd.IndexSlice
EU_Water_Agg_BF_D_cba_avg_approach = pd.DataFrame(Agg_BF_D_cba_avg_approach.iloc[25:128])
EU_Water_Agg_BF_D_cba_avg_approach = EU_Water_Agg_BF_D_cba_avg_approach.loc[:, idx[['Austria', 'Belgium', 'Bulgaria', 'Cyprus', 'Czech Republic', 'Germany', 'Denmark', 'Estonia', 'Spain', 'Finland', 'France', 'Greece', 'Croatia', 'Hungary', 'Ireland', 'Italy', 'Lithuania', 'Luxembourg', 'Latvia', 'Malta', 'Netherlands', 'Poland', 'Portugal', 'Romania', 'Sweden', 'Slovenia', 'Slovakia'],:]].groupby(axis=1,level = 1, sort= False).sum()
EU_Water_Agg_BF_D_cba_avg_approach = EU_Water_Agg_BF_D_cba_avg_approach.sum(0).T
print(EU_Water_Agg_BF_D_cba_avg_approach)
EU_Water_Agg_BF_D_cba_med_approach = Agg_BF_D_cba_med_approach.iloc[25:128]
EU_Water_Agg_BF_D_cba_med_approach = EU_Water_Agg_BF_D_cba_med_approach.loc[:, idx[['Austria', 'Belgium', 'Bulgaria', 'Cyprus', 'Czech Republic', 'Germany', 'Denmark', 'Estonia', 'Spain', 'Finland', 'France', 'Greece', 'Croatia', 'Hungary', 'Ireland', 'Italy', 'Lithuania', 'Luxembourg', 'Latvia', 'Malta', 'Netherlands', 'Poland', 'Portugal', 'Romania', 'Sweden', 'Slovenia', 'Slovakia'],:]].groupby(axis=1,level = 1, sort= False).sum()
EU_Water_Agg_BF_D_cba_con_approach = Agg_BF_D_cba_con_approach.iloc[25:128]
EU_Water_Agg_BF_D_cba_con_approach = EU_Water_Agg_BF_D_cba_con_approach.loc[:, idx[['Austria', 'Belgium', 'Bulgaria', 'Cyprus', 'Czech Republic', 'Germany', 'Denmark', 'Estonia', 'Spain', 'Finland', 'France', 'Greece', 'Croatia', 'Hungary', 'Ireland', 'Italy', 'Lithuania', 'Luxembourg', 'Latvia', 'Malta', 'Netherlands', 'Poland', 'Portugal', 'Romania', 'Sweden', 'Slovenia', 'Slovakia'],:]].groupby(axis=1,level = 1, sort= False).sum()

