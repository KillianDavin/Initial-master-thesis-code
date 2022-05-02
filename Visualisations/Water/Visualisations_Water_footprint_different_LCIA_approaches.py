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
    '/data/processed/Biodiversity Footprint/EXIO3/Average approach/BF_D_cba_2010_LCIA_disaggregted_All_Y_categories_average_approach.csv', index_col= [0], header= [0, 1], dtype = object)
Dissag_BF_D_cba_avg_approach = Dissag_BF_D_cba_avg_approach.astype(float)
Dissag_BF_D_cba_med_approach = pd.read_csv(
    '/data/processed/Biodiversity Footprint/EXIO3/Median approach/BF_D_cba_2010_LCIA_disaggregted_All_Y_categories_median_approach.csv', index_col= [0], header= [0, 1], dtype= object)
Dissag_BF_D_cba_med_approach = Dissag_BF_D_cba_med_approach.astype(float)
Dissag_BF_D_cba_con_approach = pd.read_csv(
    '/data/processed/Biodiversity Footprint/EXIO3/Continental_proxy/BF_D_cba_2010_LCIA_disaggregted_All_Y_categories_continental_proxy_approach.csv', index_col= [0], header= [0, 1], dtype= object)
Dissag_BF_D_cba_con_approach = Dissag_BF_D_cba_con_approach.astype(float)

### Cleaning and prepping tables for visualisation ###
Water_disag_BF_D_cba_avg_approach = Dissag_BF_D_cba_avg_approach.iloc[13:116]
Water_disag_BF_D_cba_med_approach = Dissag_BF_D_cba_avg_approach.iloc[13:116]
Water_disag_BF_D_cba_con_approach = Dissag_BF_D_cba_con_approach.iloc[13:116]

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