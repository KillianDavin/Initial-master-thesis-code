import pymrio
import pandas as pd

iso3_to_full_names_dict = {'AT': 'Austria', 'BE':'Belgium', 'BG':'Bulgaria','CZ':'Czech Republic', 'CY':'Cyprus', 'DE':'Germany', 'DK':'Denmark', 'EE':'Estonia',
                            'ES':'Spain','FR':'France','FI':'Finland','GR':'Greece', 'HU':'Hungary', 'HR':'Croatia', 'IE':'Ireland','IT':'Italy' ,'LT':'Lithuania', 'LV':'Latvia', 'LU': 'Luxembourg',
                           'MT':'Malta', 'NL': 'Netherlands', 'PL': 'Poland', 'PT': 'Portugal', 'SE':'Sweden', 'SK':'Slovakia', 'SI':'Slovenia','RO': 'Romania',
                           'GB': 'Great Britain', 'US':'United States', 'CN':'China', 'CA': 'Canada', 'JP': 'Japan', 'IN': 'India', 'ID': 'Indonesia',
                           'KR': 'South Korea', 'RU': 'Russia', 'NO': 'Norway', 'CH': 'Switzerland', 'TW':'Taiwan','TR':'Turkey','ZA':'South Africa', 'BR': 'Brazil',
                           'MX':'Mexico', 'AU': 'Australia', 'WA': 'RoW_Asia_and_Pacific', 'WF': 'RoW_Africa', 'WL': 'RoW_America', 'WM':'RoW_Middle_East', 'WE':'RoW_Europe'}


idx = pd.IndexSlice  # Slicing of multi index columns for separating out multiindex columns

years = range(2010, 2011)

for n, year in enumerate(years):
    print(n, year)
    exio3_folder = "C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO3"
    #exio_meta = pymrio.download_exiobase3(storage_folder=exio3_folder, system="pxp", years=[year])
    year = str(year)
    #file_path = 'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO3/IOT_'+ year +'_pxp.zip'

#################################################################################################################################################################

    ''' This file is for the calculation of biodiversity footprints using the aggregated, unchanged, LC-IMPACT biodiversity impact characterisation factors as per the
    autumn research project 2021. The land types are broken in 6 major types: Annual crops, permanent crops, pasture, extensive forestry, intensive forestry 

    This example is for the analysis of the extensive forestry land stressor'''


##########################################################################################################################################################################################
    exiobase3 = pymrio.load_all('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/interim/EXIO3')
    #exiobase3.S = pd.read_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/interim/EXIO3/satellite/S.txt'
    exiobase3.satellite.S = pd.DataFrame(exiobase3.satellite.S)
    exiobase3.satellite.S_Y = pd.DataFrame(exiobase3.satellite.S_Y)
    exiobase3.satellite.S.rename(columns = iso3_to_full_names_dict, level = 0, inplace =True)
    exiobase3.satellite.S_Y.rename(columns = iso3_to_full_names_dict, level = 0, inplace =True)


    CF_tables = pd.read_csv('C:/Users/Cillian/OneDrive - NTNU/Documents/NTNU project documents/CF sheets/Land_characterisation_thesis/Full_CF_table_median_approach.csv')
    CF_tables.set_index('Stressor name', inplace = True)
    print(list(CF_tables.index.values))
    CF_tables.rename(index = {'Permanent crops ': 'Permanent crops', 'Pasture ':'Pasture', 'Urban ':'Urban', 'Extensive forestry ': 'Extensive forestry', 'Intensive forestry ': 'Intensive forestry'}, inplace= True)
    CF_tables.rename(columns = iso3_to_full_names_dict, inplace = True)
    CF_tables.iloc[0:6,2:] = CF_tables.iloc[0:6,2:].values * 10 ** 6  # conversion from m2 to km2 for land Characterisations, index 0-6 are the land CFs in the table

    countries_Exiobase3 = list(CF_tables.columns.values)
    countries_Exiobase3.pop(0)
    countries_Exiobase3.pop(0)
##################################################################################################################################################################################################################

    #####################################################################################################################################################################

    '''The next section deals with characterizing the stressor table S, with the CF factors from table 'CF_tables'.
       The S table is broken out into smaller S_impact tables to match the various impact categories for characterization.
       The table is reformed after characterization as Char_table with units PDF per elementary flow.
       This section also calculates the characterized footprint of F_Y, which is the footprint related to household consumption or
       the impacts required for the consumption to take place.Multiplication is done via index location and for loops at different
       levels, according to indexs in the Stressor tables S_, F_Y, and CF_tables. '''

    ############################################################################################################################################################################################

    S = pd.DataFrame(exiobase3.satellite.S)
    S_Y = pd.DataFrame(exiobase3.satellite.S_Y)
    S_land_occupation = pd.DataFrame(S.iloc[0:13, :])  # land stressors
    S_Y_land_occupation = pd.DataFrame(S_Y.iloc[0:13, :])  # land stressors

    S_climate_change = pd.DataFrame(S.iloc[13:32, :])  # climate change stressors
    S_Y_climate_change = pd.DataFrame(S_Y.iloc[13:32, :])  # climate change stressors

    S_water_consumption = pd.DataFrame(S.iloc[32:135, :])  # water stressors
    S_Y_water_consumption = pd.DataFrame(S_Y.iloc[32:135, :])  # water stressors

    S_freshwater_eutrophication = pd.DataFrame(S.iloc[[136,137,138,140], :])
    S_Y_freshwater_eutrophication = pd.DataFrame(S_Y.iloc[[136,137,138,140], :])

    S_marine_eutrophication = pd.DataFrame(S.iloc[[135,139],:])
    S_Y_marine_eutrophication = pd.DataFrame(S_Y.iloc[[135,139],:])

    Land_occupation_index = S_land_occupation.index.tolist()
    Climate_change_index = S_climate_change.index.tolist()
    Water_consumption_index = S_water_consumption.index.tolist()
    Freshwater_eutrophication_index = S_freshwater_eutrophication.index.tolist()
    stressors_index_required = Land_occupation_index + Climate_change_index + Water_consumption_index + Freshwater_eutrophication_index
    Annual_Crops = ['Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice', 'Plant-based fibers', 'Sugar', 'Wheat','Annual crops']

    print(S_land_occupation.loc[Annual_Crops,:])
    Annual_crop_df = pd.DataFrame(S_land_occupation.loc[Annual_Crops,:]).sum(0)
    Annual_crop_df = pd.DataFrame(Annual_crop_df)
    print(Annual_crop_df)
    Annual_crop_df =  pd.DataFrame(Annual_crop_df).T
    Annual_crop_df_S_Y = pd.DataFrame(S_Y_land_occupation.loc[Annual_Crops,:].sum(0))
    Annual_crop_df_S_Y = pd.DataFrame(Annual_crop_df_S_Y).T
    print(Annual_crop_df)
    Permanent_crop_df = pd.DataFrame(S_land_occupation.loc['Vegetables, fruit, nuts', :])
    Permanent_crop_df = pd.DataFrame(Permanent_crop_df).T
    Permanent_crop_df_S_Y = S_Y_land_occupation.loc['Vegetables, fruit, nuts', :]
    Permanent_crop_df_S_Y = pd.DataFrame(Permanent_crop_df_S_Y).T
    print(Permanent_crop_df)

    Pasture_crop_df = S_land_occupation.loc['Pasture', :]
    Pasture_crop_df = pd.DataFrame(Pasture_crop_df).T
    Pasture_crop_df_S_Y = S_Y_land_occupation.loc['Pasture', :]
    Pasture_crop_df_S_Y = pd.DataFrame(Pasture_crop_df_S_Y).T

    Urban_crop_df = S_land_occupation.loc['Urban', :]
    Urban_crop_df = pd.DataFrame(Urban_crop_df).T
    Urban_crop_df_S_Y = S_Y_land_occupation.loc['Urban', :]
    Urban_crop_df_S_Y = pd.DataFrame(Urban_crop_df_S_Y).T

    Extensive_df = S_land_occupation.loc['Extensive forestry', :]
    Extensive_df = pd.DataFrame(Extensive_df).T
    Extensive_df_S_Y = S_Y_land_occupation.loc['Extensive forestry', :]
    Extensive_df_S_Y = pd.DataFrame(Extensive_df_S_Y).T


    Intensive_df = S_land_occupation.loc['Intensive forestry', :]
    Intensive_df = pd.DataFrame(Intensive_df).T
    Intensive_df_S_Y = S_Y_land_occupation.loc['Intensive forestry', :]
    Intensive_df_S_Y = pd.DataFrame(Intensive_df_S_Y).T

    S_land_occupation = pd.DataFrame()
    S_Y_land_occupation = pd.DataFrame()
    for land_category in (Annual_crop_df, Permanent_crop_df, Pasture_crop_df, Urban_crop_df, Extensive_df, Intensive_df):
        S_land_occupation = S_land_occupation.append(land_category)

    for land_category in (Annual_crop_df_S_Y, Permanent_crop_df_S_Y, Pasture_crop_df_S_Y, Urban_crop_df_S_Y, Extensive_df_S_Y, Intensive_df_S_Y):
        S_Y_land_occupation = S_Y_land_occupation.append(land_category)

    S_land_occupation = S_land_occupation.reset_index(drop = True)
    S_Y_land_occupation = S_Y_land_occupation.reset_index(drop = True)
    S_land_occupation.set_axis(['Annual crops', 'Permanent crops', 'Pasture', 'Urban', 'Extensive forestry', 'Intensive forestry'], axis = 'index', inplace= True)
    S_Y_land_occupation.set_axis(['Annual crops', 'Permanent crops', 'Pasture', 'Urban', 'Extensive forestry', 'Intensive forestry'],axis='index', inplace= True)
    print(S_land_occupation)



################################################################################################################################################################################

    '''Do this in the morning'''

###############################################################################################################################################################################

    labels = exiobase3.L.columns.to_list()
    exiobase3.satellite.F_Y = pd.DataFrame(exiobase3.satellite.F_Y.iloc[0:133, :])

    for land_type in ('Annual crops', 'Permanent crops', 'Pasture', 'Urban', 'Extensive forestry', 'Intensive forestry'):  # There are 6 land categories to be characterized
        for country in countries_Exiobase3:
            S_land_occupation.loc[land_type, country] = S_land_occupation.loc[land_type, country] * CF_tables.loc[land_type, country]  # matching EXIOBASE indexing with that of the CF_tables
            S_Y_land_occupation.loc[land_type, country] = S_Y_land_occupation.loc[land_type, country] * CF_tables.loc[land_type, country]  # matching EXIOBASE indexing with that of the CF_tables

            ### Climate Change ###

    for CO2_stressor in ['CO2 - combustion - air', 'CO2 - non combustion - Cement production - air',
                                 'CO2 - non combustion - Lime production - air', 'CO2 - waste - biogenic - air',
                                 'CO2 - waste - fossil - air', 'CO2 - agriculture - peat decay - air']:
        for country in countries_Exiobase3:
            S_climate_change.loc[CO2_stressor, country] = S_climate_change.loc[CO2_stressor, country] * CF_tables.loc['Carbon dioxide (fossil) - core', country]
            S_Y_climate_change.loc[CO2_stressor, country] = S_Y_climate_change.loc[CO2_stressor, country] * CF_tables.loc['Carbon dioxide (fossil) - core', country]

    Get_index_S = list(exiobase3.satellite.S.iloc[16:24, :].index.values)
    CH4_stressor_list = ['CH4 - waste - air', 'CH4 - agriculture - air']
    CH4_stressor_list.extend(Get_index_S)
    print(CH4_stressor_list)
    for Fossil_CH4_stressor in ['CH4 - combustion - air']:
        for country in countries_Exiobase3:
            S_climate_change.loc[Fossil_CH4_stressor, country] = S_climate_change.loc[Fossil_CH4_stressor, country] * CF_tables.loc['Fossil methane - core', country]
            S_Y_climate_change.loc[Fossil_CH4_stressor, country] = S_Y_climate_change.loc[Fossil_CH4_stressor, country] * CF_tables.loc['Fossil methane - core', country]

    for CH4_stressor in (CH4_stressor_list)  :
        for country in countries_Exiobase3:
            S_climate_change.loc[CH4_stressor, country] = S_climate_change.loc[CH4_stressor, country] * CF_tables.loc['Methane - core', country]
            S_Y_climate_change.loc[CH4_stressor, country] = S_Y_climate_change.loc[CH4_stressor, country] * CF_tables.loc['Methane - core', country]

    for N2O_stressor in ['N2O - combustion - air', 'N2O - agriculture - air']:
        for country in countries_Exiobase3:
            S_climate_change.loc[N2O_stressor, country] = S_climate_change.loc[N2O_stressor, country] * CF_tables.loc['Nitrous oxide - core', country]
            S_Y_climate_change.loc[N2O_stressor, country] = S_Y_climate_change.loc[N2O_stressor, country] * CF_tables.loc['Nitrous oxide - core', country]


    index = list(S_water_consumption.index.values)
    for water_consumption in index:
        for country in countries_Exiobase3:
            S_water_consumption.loc[water_consumption,country] = S_water_consumption.loc[water_consumption,country] * CF_tables.loc['Water consumption - core ', country]
            S_Y_water_consumption.loc[water_consumption,country] = S_Y_water_consumption.loc[water_consumption,country] * CF_tables.loc['Water consumption - core ', country]

    for eutrophication_pollution in ['P - agriculture - water', 'P - waste - water']:
        for country in countries_Exiobase3:
            S_freshwater_eutrophication.loc[eutrophication_pollution,country] = S_freshwater_eutrophication.loc[eutrophication_pollution,country] * CF_tables.loc['P emission to water ', country]
            S_Y_freshwater_eutrophication.loc[eutrophication_pollution,country] = S_Y_freshwater_eutrophication.loc[eutrophication_pollution,country] * CF_tables.loc['P emission to water ', country]

    for eutrophication_pollution in ['P - agriculture - soil', 'Pxx - agriculture - soil']:
        for country in countries_Exiobase3:
            S_freshwater_eutrophication.loc[eutrophication_pollution, country] = S_freshwater_eutrophication.loc[eutrophication_pollution,country] * CF_tables.loc['P emission to soil ', country]
            S_Y_freshwater_eutrophication.loc[eutrophication_pollution, country] = S_Y_freshwater_eutrophication.loc[eutrophication_pollution,country] * CF_tables.loc['P emission to soil ', country]

    for eutrophication_pollution in ['N - agriculture - water', 'N - waste - water']:
        for country in countries_Exiobase3:
            S_marine_eutrophication.loc[eutrophication_pollution, country] = S_marine_eutrophication.loc[eutrophication_pollution,country] * CF_tables.loc['N emissions to freshwater', country]
            S_Y_marine_eutrophication.loc[eutrophication_pollution, country] = S_Y_marine_eutrophication.loc[eutrophication_pollution,country] * CF_tables.loc['N emissions to freshwater', country]



    Char_table_S = pd.DataFrame(S_land_occupation)  # New characterized S tables
    Char_table_S_Y = pd.DataFrame(S_Y_land_occupation)
    Stressor_tables = [S_climate_change, S_water_consumption, S_freshwater_eutrophication, S_marine_eutrophication]
    S_Y_stressor_tables = [S_Y_climate_change, S_Y_water_consumption, S_Y_freshwater_eutrophication, S_Y_marine_eutrophication]

    for stressor in Stressor_tables:
        Char_table_S = Char_table_S.append(stressor)  # Fully formed - New characterized S tables

    for stressor in S_Y_stressor_tables:
        Char_table_S_Y = Char_table_S_Y.append(stressor)

    exiobase3.satellite.S = pd.DataFrame(Char_table_S)
    exiobase3.satellite.S_Y = pd.DataFrame(Char_table_S_Y)


    ######################################################################################################################################################################################################################################

    ''' This section deals with the quantification of the Biodiversity footprints
    following the characterization of the stressors above'''

    #############################################################################################################################################################################################################################

    exiobase3.rename_regions(
        {'AT': 'Austria', 'BE': 'Belgium', 'BG': 'Bulgaria', 'CZ': 'Czech Republic', 'CY': 'Cyprus', 'DE': 'Germany',
         'DK': 'Denmark', 'EE': 'Estonia',
         'ES': 'Spain', 'FR': 'France', 'FI': 'Finland', 'GR': 'Greece', 'HU': 'Hungary', 'HR': 'Croatia',
         'IE': 'Ireland', 'IT': 'Italy', 'LT': 'Lithuania', 'LV': 'Latvia', 'LU': 'Luxembourg',
         'MT': 'Malta', 'NL': 'Netherlands', 'PL': 'Poland', 'PT': 'Portugal', 'SE': 'Sweden', 'SK': 'Slovakia',
         'SI': 'Slovenia', 'RO': 'Romania',
         'GB': 'Great Britain', 'US': 'United States', 'CN': 'China', 'CA': 'Canada', 'JP': 'Japan', 'IN': 'India',
         'ID': 'Indonesia',
         'KR': 'South Korea', 'RU': 'Russia', 'NO': 'Norway', 'CH': 'Switzerland', 'TW': 'Taiwan', 'TR': 'Turkey',
         'ZA': 'South Africa', 'BR': 'Brazil',
         'MX': 'Mexico', 'AU': 'Australia', 'WA': 'RoW_Asia_and_Pacific', 'WF': 'RoW_Africa', 'WL': 'RoW_America',
         'WM': 'RoW_Middle_East', 'WE': 'RoW_Europe'})

    new_accounts = pymrio.calc_accounts(exiobase3.satellite.S, exiobase3.L, exiobase3.Y)  # Note here, we input Char_table_S rather than S for the calculation of the Biodiversity accounts

    D_cba_biod = pd.DataFrame(new_accounts[0])
    print(D_cba_biod.shape)
    D_cba_biod = pd.DataFrame(D_cba_biod)

    D_cba_biod = pd.DataFrame(
        D_cba_biod.loc[:, idx[:, ['Paddy rice', 'Wheat', 'Cereal grains nec', 'Vegetables, fruit, nuts', 'Oil seeds',
                          'Sugar cane, sugar beet', 'Plant-based fibers', 'Crops nec', 'Cattle', 'Pigs', 'Poultry',
                          'Meat animals nec', 'Animal products nec', 'Raw milk', 'Wool, silk-worm cocoons',
                          'Products of forestry, logging and related services (02)',
                          'Fish and other fishing products; services incidental of fishing (05)', 'Food products nec','Beverages', 'Sugar', 'Fish products', 'Dairy products',
                          'Products of meat cattle', 'Products of meat pigs', 'Products of meat poultry', 'Meat products nec', 'products of Vegetable oils and fats', 'Processed rice']]])  # Seggregating final consumer household demand
    myfile = 'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Biodiversity Footprint/EXIO3/BF_D_cba_' + year + '_LCIA_aggregated_Y_household.csv'
    D_cba_biod.to_csv(myfile)

    D_pba_biod = pd.DataFrame(new_accounts[1])
    print(D_pba_biod.shape)
    D_pba_biod = pd.DataFrame(D_pba_biod)

    D_pba_biod = pd.DataFrame(
        D_pba_biod.loc[:, idx[:, ['Paddy rice', 'Wheat', 'Cereal grains nec', 'Vegetables, fruit, nuts', 'Oil seeds',
                          'Sugar cane, sugar beet', 'Plant-based fibers', 'Crops nec', 'Cattle', 'Pigs', 'Poultry',
                          'Meat animals nec', 'Animal products nec', 'Raw milk', 'Wool, silk-worm cocoons',
                          'Products of forestry, logging and related services (02)',
                          'Fish and other fishing products; services incidental of fishing (05)', 'Food products nec','Beverages', 'Sugar', 'Fish products', 'Dairy products',
                          'Products of meat cattle', 'Products of meat pigs', 'Products of meat poultry', 'Meat products nec', 'products of Vegetable oils and fats', 'Processed rice']]])  # Seggregating final consumer household demand
    myfile = 'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Biodiversity Footprint/EXIO3/BF_D_pba_' + year + '_LCIA_aggregated_Y_household.csv'
    D_pba_biod.to_csv(myfile)




    D_imp_biod = pd.DataFrame(new_accounts[2])
    D_imp_biod = pd.DataFrame(
        D_imp_biod.loc[:, idx[:, ['Paddy rice', 'Wheat', 'Cereal grains nec', 'Vegetables, fruit, nuts', 'Oil seeds',
                          'Sugar cane, sugar beet', 'Plant-based fibers', 'Crops nec', 'Cattle', 'Pigs', 'Poultry',
                          'Meat animals nec', 'Animal products nec', 'Raw milk', 'Wool, silk-worm cocoons',
                          'Products of forestry, logging and related services (02)',
                          'Fish and other fishing products; services incidental of fishing (05)', 'Food products nec','Beverages', 'Sugar', 'Fish products', 'Dairy products',
                          'Products of meat cattle', 'Products of meat pigs', 'Products of meat poultry', 'Meat products nec', 'products of Vegetable oils and fats', 'Processed rice']]])  # Seggregating final consumer household demand
    myfile = 'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Biodiversity Footprint/EXIO3/BF_D_imp_' + year + '_LCIA_aggregated_Y_household.csv'
    D_imp_biod.to_csv(myfile)
    D_exp_biod = pd.DataFrame(new_accounts[3])
    D_exp_biod = pd.DataFrame(D_exp_biod)

    D_exp_biod = pd.DataFrame(
        D_exp_biod.loc[:, idx[:, ['Paddy rice', 'Wheat', 'Cereal grains nec', 'Vegetables, fruit, nuts', 'Oil seeds',
                          'Sugar cane, sugar beet', 'Plant-based fibers', 'Crops nec', 'Cattle', 'Pigs', 'Poultry',
                          'Meat animals nec', 'Animal products nec', 'Raw milk', 'Wool, silk-worm cocoons',
                          'Products of forestry, logging and related services (02)',
                          'Fish and other fishing products; services incidental of fishing (05)', 'Food products nec','Beverages', 'Sugar', 'Fish products', 'Dairy products',
                          'Products of meat cattle', 'Products of meat pigs', 'Products of meat poultry', 'Meat products nec', 'products of Vegetable oils and fats', 'Processed rice']]])  # Seggregating final consumer household demand
    myfile = 'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Biodiversity Footprint/EXIO3/BF_D_exp_' + year + '_LCIA_aggregated_Y_household.csv'
    D_exp_biod.to_csv(myfile)




    #import os
   #myfile = 'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO3/IOT_'+ year +'_pxp.zip'

    ## If file exists, delete it ##
    #if os.path.isfile('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO3/IOT_'+ year +'_pxp.zip'):
        #os.remove('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO3/IOT_'+ year +'_pxp.zip')
    #else:  ## Show an error ##
        #print("Error: file not found")
    # del exiobase3


