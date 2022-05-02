import pymrio
import pandas as pd
import numpy as np

##################################################################################################################################################################################################################

'''Load tables from original exiobase 2010 parsed files
   that were downloaded and parsed from the EXIOBASE Zenodo repository.
   IOT_2010_pxp 2011.zip file from version 3.8.1 of EXIOBASE '''

##################################################################################################################################################################################################################
years = range(2010, 2011)
for n, year in enumerate(years):
    print(n, year)
    exio3_folder = "C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO3"
    exio_meta = pymrio.download_exiobase3(storage_folder=exio3_folder, system="pxp", years=[year])
    year = str(year)
    file_path = 'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO3/IOT_'+ year +'_pxp.zip'
   # print(file_path)
    exiobase3 = pymrio.parse_exiobase3(path= file_path)
    S = pd.DataFrame(exiobase3.satellite.S)
    Y = pd.DataFrame(exiobase3.Y)
    # Y = Y.groupby(level= 0, axis = 1, sort = False).sum(1)   ### All consumption categories included
    idx = pd.IndexSlice  # Slicing of multi index columns for separating out multiindex columns
    #Y = pd.DataFrame(
        #Y.loc[:, idx[:, 'Final consumption expenditure by households']])  # Seggregating final consumer household demand
    #Y.columns = Y.columns.droplevel(1)
    exiobase3.Y = pd.DataFrame(Y)  # New Y tables in terms of 'Final consumption by households only'
##################################################################################################################
''' Seggregating desired final demand categories'''
##################################################################################################################

Desired_final_demand_categories = pd.DataFrame(Y.loc[idx[:, ['Paddy rice', 'Wheat', 'Cereal grains nec', 'Vegetables, fruit, nuts', 'Oil seeds',
                    'Sugar cane, sugar beet', 'Plant-based fibers', 'Crops nec', 'Cattle', 'Pigs', 'Poultry',
                    'Meat animals nec', 'Animal products nec', 'Raw milk',
                    'Fish and other fishing products; services incidental of fishing (05)', 'Food products nec',
                    'Beverages', 'Sugar', 'Fish products', 'Dairy products',
                    'Products of meat cattle', 'Products of meat pigs', 'Products of meat poultry', 'Meat products nec',
                    'products of Vegetable oils and fats', 'Processed rice']],:])

Y.loc[:,:] = 0.0
Y.loc[idx[:, ['Paddy rice', 'Wheat', 'Cereal grains nec', 'Vegetables, fruit, nuts', 'Oil seeds',
                  'Sugar cane, sugar beet', 'Plant-based fibers', 'Crops nec', 'Cattle', 'Pigs', 'Poultry',
                  'Meat animals nec', 'Animal products nec', 'Raw milk',
                  'Fish and other fishing products; services incidental of fishing (05)', 'Food products nec',
                  'Beverages', 'Sugar', 'Fish products', 'Dairy products',
                  'Products of meat cattle', 'Products of meat pigs', 'Products of meat poultry', 'Meat products nec',
                  'products of Vegetable oils and fats', 'Processed rice']], :] = Desired_final_demand_categories.values


##################################################################################################################################################################################################################


'''Segregating required stressors from S tables. Segregation is completed via index referencing of original tables.
   Details on stressors and S table row index, see Appendix F in project literature'''

##################################################################################################################################################################################################################


land_stressors = pd.DataFrame(S.iloc[[446,447,448,449,450,451,452,453,454,455,456,457,458,459, 461,462,463,464,465],:])  #Seperation of land use categories using indexing. Rows obtained from csv file
water_stressors = pd.DataFrame(S.iloc[923:1026])  #Blue water consumption stressor rows
climate_change_stressors = pd.DataFrame(S.iloc[[23,24,25,67,68,69,70,71,72,73,74,92,93,426,427,429,435,437,438]]) #Climate change stressor rows
eutrophication_stressors = pd.DataFrame(S.iloc[[432,433,434,440,443]]) #Marine and Fresh eutrophication

#Aggregation of exiobase land use categories to LC-IMPACT categories

Annual_crop_df = pd.DataFrame(land_stressors.iloc[[0,1,7,8,9,10,12],:])
Fodder_crop_df = pd.DataFrame(land_stressors.iloc[[2,3,4,5,6],:]).sum(0) #Aggregation of the fodder crop categories in exiobase to the singular LC-IMPACT category for Land Use
print(Annual_crop_df)
Fodder_crop_df = pd.DataFrame(Fodder_crop_df).T #As python outputs a column vector for a summation operation, the transpose function T is used to return the annual crop dataframe to it's original Dataframe index/column set up with countries and products as the column index and stressor as the row index.
Permanent_crop_df = pd.DataFrame(land_stressors.iloc[[11],:]).sum(0)  #Aggregation of permanent crop categories to LC-Impact land category
Permanent_crop_df = pd.DataFrame(Permanent_crop_df).T   #Transposing to original Dataframe layout.
Pasture_crop_df = pd.DataFrame(land_stressors.iloc[[14,15,16],:]).sum(0) #Aggregation of Pasture crop land use categories
print(Annual_crop_df)
Pasture_crop_df = pd.DataFrame(Pasture_crop_df).T
Urban_df = pd.DataFrame(land_stressors.iloc[[17],:]).sum(0) #Aggregation of Urban land use categories
Urban_df = pd.DataFrame(Urban_df).T
Intensive_forestry_df = pd.DataFrame(land_stressors.iloc[[13],:]).sum(0) #Aggregation of Intensive forestry land use stresors to LC-Impact category
Intensive_forestry_df = pd.DataFrame(Intensive_forestry_df).T
Extensive_forestry_df = pd.DataFrame(land_stressors.iloc[[18],:]).sum(0) #Aggregation of Intensive forestry land use stresors to LC-Impact
Extensive_forestry_df = pd.DataFrame(Extensive_forestry_df).T

#Re-creating a combined dataframe for the aggregated land use stressors

Land_aggregated_df = Annual_crop_df
landuse_list = (Fodder_crop_df,Permanent_crop_df,Pasture_crop_df,Urban_df,Extensive_forestry_df,Intensive_forestry_df)
new_land_categories_index = ('Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice', 'Plant-based fibers','Sugar','Wheat', 'Fodder crops', 'Permanent Crops', 'Pasture', 'Urban', 'Extensive forestry', 'Intensive forestry')
for i in landuse_list :
    Land_aggregated_df = Land_aggregated_df.append(i)   #Appending Land_aggregated_df with each of the aggregated land use categories

Land_aggregated_df.reset_index()
Land_aggregated_df.set_axis(new_land_categories_index, inplace=True) #Updating the index row labels

#Combining the aggregated land use stressor categories with the disaggregated land use stressors, and the stressors for the other impact categories being analysed. This is the final compiled stressor matrix.
#Not necessary to add land stressors, but nice to have for future reference if required.

stressor_list = (climate_change_stressors,water_stressors,eutrophication_stressors,land_stressors)
exiobase3.satellite.S = Land_aggregated_df  #Full_stressor_list = All required stressors (aggregated and disaggregated) for footprint calculations
for i in stressor_list :
    exiobase3.satellite.S = exiobase3.satellite.S.append(i)

S = pd.DataFrame(exiobase3.satellite.S)
S.to_csv('S_check.csv')
##################################################################################################################################################################################################################

'''Segregating required stressors from S_Y tables in exactly the same fashion as what was completed above for the S tables'''

##################################################################################################################################################################################################################

S_Y = pd.DataFrame(exiobase3.satellite.S_Y)
land_stressors_S_Y = pd.DataFrame(S_Y.iloc[[446,447,448,449,450,451,452,453,454,455,456,457,458,459, 461,462,463,464,465],:])  #Seperation of land use categories using indexing. Rows obtained from csv file
water_stressors_S_Y = pd.DataFrame(S_Y.iloc[923:1026])  #Blue water consumption stressor rows
climate_change_stressors_S_Y = pd.DataFrame(S_Y.iloc[[23,24,25,67,68,69,70,71,72,73,74,92,93,426,427,429,435,437,438]]) #Global warming stressor rows
eutrophication_stressors_S_Y = pd.DataFrame(S_Y.iloc[[432,433,434,440,443]]) #Marine and Fresh eutrophication

#Combining the aggregated land use stressor categories with the disaggregated land use stressors, and the stressors for the other impact categories being analysed. This is the final compiled stressor matrix.

#Aggregation of exiobase land use categories to LC-IMPACT categories_S_Y

Fodder_crop_df_S_Y = pd.DataFrame(land_stressors_S_Y.iloc[[2,3,4,5,6],:]).sum(0) #Aggregation of the annual crop categories in exiobase to the singular LC-IMPACT category for Land Use
Fodder_crop_df_S_Y = pd.DataFrame(Fodder_crop_df_S_Y).T #As python outputs a column vector for a sumation operation, the transpose function T is used to return the annual crop dataframe to it's original Dataframe index/column set up with countries and products as the column index and stressor as the row index.
Annual_crop_df_S_Y = pd.DataFrame(land_stressors_S_Y.iloc[[0,1,7,8,9,10,12],:])
Permanent_crop_df_S_Y = pd.DataFrame(land_stressors_S_Y.iloc[[11],:]).sum(0)  #Aggregation of permanent crop categories to LC-Impact land category
Permanent_crop_df_S_Y = pd.DataFrame(Permanent_crop_df_S_Y).T   #Transposing to original Dataframe layout.
Pasture_crop_df_S_Y = pd.DataFrame(land_stressors_S_Y.iloc[[14,15,16],:]).sum(0) #Aggregation of Pasture crop land use categories
Pasture_crop_df_S_Y = pd.DataFrame(Pasture_crop_df_S_Y).T
Urban_df_S_Y = pd.DataFrame(land_stressors_S_Y.iloc[[17],:]).sum(0) #Aggregation of Urban land use categories
Urban_df_S_Y = pd.DataFrame(Urban_df_S_Y).T
Intensive_forestry_df_S_Y = pd.DataFrame(land_stressors_S_Y.iloc[[13],:]).sum(0) #Aggregation of Intensive forestry land use stresors to LC-Impact category
Intensive_forestry_df_S_Y = pd.DataFrame(Intensive_forestry_df_S_Y).T
Extensive_forestry_df_S_Y = pd.DataFrame(land_stressors_S_Y.iloc[[18],:]).sum(0) #Aggregation of Intensive forestry land use stresors to LC-Impact
Extensive_forestry_df_S_Y = pd.DataFrame(Extensive_forestry_df_S_Y).T

#Re-creating a combined dataframe for the aggregated land use stressors_F_Y

Land_aggregated_df_S_Y = Annual_crop_df_S_Y
landuse_list = (Fodder_crop_df_S_Y,Permanent_crop_df_S_Y,Pasture_crop_df_S_Y,Urban_df_S_Y,Extensive_forestry_df_S_Y,Intensive_forestry_df_S_Y)
new_land_categories_index = ('Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice', 'Plant-based fibers','Sugar','Wheat', 'Fodder crops', 'Permanent Crops', 'Pasture', 'Urban', 'Extensive forestry', 'Intensive forestry')
for i in landuse_list :
    Land_aggregated_df_S_Y = Land_aggregated_df_S_Y.append(i)   #Appending Land_aggregated_df with each of the aggregated land use categories

Land_aggregated_df_S_Y.reset_index()
Land_aggregated_df_S_Y.set_axis(new_land_categories_index, inplace=True) #Updating the index row labels

#Combining the aggregated land use stressor categories with the disaggregated land use stressors, and the stressors for the other impact categories being analysed. This is the final compiled stressor matrix for F_Y.

stressor_list_S_Y = (climate_change_stressors_S_Y,water_stressors_S_Y,eutrophication_stressors_S_Y,land_stressors_S_Y)
exiobase3.satellite.S_Y = Land_aggregated_df_S_Y  #Full_stressor_list = All required stressors (aggregated and disaggregated) for footprint calculations
for i in stressor_list_S_Y :
    exiobase3.satellite.S_Y = exiobase3.satellite.S_Y.append(i)

#exiobase3.satellite.S_Y = pd.DataFrame(exiobase3.satellite.S_Y.loc[:,idx[:,'Final consumption expenditure by households']])  #Seggregating final consumer househould expenditure
#exiobase3.satellite.S_Y = pd.DataFrame(exiobase3.satellite.S_Y.loc[:, idx[:,'Final consumption expenditure by households']])  # Seggregating final consumer househould expenditure
S_Y = pd.DataFrame(exiobase3.satellite.S_Y)


##################################################################################################################################################################################################################

'''With a new Y table, S table and S_Y table, all other tables are reset to the co-efficients
    for the recalculation of new x,F,Z,M tables. Resetting of coefficients with pymrio resets all tables in EXIOBASE other than the
    A and L matrices'''


##################################################################################################################################################################################################################

exiobase3.reset_all_to_coefficients()
print(exiobase3.A) #9800x9800
exiobase3.L = pymrio.calc_L(exiobase3.A)
print(exiobase3.L) #9800x9800
print(exiobase3.x) #0
print(exiobase3.satellite.F) #0
print(exiobase3.Z) #0
print(exiobase3.satellite.M) #0
exiobase3.Y = pd.DataFrame(Y)  #Setting Y tables to Y tables formed in the first section of the code
exiobase3.satellite.S = pd.DataFrame(S) #Setting S tables to S tables formed in the second section of the code
exiobase3.satellite.S_Y = pd.DataFrame(S_Y) #Setting S_Y tables to S_Y tables formed in third section of the code
Y = exiobase3.Y
exiobase3.x = pymrio.calc_x_from_L(exiobase3.L, exiobase3.Y.sum(1)) #Using PYMRIO functionality to calculate x from L and Y tables
exiobase3.x.to_csv('x_check.csv')

exiobase3.Z = pymrio.calc_Z(exiobase3.A, exiobase3.x) #Using PYMRIO functionality to calculate Z from A and x tables


exiobase3.satellite.F_Y = pd.DataFrame(pymrio.calc_F_Y(exiobase3.satellite.S_Y,pd.DataFrame(exiobase3.Y.sum(0)).T))
print(exiobase3.satellite.F_Y.shape)
exiobase3.satellite.F = pd.DataFrame(pymrio.calc_F(exiobase3.satellite.S,exiobase3.x))
print(exiobase3.satellite.S)
print(exiobase3.satellite.F)
print(exiobase3.satellite.F_Y)
print(exiobase3.satellite.F.shape)
exiobase3.M = pd.DataFrame(pymrio.calc_M(exiobase3.satellite.S,exiobase3.L))
exiobase3.Y = pd.DataFrame(Y.groupby(level=0, axis=1, sort=False).sum(1))

#######################################################################################################################################################################################################################################################################

'''First section reads in Characterization Factor tables, and readjusts the index and columns as they become unattached when reading
between csv and pandas. Depending on the approach, different tables will be loaded here for the CF_tables variable.
CF Tables for the median approach will be loaded when median approach footprints are to be calculated and so on......
Layout of the CF tables can be seen in Appendix C of the project literature'''

##############################################################################################################################################

CF_tables = pd.read_csv('C:/Users/Cillian/OneDrive - NTNU/Documents/NTNU project documents/CF sheets/Land_characterisation_thesis/Full_CF_table_continental_proxy_approach.csv')
index_labels = list(CF_tables.iloc[0:,0])
stressor_index_label = list(CF_tables.iloc[0:,1])
unit_labels_index = list(CF_tables.iloc[0:,2])
CF_tables = pd.DataFrame(CF_tables.iloc[0:,3:])
column_labels = CF_tables.columns.to_list()
CF_tables =CF_tables.values.astype(float)
CF_tables = pd.DataFrame(CF_tables,index=[stressor_index_label],columns= column_labels)

CF_tables.iloc[0:6,:] = CF_tables.iloc[0:6,:]*(10**6)  #coversion from m2 to km2 for land Characterisations, index 0-6 are the land CFs in the table
CF_tables.iloc[22:24, :] = CF_tables.iloc[22:24,:]*(10**6) #coversion from m3 to Mm3 for Water consumption as per exiobase, index 22 and 23 are the water CFs in the table



###########################################################################################################################################################################################

'''The next section deals with characterizing the stressor table S, with the CF factors from table 'CF_tables'.
   The S table is broken out into smaller S_impact tables to match the various impact categories for characterization.
   The table is reformed after characterization as Char_table with units PDF per elementary flow.
   This section also calculates the characterized footprint of F_Y, which is the footprint related to household consumption or
   the impacts required for the consumption to take place.Multiplication is done via index location and for loops at different
   levels, according to indexs in the Stressor tables S_, F_Y, and CF_tables. '''

############################################################################################################################################################################################

S = pd.DataFrame(exiobase3.satellite.S)
S_land_occupation = pd.DataFrame(S.iloc[0:13,:])  #land stressors
S_climate_change = pd.DataFrame(S.iloc[13:32,:]) #climate change stressors
S_water_consumption = pd.DataFrame(S.iloc[32:135,:]) #water stressors
S_freshwater_eutrophication = pd.DataFrame(S.iloc[135:138,:])
S_freshwater_eutrophication = S_freshwater_eutrophication.append(S.iloc[139,:]) #freshwater eutrophication stressors
S_marine_eutrophication = pd.DataFrame(S.iloc[138,:]).T #Marine eutrophication stressors
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


for stressor_index in range(0,8):   #There are 6 land categories to be characterized
    lower_range = 0
    upper_range= 200
    for CF_table_column_index in range(0,49):  #49 CF factors per impact pathway in CF_tables
        if upper_range <= 9800:
            for col in range(lower_range, upper_range):
                S_land_occupation.iat[stressor_index,col] = S_land_occupation.iat[stressor_index,col]*CF_tables.iat[0,CF_table_column_index]    #matching EXIOBASE indexing with that of the CF_tables

            lower_range += 200
            upper_range += 200

n = 0           
for stressor_index in range(8,13):   #There are 6 land categories to be characterized
    lower_range = 0
    upper_range= 200 
    n += 1
    for CF_table_column_index in range(0,49):  #49 CF factors per impact pathway in CF_tables
        if upper_range <= 9800:
            for col in range(lower_range, upper_range):
                S_land_occupation.iat[stressor_index,col] = S_land_occupation.iat[stressor_index,col]*CF_tables.iat[n,CF_table_column_index]    #matching EXIOBASE indexing with that of the CF_tables

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

Char_table_S.to_csv('S_check.csv)')

############################################################################################################################################################################################

''' Same method completed for F_Y tables'''

############################################################################################################################################################################################

for stressor_index in range(0, 8):
    for CF_table_column_index in range(0, 49):
        exiobase3.satellite.F_Y.iat[stressor_index, CF_table_column_index] = CF_tables.iat[0, CF_table_column_index] * exiobase3.satellite.F_Y.iat[stressor_index, CF_table_column_index]

n = 0
for stressor_index in range(8, 13):
    n += 1
    for CF_table_column_index in range(0, 49):
        exiobase3.satellite.F_Y.iat[stressor_index, CF_table_column_index] = CF_tables.iat[n, CF_table_column_index] * exiobase3.satellite.F_Y.iat[stressor_index, CF_table_column_index]

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

exiobase3.satellite.S = pd.DataFrame(Char_table_S)

exiobase3.rename_regions(
    {'AT': 'Austria', 'BE': 'Belgium', 'BG': 'Bulgaria', 'CZ': 'Czech Republic', 'CY': 'Cyprus', 'DE': 'Germany',
     'DK': 'Denmark', 'EE': 'Estonia',
     'ES': 'Spain', 'FR': 'France', 'FI': 'Finland', 'GR': 'Greece', 'HU': 'Hungary', 'HR': 'Croatia', 'IE': 'Ireland',
     'IT': 'Italy', 'LT': 'Lithuania', 'LV': 'Latvia', 'LU': 'Luxembourg',
     'MT': 'Malta', 'NL': 'Netherlands', 'PL': 'Poland', 'PT': 'Portugal', 'SE': 'Sweden', 'SK': 'Slovakia',
     'SI': 'Slovenia', 'RO': 'Romania',
     'GB': 'Great Britain', 'US': 'United States', 'CN': 'China', 'CA': 'Canada', 'JP': 'Japan', 'IN': 'India',
     'ID': 'Indonesia',
     'KR': 'South Korea', 'RU': 'Russia', 'NO': 'Norway', 'CH': 'Switzerland', 'TW': 'Taiwan', 'TR': 'Turkey',
     'ZA': 'South Africa', 'BR': 'Brazil',
     'MX': 'Mexico', 'AU': 'Australia', 'WA': 'RoW_Asia_and_Pacific', 'WF': 'RoW_Africa', 'WL': 'RoW_America',
     'WM': 'RoW_Middle_East', 'WE': 'RoW_Europe'})

new_accounts = pymrio.calc_accounts(exiobase3.satellite.S, exiobase3.L, exiobase3.Y)  #Note here, we input Char_table_S rather than S for the calculation of the Biodiversity accounts

D_cba = pd.DataFrame(new_accounts[0])
D_cba = pd.DataFrame(D_cba.loc[:, idx[:, ['Paddy rice', 'Wheat', 'Cereal grains nec', 'Vegetables, fruit, nuts', 'Oil seeds',
                          'Sugar cane, sugar beet', 'Plant-based fibers', 'Crops nec', 'Cattle', 'Pigs', 'Poultry',
                          'Meat animals nec', 'Animal products nec', 'Raw milk',
                          'Fish and other fishing products; services incidental of fishing (05)', 'Food products nec','Beverages', 'Sugar', 'Fish products', 'Dairy products',
                          'Products of meat cattle', 'Products of meat pigs', 'Products of meat poultry', 'Meat products nec', 'products of Vegetable oils and fats', 'Processed rice']]])
D_cba.to_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Autumn Project 2021/Biodiversity Footprint/Dissagregated_BF_D_cba_2010_LCIA_household_Y_categories_agrifood_final_demand_continental_proxy_approach.csv')

D_pba = pd.DataFrame(new_accounts[1])
D_pba = pd.DataFrame(D_pba.loc[:, idx[:, ['Paddy rice', 'Wheat', 'Cereal grains nec', 'Vegetables, fruit, nuts', 'Oil seeds',
                          'Sugar cane, sugar beet', 'Plant-based fibers', 'Crops nec', 'Cattle', 'Pigs', 'Poultry',
                          'Meat animals nec', 'Animal products nec', 'Raw milk',
                          'Fish and other fishing products; services incidental of fishing (05)', 'Food products nec','Beverages', 'Sugar', 'Fish products', 'Dairy products',
                          'Products of meat cattle', 'Products of meat pigs', 'Products of meat poultry', 'Meat products nec', 'products of Vegetable oils and fats', 'Processed rice']]])
D_pba.to_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Autumn Project 2021/Biodiversity Footprint/Dissagregated_BF_D_pba_2010_LCIA_household_Y_categories_agrifood_final_demand_continental_proxy_approach.csv')

D_imp = pd.DataFrame(new_accounts[2])
D_imp = pd.DataFrame(D_imp.loc[:, idx[:, ['Paddy rice', 'Wheat', 'Cereal grains nec', 'Vegetables, fruit, nuts', 'Oil seeds',
                          'Sugar cane, sugar beet', 'Plant-based fibers', 'Crops nec', 'Cattle', 'Pigs', 'Poultry',
                          'Meat animals nec', 'Animal products nec', 'Raw milk',
                          'Fish and other fishing products; services incidental of fishing (05)', 'Food products nec','Beverages', 'Sugar', 'Fish products', 'Dairy products',
                          'Products of meat cattle', 'Products of meat pigs', 'Products of meat poultry', 'Meat products nec', 'products of Vegetable oils and fats', 'Processed rice']]])

D_imp.to_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Autumn Project 2021/Biodiversity Footprint/Dissagregated_BF_D_imp_2010_LCIA_Y_categories_agrifood_final_demand_continental_proxy_approach.csv')

D_exp = pd.DataFrame(new_accounts[3])
D_exp = pd.DataFrame(D_exp.loc[:, idx[:, ['Paddy rice', 'Wheat', 'Cereal grains nec', 'Vegetables, fruit, nuts', 'Oil seeds',
                          'Sugar cane, sugar beet', 'Plant-based fibers', 'Crops nec', 'Cattle', 'Pigs', 'Poultry',
                          'Meat animals nec', 'Animal products nec', 'Raw milk',
                          'Fish and other fishing products; services incidental of fishing (05)', 'Food products nec','Beverages', 'Sugar', 'Fish products', 'Dairy products',
                          'Products of meat cattle', 'Products of meat pigs', 'Products of meat poultry', 'Meat products nec', 'products of Vegetable oils and fats', 'Processed rice']]])

D_exp.to_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Autumn Project 2021/Biodiversity Footprint/Dissagregated_BF_D_exp_2010_LCIA_Y_categories_agrifood_final_demand_continental_proxy_approach.csv')


