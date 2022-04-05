import numpy as np
import pymrio
import pandas as pd

######################################################################################################################################################################################################################################################################

''' This file reads in the new EXIOBASE tables calculated in part 1 for the calculation of combined
S table and LC-IMPACT characterisation tables, followed by the calculation of Biodiversity Footprint accounts'''

######################################################################################################################################################################################################################################################################



exiobase3 = pymrio.load_all('C:/Users/Cillian/PycharmProjects/MRIO_project_Ver_01/Exiobase3 folder/Exiobase3 coefficient tables (latest)')


######################################################################################################################################################################################################################################################################

'''First section reads in Characterization Factor tables, and readjusts the index and columns as they become unattached when reading
between csv and pandas. Depending on the approach, different tables will be loaded here for the CF_tables variable.
CF Tables for the median approach will be loaded when median approach footprints are to be calculated and so on......
Layout of the CF tables can be seen in Appendix C of the project literature'''

##############################################################################################################################################
CF_tables = pd.read_csv('C:/Users/Cillian/OneDrive/Documents/NTNU project documents/CF sheets/CSV CF files/Full_CF_table_median_approach.csv')
index_labels = list(CF_tables.iloc[0:,0])
stressor_index_label = list(CF_tables.iloc[0:,1])
unit_labels_index = list(CF_tables.iloc[0:,2])
CF_tables = pd.DataFrame(CF_tables.iloc[0:,3:])
column_labels = CF_tables.columns.to_list()
CF_tables =CF_tables.values.astype(float)
CF_tables = pd.DataFrame(CF_tables,index=[stressor_index_label],columns= column_labels)

CF_tables.iloc[0:6,:] = CF_tables.iloc[0:6,:]*(10**6)  #coversion from m2 to km2 for land Characterisations, index 0-6 are the land CFs in the table
CF_tables.iloc[22:24, :] = CF_tables.iloc[22:24,:]*(10**6) #coversion from m3 to Mm3 for Water consumption as per exiobase, index 22 and 23 are the water CFs in the table
print(CF_tables)


###########################################################################################################################################################################################

'''The next section deals with characterizing the stressor table S, with the CF factors from table 'CF_tables'.
   The S table is broken out into smaller S_impact tables to match the various impact categories for characterization.
   The table is reformed after characterization as Char_table with units PDF per elementary flow.
   This section also calculates the characterized footprint of F_Y, which is the footprint related to household consumption or
   the impacts required for the consumption to take place.Multiplication is done via index location and for loops at different
   levels, according to indexs in the Stressor tables S_, F_Y, and CF_tables. '''

############################################################################################################################################################################################

S = pd.DataFrame(exiobase3.satellite.S)
S_land_occupation = pd.DataFrame(S.iloc[0:6,:])  #land stressors
S_climate_change = pd.DataFrame(S.iloc[6:25,:]) #climate change stressors
S_water_consumption = pd.DataFrame(S.iloc[25:128,:]) #water stressors
S_freshwater_eutrophication = pd.DataFrame(S.iloc[128:131,:])
S_freshwater_eutrophication = S_freshwater_eutrophication.append(S.iloc[132,:]) #freshwater eutrophication stressors
S_marine_eutrophication = pd.DataFrame(S.iloc[131,:]).T #Marine eutrophication stressors
Land_occupation_index = S_land_occupation.index.tolist()
Climate_change_index = S_climate_change.index.tolist()
Water_consumption_index = S_water_consumption.index.tolist()
Freshwater_eutrophication_index = S_freshwater_eutrophication.index.tolist()
stressors_index_required = Land_occupation_index + Climate_change_index + Water_consumption_index + Freshwater_eutrophication_index
print(S_marine_eutrophication)
print(S_marine_eutrophication.shape)

regions = exiobase3.get_regions()
labels = exiobase3.L.columns.to_list()
exiobase3.satellite.F_Y = pd.DataFrame(exiobase3.satellite.F_Y.iloc[0:133,:])


for stressor_index in range(0,6):   #There are 6 land categories to be characterized
    lower_range = 0
    upper_range= 200
    for CF_table_column_index in range(0,49):  #49 CF factors per impact pathway in CF_tables
        if upper_range <= 9800:
            for col in range(lower_range, upper_range):
                S_land_occupation.iat[stressor_index,col] = S_land_occupation.iat[stressor_index,col]*CF_tables.iat[stressor_index,CF_table_column_index]    #matching EXIOBASE indexing with that of the CF_tables

            lower_range += 200
            upper_range += 200

lower_range = 0
upper_range = 200
for CF_table_column_index in range(0,49):

    if upper_range <= 9800:
        for col in range(lower_range, upper_range):
            S_climate_change.iat[0,col] = S_climate_change.iat[0,col]*CF_tables.iat[6,CF_table_column_index] + S_climate_change.iat[0,col]*CF_tables.iat[14,CF_table_column_index]  #Core Characterisation of CO2 combustion stressors for terrestrial and aquatic climate change PDF
            S_climate_change.iat[1,col] = S_climate_change.iat[1, col] * CF_tables.iat[7, CF_table_column_index] + S_climate_change.iat[1, col] * CF_tables.iat[15, CF_table_column_index] #Core Characterisation of CH4 combustion stressors for terrestrial and aquatic climate change PDF
            S_climate_change.iat[2,col] = S_climate_change.iat[2, col] * CF_tables.iat[9, CF_table_column_index] + S_climate_change.iat[2, col] * CF_tables.iat[17, CF_table_column_index] #Core Characterisation of N20 combustion stressors for terrestrial and aquatic climate change PDF
            S_climate_change.iat[13,col] = S_climate_change.iat[13, col] * CF_tables.iat[7, CF_table_column_index] + S_climate_change.iat[13,col] * CF_tables.iat[15,CF_table_column_index]  # Core characterisation of methane release from agriculture for terrestrial and aquatic climate change PDF
            S_climate_change.iat[14, col] = S_climate_change.iat[14, col] * CF_tables.iat[6, CF_table_column_index] + S_climate_change.iat[14,col] * CF_tables.iat[14,CF_table_column_index]  # Core characterisation of CO2 release from peat decay in agriculture for terrestrial and aquatic climate change PDF
            S_climate_change.iat[15, col] = S_climate_change.iat[15, col] * CF_tables.iat[9, CF_table_column_index] + S_climate_change.iat[15,col] * CF_tables.iat[17,CF_table_column_index]  # Core characterisation of N20 release from agriculture for terrestrial and aquatic climate change PDF
            S_climate_change.iat[16, col] = S_climate_change.iat[16, col] * CF_tables.iat[7, CF_table_column_index] + S_climate_change.iat[16,col] * CF_tables.iat[16,CF_table_column_index]  # Core characterisation of methane release from waste for terrestrial and aquatic climate change PDF
        lower_range += 200
        upper_range += 200


for stressor_index in range(3,11):
    lower_range = 0
    upper_range = 200
    for CF_table_column_index in range(0, 49):
        if upper_range <= 9800:
            for col in range(lower_range, upper_range):
                S_climate_change.iat[stressor_index, col] = S_climate_change.iat[stressor_index, col] * CF_tables.iat[8, CF_table_column_index] + S_climate_change.iat[stressor_index, col] * CF_tables.iat[16, CF_table_column_index] #Core characterisation of fossil Methane non combustion stressors for terrestrial and aquatic climate change PDF
        lower_range += 200
        upper_range += 200


for stressor_index in range(11,13):
    lower_range = 0
    upper_range = 200
    for CF_table_column_index in range(0, 49):
        if upper_range <= 9800:
            for col in range(lower_range, upper_range):
                S_climate_change.iat[stressor_index, col] = S_climate_change.iat[stressor_index, col] * CF_tables.iat[6, CF_table_column_index] + S_climate_change.iat[stressor_index, col] * CF_tables.iat[14, CF_table_column_index] #Core characterisation of non combustive CO2 release from cement/lime production for terrestrial and aquatic climate change PDF
        lower_range += 200
        upper_range += 200

for stressor_index in range(17,19):
    lower_range = 0
    upper_range = 200
    for CF_table_column_index in range(0, 49):
        if upper_range <= 9800:
            for col in range(lower_range, upper_range):
                S_climate_change.iat[stressor_index, col] = S_climate_change.iat[stressor_index, col] * CF_tables.iat[6, CF_table_column_index] + S_climate_change.iat[stressor_index, col] * CF_tables.iat[14, CF_table_column_index] #Core characterisations of CO2 for fossil and biogenic waste for terrestrial and aquatic climate change PDF

        lower_range += 200
        upper_range += 200


for stressor_index in range(0,103): #103 water stressors, to be characterized by the same core LC-IMPACT factors per country
    lower_range = 0
    upper_range = 200
    for CF_table_column_index in range(0, 49):
        if upper_range <= 9800:
            for col in range(lower_range, upper_range):
                S_water_consumption.iat[stressor_index, col] = S_water_consumption.iat[stressor_index, col] * CF_tables.iat[22, CF_table_column_index] #Core characterisation of water consumption stressors. There are 103 water stressors, hence the range in the for loop
        lower_range += 200
        upper_range += 200


lower_range = 0
upper_range= 200
for CF_table_column_index in range(0, 49):
    if upper_range <= 9800:
        for col in range(lower_range, upper_range):
            S_freshwater_eutrophication.iat[0,col] = S_freshwater_eutrophication.iat[0,col]*CF_tables.iat[28,CF_table_column_index] #Characterisation of agricultural phosphorus emissions to soil stressors for freshwater eutrophication impact category
            S_freshwater_eutrophication.iat[2,col] = S_freshwater_eutrophication.iat[2,col]*CF_tables.iat[28,CF_table_column_index] #Characterisation of agricultural phosphorus emissions to soil stressors for freshwater eutrophication impact category
            S_freshwater_eutrophication.iat[1,col] = S_freshwater_eutrophication.iat[1,col]*CF_tables.iat[27,CF_table_column_index] #Characterisation of agricultural phosphorus emissions to water stressors for freshwater eutrophication impact category
            S_freshwater_eutrophication.iat[3,col] = S_freshwater_eutrophication.iat[3,col]*CF_tables.iat[27,CF_table_column_index] #Characterisation of agricultural phosphorus emissions to water stressors for freshwater eutrophication impact category
    lower_range += 200
    upper_range += 200

lower_range = 0
upper_range= 200
for CF_table_column_index in range(0,49):
    if upper_range <= 9800:
        for col in range(lower_range, upper_range):
            S_marine_eutrophication.iat[0,col] = S_marine_eutrophication.iat[0,col]*CF_tables.iat[25,CF_table_column_index]
    lower_range += 200
    upper_range += 200



Char_table_S = pd.DataFrame(S_land_occupation)   #New characterized S tables
Stressor_tables = [S_climate_change,S_water_consumption,S_freshwater_eutrophication,S_marine_eutrophication]

for stressor in Stressor_tables:
    Char_table_S = Char_table_S.append(stressor)  #Fully formed - New characterized S tables
Char_table_S.to_csv('Char_table_S.csv')


############################################################################################################################################################################################

''' Same method completed for F_Y tables'''

############################################################################################################################################################################################
for stressor_index in range(0, 6):
    for CF_table_column_index in range(0, 49):
        exiobase3.satellite.F_Y.iat[stressor_index, CF_table_column_index] = CF_tables.iat[stressor_index, CF_table_column_index] * exiobase3.satellite.F_Y.iat[stressor_index, CF_table_column_index]

for CF_table_column_index in range(0,49):
    exiobase3.satellite.F_Y.iat[6, CF_table_column_index] = CF_tables.iat[6, CF_table_column_index] * exiobase3.satellite.F_Y.iat[6, CF_table_column_index] #Core Characterisation of CO2 combustion stressors for terrestrial and aquatic climate change PDF
    exiobase3.satellite.F_Y.iat[7, CF_table_column_index] = CF_tables.iat[7, CF_table_column_index] * exiobase3.satellite.F_Y.iat[7, CF_table_column_index] #Core Characterisation of CH4 combustion stressors for terrestrial and aquatic climate change PDF
    exiobase3.satellite.F_Y.iat[8, CF_table_column_index] = CF_tables.iat[9, CF_table_column_index] * exiobase3.satellite.F_Y.iat[8, CF_table_column_index] # Core characterisation of methane release from agriculture for terrestrial and aquatic climate change PDF
    exiobase3.satellite.F_Y.iat[19, CF_table_column_index] = CF_tables.iat[7, CF_table_column_index] * exiobase3.satellite.F_Y.iat[19, CF_table_column_index] # Core characterisation of methane release from agriculture for terrestrial and aquatic climate change PDF
    exiobase3.satellite.F_Y.iat[20, CF_table_column_index] = CF_tables.iat[6, CF_table_column_index] * exiobase3.satellite.F_Y.iat[20, CF_table_column_index] # Core characterisation of CO2 release from peat decay in agriculture for terrestrial and aquatic climate change PDF
    exiobase3.satellite.F_Y.iat[21, CF_table_column_index] = CF_tables.iat[9, CF_table_column_index] * exiobase3.satellite.F_Y.iat[21, CF_table_column_index] # Core characterisation of N20 release from agriculture for terrestrial and aquatic climate change PDF
    exiobase3.satellite.F_Y.iat[22, CF_table_column_index] = CF_tables.iat[7, CF_table_column_index] * exiobase3.satellite.F_Y.iat[22, CF_table_column_index] # Core characterisation of methane release from waste for terrestrial and aquatic climate change PDF

for stressor_index in range(3,11):
    for CF_table_column_index in range(0, 49):
        exiobase3.satellite.F_Y.iat[stressor_index+6, CF_table_column_index] = CF_tables.iat[8, CF_table_column_index] * exiobase3.satellite.F_Y.iat[stressor_index+6, CF_table_column_index]  #Core characterisation of fossil Methane non combustion stressors for terrestrial and aquatic climate change PDF
for stressor_index in range(11,13):
    for CF_table_column_index in range(0, 49):
            exiobase3.satellite.F_Y.iat[stressor_index+6, CF_table_column_index] = CF_tables.iat[6, CF_table_column_index] * exiobase3.satellite.F_Y.iat[stressor_index+6, CF_table_column_index]  #Core characterisation of fossil Methane non combustion stressors for terrestrial and aquatic climate change PDF
for stressor_index in range(17,19):
    for CF_table_column_index in range(0, 49):
            exiobase3.satellite.F_Y.iat[stressor_index + 6, CF_table_column_index] = CF_tables.iat[6, CF_table_column_index] * exiobase3.satellite.F_Y.iat[stressor_index + 6, CF_table_column_index]  #Core characterisations of CO2 for fossil and biogenic waste for terrestrial and aquatic climate change PDF

for stressor_index in range(0,103):
    for CF_table_column_index in range(0, 49):
            exiobase3.satellite.F_Y.iat[stressor_index + 25, CF_table_column_index] = CF_tables.iat[22,CF_table_column_index]*exiobase3.satellite.F_Y.iat[stressor_index + 25, CF_table_column_index] #Core characterisation of water consumption stressors. There are 103 water stressors, hence the range in the for loop

for CF_table_column_index in range(0, 49):
    exiobase3.satellite.F_Y.iat[128, CF_table_column_index] = CF_tables.iat[28,CF_table_column_index]*exiobase3.satellite.F_Y.iat[128, CF_table_column_index] #Characterisation of agricultural phosphorus emissions to soil stressors for freshwater eutrophication impact category
    exiobase3.satellite.F_Y.iat[130, CF_table_column_index] = CF_tables.iat[28,CF_table_column_index]*exiobase3.satellite.F_Y.iat[130, CF_table_column_index] #Characterisation of agricultural phosphorus emissions to soil stressors for freshwater eutrophication impact category
    exiobase3.satellite.F_Y.iat[129, CF_table_column_index] = CF_tables.iat[27,CF_table_column_index]*exiobase3.satellite.F_Y.iat[129, CF_table_column_index] #Characterisation of agricultural phosphorus emissions to water stressors for freshwater eutrophication impact category
    exiobase3.satellite.F_Y.iat[132, CF_table_column_index] = CF_tables.iat[27,CF_table_column_index]*exiobase3.satellite.F_Y.iat[131, CF_table_column_index] #Characterisation of agricultural phosphorus emissions to water stressors for freshwater eutrophication impact category

for CF_table_column_index in range(0,49):
    exiobase3.satellite.F_Y.iat[131, CF_table_column_index] = CF_tables.iat[25,CF_table_column_index]*exiobase3.satellite.F_Y.iat[131, CF_table_column_index] #Characterisation of Nitrogen emissions to wastewater for Marine eutrophication impact category.

#Re-ordering F_Y stressor table so it matches index of D_cba and D_pba for addition below
Nitrogen_df = pd.DataFrame(exiobase3.satellite.F_Y.iloc[131,:]).T

Nitrogen_df.astype(float)

Phosphoros_df = pd.DataFrame(exiobase3.satellite.F_Y.iloc[132,:]).T
Phosphoros_df.astype(float)
Appending_group = (Phosphoros_df,Nitrogen_df)
exiobase3.satellite.F_Y = pd.DataFrame(exiobase3.satellite.F_Y.iloc[0:131,:])
for i in Appending_group:
    exiobase3.satellite.F_Y = exiobase3.satellite.F_Y.append(i)
print(exiobase3.satellite.F_Y.shape)
print(exiobase3.satellite.F_Y)

F_Y_biod = pd.DataFrame(exiobase3.satellite.F_Y)



######################################################################################################################################################################################################################################

''' This section deals with the quantification of the Biodiversity footprints
following the characterization of the stressors above'''

#############################################################################################################################################################################################################################

regions = exiobase3.get_regions()

new_accounts = pymrio.calc_accounts(Char_table_S, exiobase3.L, exiobase3.Y, nr_sectors=200)  #Note here, we input Char_table_S rather than S for the calculation of the Biodiversity accounts

D_cba_biod = pd.DataFrame(new_accounts[0])
print(D_cba_biod.shape)
D_pba_biod = pd.DataFrame(new_accounts[1])


D_imp_biod = pd.DataFrame(new_accounts[2])
D_imp_biod.to_csv('D_imp_biod.csv')

D_exp_biod = pd.DataFrame(new_accounts[3])
D_exp_biod.to_csv('D_exp_biod.csv')

######################################################################################################################################################################################################################################
'''For calculating total footprint with F_Y'''
######################################################################################################################################################################################################################################

D_cba_total = pd.DataFrame(D_cba_biod.groupby(axis = 1, level=0,sort=False).sum())  #Changing shape of D_cba from 153x9800 to 152x49 for matrix addition with F_Y
D_cba_total = D_cba_total.add(F_Y_biod.values) #matrix addition
D_cba_total.to_csv('D_cba_total_median.csv')
D_pba_total = pd.DataFrame(D_pba_biod.groupby(axis = 1, level=0,sort=False).sum()) #Changing shape of D_pba from 153x9800 to 152x49 for matrix addition with F_Y
D_pba_total = D_pba_total.add(F_Y_biod.values)   #matrix addition
D_pba_total.to_csv('D_pba_total_median.csv')