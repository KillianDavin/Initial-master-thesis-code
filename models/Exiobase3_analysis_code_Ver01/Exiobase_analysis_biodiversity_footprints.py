import pymrio
import pandas as pd
years = range(1995, 2016)
TS_D_cba_biod = pd.DataFrame()
TS_D_pba_biod = pd.DataFrame()
TS_D_imp_biod = pd.DataFrame()
TS_D_exp_biod = pd.DataFrame()
type_of_analysis =input("What type of model run is this?:  ('Normal_LC_IMPACT': 'Disaggregated_LC_IMPACT')" )
#################################################################################################################################################################

''' This file is for the calculation of source tables when analysing the origins of stressor impacts.
Individual stressors must be diagonalized to form square 9800 x 9800 S tables, and footprints are recalculated individually
in terms of the stressor being analysed. This file gives an example of the operations completed for the diagonolisation of
one stressor and the calculation of the footprints thereafter. This file must be executed 6 times for example, if looking
to find the total source impacts due to land use (6 impact categories that need to be diagonalized individually).
Each stressor footprint is calculated individual and added together at the end to form 9800 x 9800 Footprint tables in terms
of land use etc....

This example is for the analysis of the extensive forestry land stressor'''


##########################################################################################################################################################################################
iso3_to_full_names_dict = {'AT': 'Austria', 'BE':'Belgium', 'BG':'Bulgaria','CZ':'Czech Republic', 'CY':'Cyprus', 'DE':'Germany', 'DK':'Denmark', 'EE':'Estonia',
                            'ES':'Spain','FR':'France','FI':'Finland', 'HR':'Hungary', 'IE':'Ireland','IT':'Italy' ,'LT':'Lithuania', 'LV':'Latvia', 'LU': 'Luxembourg',
                           'MT':'Malta', 'NL': 'Netherlands', 'PL': 'Poland', 'PT': 'Portugal', 'SE':'Sweden', 'SK':'Slovakia', 'SL':'Slovenia','RO': 'Romania',
                           'GB': 'Great Britain', 'US':'United States', 'CN':'China', 'CA': 'Canada', 'JP': 'Japan', 'IN': 'India', 'ID': 'Indonesia',
                           'KR': 'South Korea', 'RU': 'Russia', 'NO': 'Norway', 'CH': 'Switzerland', 'TW':'Taiwan','TR':'Turkey','ZA':'South Africa', 'BR': 'Brazil',
                           'MX':'Mexico', 'AU': 'Australia', 'WA': 'RoW_Asia_and_Pacific', 'WF': 'RoW_Africa', 'WL': 'RoW_America', 'WM':'RoW_Middle_East', 'WE':'RoW_Europe'}




##########################################################################################################################################################

''' Loading in the LC-Impact characterisation factors and the tailored & opitimised Land and water characterisation factors calculated in previous steps 
Land_CF_tables represent the disaggegrated PDFs for the various crop/land use types, Water_CF_tables represent the water impacts for the disaggregated crop types, 
 while LC '''


##########################################################################################################################################################

Land_CF_tables = pd.read_csv('C:/Users/Cillian/OneDrive - NTNU/Documents/NTNU project documents/ArcGIS_shapefiles_MT2022/GIS_layers_output/Final_sheets_for_Exiobase/land_characterization_factors_with_ROW_regions_ver02.csv')
Land_CF_tables.set_index('Land Type', inplace = True)
#Land_Land_CF_tables = Land_Land_CF_tables.values.astype(float)



Land_CF_tables = Land_CF_tables* (
        10 ** 6)  # conversion from m2 to km2 for land Characterisations, index 0-6 are the land CFs in the table

print(Land_CF_tables)

LC_Impact_CF_tables = pd.read_csv('C:/Users/Cillian/OneDrive - NTNU/Documents/NTNU project documents/CF sheets/Land_characterisation_thesis/Full_CF_table_median_approach.csv')
LC_Impact_CF_tables.set_index('Stressor name', inplace = True)
LC_Impact_CF_tables.rename(columns = iso3_to_full_names_dict, inplace = True)

Water_CF_tables = pd.read_csv('C:/Users/Cillian/OneDrive - NTNU/Documents/NTNU project documents/ArcGIS_shapefiles_MT2022/GIS_layers_output/Final_sheets_for_Exiobase/Watershed_aggregated_national_and_ROW_level_characterisation_factors_ver01.csv')
Water_CF_tables.set_index('Crop Type', inplace = True)

###########################################################################################################################################################################################

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
##################################################################################################################################################################################################################

    '''Segregating the household consumption category from the Y tables'''

##################################################################################################################################################################################################################
    idx = pd.IndexSlice  # Slicing of multi index columns for separating out multiindex columns
    Y = pd.DataFrame(
        Y.loc[:, idx[:, 'Final consumption expenditure by households']])  # Seggregating final consumer household demand
    print(Y)
    exiobase3.Y = pd.DataFrame(Y)  # New Y tables in terms of 'Final consumption by households only'

##################################################################################################################################################################################################################

    '''Segregating required stressors from S tables. Segregation is completed via index referencing of original tables.
       Details on stressors and S table row index, see Appendix F in project literature'''

##################################################################################################################################################################################################################
    if type_of_analysis == 'Normal_LC_IMPACT':

        land_stressors = pd.DataFrame(
            S.iloc[[446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 461, 462, 463, 464, 465],
            :])  # Seperation of land use categories using indexing. Rows obtained from csv file
        water_stressors = pd.DataFrame(S.iloc[923:1026])  # Blue water consumption stressor rows
        climate_change_stressors = pd.DataFrame(S.iloc[
                                                [23, 24, 25, 67, 68, 69, 70, 71, 72, 73, 74, 92, 93, 426, 427, 429, 435,
                                                 437, 438]])  # Climate change stressor rows
        eutrophication_stressors = pd.DataFrame(S.iloc[[432, 433, 434, 440, 443]])  # Marine and Fresh eutrophication

        # Aggregation of exiobase land use categories to LC-IMPACT categories

        Annual_crop_df = pd.DataFrame(land_stressors.iloc[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12], :]).sum(
            0)  # Aggregation of the annual crop categories in exiobase to the singular LC-IMPACT category for Land Use
        print(Annual_crop_df)
        Annual_crop_df = pd.DataFrame(
            Annual_crop_df).T  # As python outputs a column vector for a summation operation, the transpose function T is used to return the annual crop dataframe to it's original Dataframe index/column set up with countries and products as the column index and stressor as the row index.
        Permanent_crop_df = pd.DataFrame(land_stressors.iloc[[11], :]).sum(
            0)  # Aggregation of permanent crop categories to LC-Impact land category
        Permanent_crop_df = pd.DataFrame(Permanent_crop_df).T  # Transposing to original Dataframe layout.
        Pasture_crop_df = pd.DataFrame(land_stressors.iloc[[14, 15, 16], :]).sum(
            0)  # Aggregation of Pasture crop land use categories
        print(Annual_crop_df)
        Pasture_crop_df = pd.DataFrame(Pasture_crop_df).T
        Urban_df = pd.DataFrame(land_stressors.iloc[[17], :]).sum(0)  # Aggregation of Urban land use categories
        Urban_df = pd.DataFrame(Urban_df).T
        Intensive_forestry_df = pd.DataFrame(land_stressors.iloc[[13], :]).sum(
            0)  # Aggregation of Intensive forestry land use stresors to LC-Impact category
        Intensive_forestry_df = pd.DataFrame(Intensive_forestry_df).T
        Extensive_forestry_df = pd.DataFrame(land_stressors.iloc[[18], :]).sum(
            0)  # Aggregation of Intensive forestry land use stresors to LC-Impact
        Extensive_forestry_df = pd.DataFrame(Extensive_forestry_df).T

        # Re-creating a combined dataframe for the aggregated land use stressors

        Land_aggregated_df = Annual_crop_df
        landuse_list = (Permanent_crop_df, Pasture_crop_df, Urban_df, Extensive_forestry_df, Intensive_forestry_df)
        new_land_categories_index = (
        'Annual crops', 'Permanent Crops', 'Pasture', 'Urban', 'Extensive forestry', 'Intensive forestry')
        for i in landuse_list:
            Land_aggregated_df = Land_aggregated_df.append(
                i)  # Appending Land_aggregated_df with each of the aggregated land use categories

        Land_aggregated_df.reset_index()
        Land_aggregated_df.set_axis(new_land_categories_index, inplace=True)  # Updating the index row labels

        # Combining the aggregated land use stressor categories with the disaggregated land use stressors, and the stressors for the other impact categories being analysed. This is the final compiled stressor matrix.
        # Not necessary to add land stressors, but nice to have for future reference if required.

        stressor_list = (climate_change_stressors, water_stressors, eutrophication_stressors, land_stressors)
        exiobase3.satellite.S = Land_aggregated_df  # Full_stressor_list = All required stressors (aggregated and disaggregated) for footprint calculations
        for i in stressor_list:
            exiobase3.satellite.S = exiobase3.satellite.S.append(i)

        S = pd.DataFrame(exiobase3.satellite.S)
        S.to_csv('S_check.csv')

        ##################################################################################################################################################################################################################

        '''Segregating required stressors from S_Y tables in exactly the same fashion as what was completed above for the S tables'''

        ##################################################################################################################################################################################################################

        S_Y = pd.DataFrame(exiobase3.satellite.S_Y)
        land_stressors_S_Y = pd.DataFrame(
            S_Y.iloc[[446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 461, 462, 463, 464, 465],
            :])  # Seperation of land use categories using indexing. Rows obtained from csv file
        water_stressors_S_Y = pd.DataFrame(S_Y.iloc[923:1026])  # Blue water consumption stressor rows
        climate_change_stressors_S_Y = pd.DataFrame(S_Y.iloc[
                                                        [23, 24, 25, 67, 68, 69, 70, 71, 72, 73, 74, 92, 93, 426, 427, 429,
                                                         435, 437, 438]])  # Global warming stressor rows
        eutrophication_stressors_S_Y = pd.DataFrame(S_Y.iloc[[432, 433, 434, 440, 443]])  # Marine and Fresh eutrophication

        # Combining the aggregated land use stressor categories with the disaggregated land use stressors, and the stressors for the other impact categories being analysed. This is the final compiled stressor matrix.

        # Aggregation of exiobase land use categories to LC-IMPACT categories_S_Y

        Annual_crop_df_S_Y = pd.DataFrame(land_stressors_S_Y.iloc[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12], :]).sum(
            0)  # Aggregation of the annual crop categories in exiobase to the singular LC-IMPACT category for Land Use
        Annual_crop_df_S_Y = pd.DataFrame(
            Annual_crop_df_S_Y).T  # As python outputs a column vector for a sumation operation, the transpose function T is used to return the annual crop dataframe to it's original Dataframe index/column set up with countries and products as the column index and stressor as the row index.
        Permanent_crop_df_S_Y = pd.DataFrame(land_stressors_S_Y.iloc[[11], :]).sum(
            0)  # Aggregation of permanent crop categories to LC-Impact land category
        Permanent_crop_df_S_Y = pd.DataFrame(Permanent_crop_df_S_Y).T  # Transposing to original Dataframe layout.
        Pasture_crop_df_S_Y = pd.DataFrame(land_stressors_S_Y.iloc[[14, 15, 16], :]).sum(
            0)  # Aggregation of Pasture crop land use categories
        Pasture_crop_df_S_Y = pd.DataFrame(Pasture_crop_df_S_Y).T
        Urban_df_S_Y = pd.DataFrame(land_stressors_S_Y.iloc[[17], :]).sum(0)  # Aggregation of Urban land use categories
        Urban_df_S_Y = pd.DataFrame(Urban_df_S_Y).T
        Intensive_forestry_df_S_Y = pd.DataFrame(land_stressors_S_Y.iloc[[13], :]).sum(
            0)  # Aggregation of Intensive forestry land use stresors to LC-Impact category
        Intensive_forestry_df_S_Y = pd.DataFrame(Intensive_forestry_df_S_Y).T
        Extensive_forestry_df_S_Y = pd.DataFrame(land_stressors_S_Y.iloc[[18], :]).sum(
            0)  # Aggregation of Intensive forestry land use stresors to LC-Impact
        Extensive_forestry_df_S_Y = pd.DataFrame(Extensive_forestry_df_S_Y).T

        # Re-creating a combined dataframe for the aggregated land use stressors_F_Y

        Land_aggregated_df_S_Y = Annual_crop_df_S_Y
        landuse_list = (
        Permanent_crop_df_S_Y, Pasture_crop_df_S_Y, Urban_df_S_Y, Extensive_forestry_df_S_Y, Intensive_forestry_df_S_Y)
        new_land_categories_index = (
        'Annual crops', 'Permanent Crops', 'Pasture', 'Urban', 'Extensive forestry', 'Intensive forestry')
        for i in landuse_list:
            Land_aggregated_df_S_Y = Land_aggregated_df_S_Y.append(
                i)  # Appending Land_aggregated_df with each of the aggregated land use categories

        Land_aggregated_df_S_Y.reset_index()
        Land_aggregated_df_S_Y.set_axis(new_land_categories_index, inplace=True)  # Updating the index row labels

        # Combining the aggregated land use stressor categories with the disaggregated land use stressors, and the stressors for the other impact categories being analysed. This is the final compiled stressor matrix for F_Y.

        stressor_list_S_Y = (
        climate_change_stressors_S_Y, water_stressors_S_Y, eutrophication_stressors_S_Y, land_stressors_S_Y)
        exiobase3.satellite.S_Y = Land_aggregated_df_S_Y  # Full_stressor_list = All required stressors (aggregated and disaggregated) for footprint calculations
        for i in stressor_list_S_Y:
            exiobase3.satellite.S_Y = exiobase3.satellite.S_Y.append(i)

        exiobase3.satellite.S_Y = pd.DataFrame(exiobase3.satellite.S_Y.loc[:, idx[:,
                                                                              'Final consumption expenditure by households']])  # Seggregating final consumer househould expenditure

        S_Y = pd.DataFrame(exiobase3.satellite.S_Y)


        ##################################################################################################################################################################################################################

        '''With a new Y table, S table and S_Y table, all other tables are reset to the co-efficients
            for the recalculation of new x,F,Z,M tables. Resetting of coefficients with pymrio resets all tables in EXIOBASE other than the
            A and L matrices'''

        ##################################################################################################################################################################################################################
        exiobase3.reset_all_to_coefficients()
        print(exiobase3.A)  # 9800x9800
        exiobase3.L = pymrio.calc_L(exiobase3.A)
        print(exiobase3.L)  # 9800x9800

        print(exiobase3.x)  # 0
        print(exiobase3.satellite.F)  # 0
        print(exiobase3.Z)  # 0
        print(exiobase3.satellite.M)  # 0
        exiobase3.Y = pd.DataFrame(Y)  # Setting Y tables to Y tables formed in the first section of the code
        exiobase3.satellite.S = pd.DataFrame(S)  # Setting S tables to S tables formed in the second section of the code
        exiobase3.satellite.S_Y = pd.DataFrame(S_Y)  # Setting S_Y tables to S_Y tables formed in third section of the code
        Y = exiobase3.Y
        exiobase3.x = pymrio.calc_x_from_L(exiobase3.L, exiobase3.Y.sum(1))  # Using PYMRIO functionality to calculate x from L and Y tables
        exiobase3.Z = pymrio.calc_Z(exiobase3.A,
                                    exiobase3.x)  # Using PYMRIO functionality to calculate Z from A and x tables

        exiobase3.satellite.F_Y = pd.DataFrame(pymrio.calc_F_Y(exiobase3.satellite.S_Y, exiobase3.Y.sum(0)))
        print(exiobase3.satellite.F_Y.shape)
        exiobase3.satellite.F = pd.DataFrame(pymrio.calc_F(exiobase3.satellite.S, exiobase3.x))
        print(exiobase3.satellite.S)
        print(exiobase3.satellite.F)
        print(exiobase3.satellite.F_Y)
        print(exiobase3.satellite.F.shape)
        exiobase3.M = pd.DataFrame(pymrio.calc_M(exiobase3.satellite.S, exiobase3.L))
        ##################################################################################################################################################################################################################

        #####################################################################################################################################################################

        '''The next section deals with characterizing the stressor table S, with the CF factors from table 'Land_CF_tables'.
           The S table is broken out into smaller S_impact tables to match the various impact categories for characterization.
           The table is reformed after characterization as Char_table with units PDF per elementary flow.
           This section also calculates the characterized footprint of F_Y, which is the footprint related to household consumption or
           the impacts required for the consumption to take place.Multiplication is done via index location and for loops at different
           levels, according to indexs in the Stressor tables S_, F_Y, and Land_CF_tables. '''

        ############################################################################################################################################################################################

        S = pd.DataFrame(exiobase3.satellite.S)
        S_land_occupation = pd.DataFrame(S.iloc[0:6, :])  # land stressors
        S_climate_change = pd.DataFrame(S.iloc[6:25, :])  # climate change stressors
        S_water_consumption = pd.DataFrame(S.iloc[25:128, :])  # water stressors
        S_freshwater_eutrophication = pd.DataFrame(S.iloc[128:131, :])
        S_freshwater_eutrophication = S_freshwater_eutrophication.append(
            S.iloc[132, :])  # freshwater eutrophication stressors
        S_marine_eutrophication = pd.DataFrame(S.iloc[131, :]).T  # Marine eutrophication stressors
        Land_occupation_index = S_land_occupation.index.tolist()
        Climate_change_index = S_climate_change.index.tolist()
        Water_consumption_index = S_water_consumption.index.tolist()
        Freshwater_eutrophication_index = S_freshwater_eutrophication.index.tolist()
        stressors_index_required = Land_occupation_index + Climate_change_index + Water_consumption_index + Freshwater_eutrophication_index
        print(S_marine_eutrophication)
        print(S_marine_eutrophication.shape)

        regions = exiobase3.get_regions()
        labels = exiobase3.L.columns.to_list()
        exiobase3.satellite.F_Y = pd.DataFrame(exiobase3.satellite.F_Y.iloc[0:133, :])

        for stressor_index in range(0, 6):  # There are 6 land categories to be characterized
            lower_range = 0
            upper_range = 200
            for CF_table_column_index in range(0, 49):  # 49 CF factors per impact pathway in Land_CF_tables
                if upper_range <= 9800:
                    for col in range(lower_range, upper_range):
                        S_land_occupation.iat[stressor_index, col] = S_land_occupation.iat[stressor_index, col] * \
                                                                     Land_CF_tables.iat[
                                                                         stressor_index, CF_table_column_index]  # matching EXIOBASE indexing with that of the Land_CF_tables

                    lower_range += 200
                    upper_range += 200

        lower_range = 0
        upper_range = 200
        for CF_table_column_index in range(0, 49):

            if upper_range <= 9800:
                for col in range(lower_range, upper_range):
                    S_climate_change.iat[0, col] = S_climate_change.iat[0, col] * Land_CF_tables.iat[6, CF_table_column_index] + \
                                                   S_climate_change.iat[0, col] * Land_CF_tables.iat[
                                                       14, CF_table_column_index]  # Core Characterisation of CO2 combustion stressors for terrestrial and aquatic climate change PDF
                    S_climate_change.iat[1, col] = S_climate_change.iat[1, col] * Land_CF_tables.iat[7, CF_table_column_index] + \
                                                   S_climate_change.iat[1, col] * Land_CF_tables.iat[
                                                       15, CF_table_column_index]  # Core Characterisation of CH4 combustion stressors for terrestrial and aquatic climate change PDF
                    S_climate_change.iat[2, col] = S_climate_change.iat[2, col] * Land_CF_tables.iat[9, CF_table_column_index] + \
                                                   S_climate_change.iat[2, col] * Land_CF_tables.iat[
                                                       17, CF_table_column_index]  # Core Characterisation of N20 combustion stressors for terrestrial and aquatic climate change PDF
                    S_climate_change.iat[13, col] = S_climate_change.iat[13, col] * Land_CF_tables.iat[
                        7, CF_table_column_index] + S_climate_change.iat[13, col] * Land_CF_tables.iat[
                                                        15, CF_table_column_index]  # Core characterisation of methane release from agriculture for terrestrial and aquatic climate change PDF
                    S_climate_change.iat[14, col] = S_climate_change.iat[14, col] * Land_CF_tables.iat[
                        6, CF_table_column_index] + S_climate_change.iat[14, col] * Land_CF_tables.iat[
                                                        14, CF_table_column_index]  # Core characterisation of CO2 release from peat decay in agriculture for terrestrial and aquatic climate change PDF
                    S_climate_change.iat[15, col] = S_climate_change.iat[15, col] * Land_CF_tables.iat[
                        9, CF_table_column_index] + S_climate_change.iat[15, col] * Land_CF_tables.iat[
                                                        17, CF_table_column_index]  # Core characterisation of N20 release from agriculture for terrestrial and aquatic climate change PDF
                    S_climate_change.iat[16, col] = S_climate_change.iat[16, col] * Land_CF_tables.iat[
                        7, CF_table_column_index] + S_climate_change.iat[16, col] * Land_CF_tables.iat[
                                                        16, CF_table_column_index]  # Core characterisation of methane release from waste for terrestrial and aquatic climate change PDF
                lower_range += 200
                upper_range += 200

        for stressor_index in range(3, 11):
            lower_range = 0
            upper_range = 200
            for CF_table_column_index in range(0, 49):
                if upper_range <= 9800:
                    for col in range(lower_range, upper_range):
                        S_climate_change.iat[stressor_index, col] = S_climate_change.iat[stressor_index, col] * \
                                                                    Land_CF_tables.iat[8, CF_table_column_index] + \
                                                                    S_climate_change.iat[stressor_index, col] * \
                                                                    Land_CF_tables.iat[
                                                                        16, CF_table_column_index]  # Core characterisation of fossil Methane non combustion stressors for terrestrial and aquatic climate change PDF
                lower_range += 200
                upper_range += 200

        for stressor_index in range(11, 13):
            lower_range = 0
            upper_range = 200
            for CF_table_column_index in range(0, 49):
                if upper_range <= 9800:
                    for col in range(lower_range, upper_range):
                        S_climate_change.iat[stressor_index, col] = S_climate_change.iat[stressor_index, col] * \
                                                                    Land_CF_tables.iat[6, CF_table_column_index] + \
                                                                    S_climate_change.iat[stressor_index, col] * \
                                                                    Land_CF_tables.iat[
                                                                        14, CF_table_column_index]  # Core characterisation of non combustive CO2 release from cement/lime production for terrestrial and aquatic climate change PDF
                lower_range += 200
                upper_range += 200

        for stressor_index in range(17, 19):
            lower_range = 0
            upper_range = 200
            for CF_table_column_index in range(0, 49):
                if upper_range <= 9800:
                    for col in range(lower_range, upper_range):
                        S_climate_change.iat[stressor_index, col] = S_climate_change.iat[stressor_index, col] * \
                                                                    Land_CF_tables.iat[6, CF_table_column_index] + \
                                                                    S_climate_change.iat[stressor_index, col] * \
                                                                    Land_CF_tables.iat[
                                                                        14, CF_table_column_index]  # Core characterisations of CO2 for fossil and biogenic waste for terrestrial and aquatic climate change PDF

                lower_range += 200
                upper_range += 200

        for stressor_index in range(0,
                                    103):  # 103 water stressors, to be characterized by the same core LC-IMPACT factors per country
            lower_range = 0
            upper_range = 200
            for CF_table_column_index in range(0, 49):
                if upper_range <= 9800:
                    for col in range(lower_range, upper_range):
                        S_water_consumption.iat[stressor_index, col] = S_water_consumption.iat[stressor_index, col] * \
                                                                       Land_CF_tables.iat[
                                                                           22, CF_table_column_index]  # Core characterisation of water consumption stressors. There are 103 water stressors, hence the range in the for loop
                lower_range += 200
                upper_range += 200

        lower_range = 0
        upper_range = 200
        for CF_table_column_index in range(0, 49):
            if upper_range <= 9800:
                for col in range(lower_range, upper_range):
                    S_freshwater_eutrophication.iat[0, col] = S_freshwater_eutrophication.iat[0, col] * Land_CF_tables.iat[
                        28, CF_table_column_index]  # Characterisation of agricultural phosphorus emissions to soil stressors for freshwater eutrophication impact category
                    S_freshwater_eutrophication.iat[2, col] = S_freshwater_eutrophication.iat[2, col] * Land_CF_tables.iat[
                        28, CF_table_column_index]  # Characterisation of agricultural phosphorus emissions to soil stressors for freshwater eutrophication impact category
                    S_freshwater_eutrophication.iat[1, col] = S_freshwater_eutrophication.iat[1, col] * Land_CF_tables.iat[
                        27, CF_table_column_index]  # Characterisation of agricultural phosphorus emissions to water stressors for freshwater eutrophication impact category
                    S_freshwater_eutrophication.iat[3, col] = S_freshwater_eutrophication.iat[3, col] * Land_CF_tables.iat[
                        27, CF_table_column_index]  # Characterisation of agricultural phosphorus emissions to water stressors for freshwater eutrophication impact category
            lower_range += 200
            upper_range += 200

        lower_range = 0
        upper_range = 200
        for CF_table_column_index in range(0, 49):
            if upper_range <= 9800:
                for col in range(lower_range, upper_range):
                    S_marine_eutrophication.iat[0, col] = S_marine_eutrophication.iat[0, col] * Land_CF_tables.iat[
                        25, CF_table_column_index]
            lower_range += 200
            upper_range += 200

        Char_table_S = pd.DataFrame(S_land_occupation)  # New characterized S tables
        Stressor_tables = [S_climate_change, S_water_consumption, S_freshwater_eutrophication, S_marine_eutrophication]

        for stressor in Stressor_tables:
            Char_table_S = Char_table_S.append(stressor)  # Fully formed - New characterized S tables
        Char_table_S.to_csv('Char_table_S.csv')

        ############################################################################################################################################################################################

        ''' Same method completed for F_Y tables'''

        ############################################################################################################################################################################################
        for stressor_index in range(0, 6):
            for CF_table_column_index in range(0, 49):
                exiobase3.satellite.F_Y.iat[stressor_index, CF_table_column_index] = Land_CF_tables.iat[
                                                                                         stressor_index, CF_table_column_index] * \
                                                                                     exiobase3.satellite.F_Y.iat[
                                                                                         stressor_index, CF_table_column_index]

        for CF_table_column_index in range(0, 49):
            exiobase3.satellite.F_Y.iat[6, CF_table_column_index] = Land_CF_tables.iat[6, CF_table_column_index] * \
                                                                    exiobase3.satellite.F_Y.iat[
                                                                        6, CF_table_column_index]  # Core Characterisation of CO2 combustion stressors for terrestrial and aquatic climate change PDF
            exiobase3.satellite.F_Y.iat[7, CF_table_column_index] = Land_CF_tables.iat[7, CF_table_column_index] * \
                                                                    exiobase3.satellite.F_Y.iat[
                                                                        7, CF_table_column_index]  # Core Characterisation of CH4 combustion stressors for terrestrial and aquatic climate change PDF
            exiobase3.satellite.F_Y.iat[8, CF_table_column_index] = Land_CF_tables.iat[9, CF_table_column_index] * \
                                                                    exiobase3.satellite.F_Y.iat[
                                                                        8, CF_table_column_index]  # Core characterisation of methane release from agriculture for terrestrial and aquatic climate change PDF
            exiobase3.satellite.F_Y.iat[19, CF_table_column_index] = Land_CF_tables.iat[7, CF_table_column_index] * \
                                                                     exiobase3.satellite.F_Y.iat[
                                                                         19, CF_table_column_index]  # Core characterisation of methane release from agriculture for terrestrial and aquatic climate change PDF
            exiobase3.satellite.F_Y.iat[20, CF_table_column_index] = Land_CF_tables.iat[6, CF_table_column_index] * \
                                                                     exiobase3.satellite.F_Y.iat[
                                                                         20, CF_table_column_index]  # Core characterisation of CO2 release from peat decay in agriculture for terrestrial and aquatic climate change PDF
            exiobase3.satellite.F_Y.iat[21, CF_table_column_index] = Land_CF_tables.iat[9, CF_table_column_index] * \
                                                                     exiobase3.satellite.F_Y.iat[
                                                                         21, CF_table_column_index]  # Core characterisation of N20 release from agriculture for terrestrial and aquatic climate change PDF
            exiobase3.satellite.F_Y.iat[22, CF_table_column_index] = Land_CF_tables.iat[7, CF_table_column_index] * \
                                                                     exiobase3.satellite.F_Y.iat[
                                                                         22, CF_table_column_index]  # Core characterisation of methane release from waste for terrestrial and aquatic climate change PDF

        for stressor_index in range(3, 11):
            for CF_table_column_index in range(0, 49):
                exiobase3.satellite.F_Y.iat[stressor_index + 6, CF_table_column_index] = Land_CF_tables.iat[
                                                                                             8, CF_table_column_index] * \
                                                                                         exiobase3.satellite.F_Y.iat[
                                                                                             stressor_index + 6, CF_table_column_index]  # Core characterisation of fossil Methane non combustion stressors for terrestrial and aquatic climate change PDF
        for stressor_index in range(11, 13):
            for CF_table_column_index in range(0, 49):
                exiobase3.satellite.F_Y.iat[stressor_index + 6, CF_table_column_index] = Land_CF_tables.iat[
                                                                                             6, CF_table_column_index] * \
                                                                                         exiobase3.satellite.F_Y.iat[
                                                                                             stressor_index + 6, CF_table_column_index]  # Core characterisation of fossil Methane non combustion stressors for terrestrial and aquatic climate change PDF
        for stressor_index in range(17, 19):
            for CF_table_column_index in range(0, 49):
                exiobase3.satellite.F_Y.iat[stressor_index + 6, CF_table_column_index] = Land_CF_tables.iat[
                                                                                             6, CF_table_column_index] * \
                                                                                         exiobase3.satellite.F_Y.iat[
                                                                                             stressor_index + 6, CF_table_column_index]  # Core characterisations of CO2 for fossil and biogenic waste for terrestrial and aquatic climate change PDF

        for stressor_index in range(0, 103):
            for CF_table_column_index in range(0, 49):
                exiobase3.satellite.F_Y.iat[stressor_index + 25, CF_table_column_index] = Land_CF_tables.iat[
                                                                                              22, CF_table_column_index] * \
                                                                                          exiobase3.satellite.F_Y.iat[
                                                                                              stressor_index + 25, CF_table_column_index]  # Core characterisation of water consumption stressors. There are 103 water stressors, hence the range in the for loop

        for CF_table_column_index in range(0, 49):
            exiobase3.satellite.F_Y.iat[128, CF_table_column_index] = Land_CF_tables.iat[28, CF_table_column_index] * \
                                                                      exiobase3.satellite.F_Y.iat[
                                                                          128, CF_table_column_index]  # Characterisation of agricultural phosphorus emissions to soil stressors for freshwater eutrophication impact category
            exiobase3.satellite.F_Y.iat[130, CF_table_column_index] = Land_CF_tables.iat[28, CF_table_column_index] * \
                                                                      exiobase3.satellite.F_Y.iat[
                                                                          130, CF_table_column_index]  # Characterisation of agricultural phosphorus emissions to soil stressors for freshwater eutrophication impact category
            exiobase3.satellite.F_Y.iat[129, CF_table_column_index] = Land_CF_tables.iat[27, CF_table_column_index] * \
                                                                      exiobase3.satellite.F_Y.iat[
                                                                          129, CF_table_column_index]  # Characterisation of agricultural phosphorus emissions to water stressors for freshwater eutrophication impact category
            exiobase3.satellite.F_Y.iat[132, CF_table_column_index] = Land_CF_tables.iat[27, CF_table_column_index] * \
                                                                      exiobase3.satellite.F_Y.iat[
                                                                          131, CF_table_column_index]  # Characterisation of agricultural phosphorus emissions to water stressors for freshwater eutrophication impact category

        for CF_table_column_index in range(0, 49):
            exiobase3.satellite.F_Y.iat[131, CF_table_column_index] = Land_CF_tables.iat[25, CF_table_column_index] * \
                                                                      exiobase3.satellite.F_Y.iat[
                                                                          131, CF_table_column_index]  # Characterisation of Nitrogen emissions to wastewater for Marine eutrophication impact category.

        # Re-ordering F_Y stressor table so it matches index of D_cba and D_pba for addition below
        Nitrogen_df = pd.DataFrame(exiobase3.satellite.F_Y.iloc[131, :]).T

        Nitrogen_df.astype(float)

        Phosphoros_df = pd.DataFrame(exiobase3.satellite.F_Y.iloc[132, :]).T
        Phosphoros_df.astype(float)
        Appending_group = (Phosphoros_df, Nitrogen_df)
        exiobase3.satellite.F_Y = pd.DataFrame(exiobase3.satellite.F_Y.iloc[0:131, :])
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

        new_accounts = pymrio.calc_accounts(Char_table_S, exiobase3.L, exiobase3.Y,
                                            nr_sectors=200)  # Note here, we input Char_table_S rather than S for the calculation of the Biodiversity accounts

        D_cba_biod = pd.DataFrame(new_accounts[0])
        print(D_cba_biod.shape)
        D_cba_biod = pd.DataFrame(D_cba_biod)

        D_cba_biod = pd.DataFrame(
            D_cba_biod.loc[:, idx[:, ['Paddy rice', 'Wheat', 'Cereal grains nec', 'Vegetables, fruit, nuts', 'Oil seeds',
                                 'Sugar cane, sugar beet', 'Plant-based fibers', 'Crops nec', 'Cattle', 'Pigs', 'Poultry',
                                 'Meat animals nec', 'Animal products nec', 'Raw milk', 'Wool, silk-worm cocoons',
                                 'Products of forestry, logging and related services (02)',
                                 'Fish and other fishing products; services incidental of fishing (05)']]])  # Seggregating final consumer household demand
        D_cba_biod.to_csv('D_cba_test.csv')
        ColumnX = list(D_cba_biod.columns.levels[0])
        Column2 = []
        Product_categories = ['Paddy rice', 'Wheat', 'Cereal grains nec', 'Vegetables, fruit, nuts', 'Oil seeds',
                              'Sugar cane, sugar beet', 'Plant-based fibers', 'Crops nec', 'Cattle', 'Pigs', 'Poultry',
                              'Meat animals nec', 'Animal products nec', 'Raw milk', 'Wool, silk-worm cocoons',
                              'Products of forestry, logging and related services (02)',
                              'Fish and other fishing products; services incidental of fishing (05)']

        Column2 = ColumnX * len(Product_categories)
        Column3 = []
        for i in range(0, len(Product_categories)):
            Column3 += [Product_categories[i]] * 49
        Column1 = [year] * len(Column2)
        print(len(Column1))
        print(len(Column2))
        print(len(Column3))
        print(Column1)
        print(Column2)
        print(Column3)
        column_multi_index = pd.MultiIndex.from_arrays([Column1, Column2, Column3])
        D_cba_biod = pd.DataFrame(D_cba_biod.values, index=D_cba_biod.index, columns=column_multi_index)
        TS_D_cba_biod = pd.concat([TS_D_cba_biod, D_cba_biod], axis=1).reindex(D_cba_biod.index)
        print(TS_D_cba_biod)
        print(TS_D_cba_biod.shape)

        TS_D_cba_biod.to_csv('BF_D_cba_Med_Approach_Ver01.csv')

        D_pba_biod = pd.DataFrame(new_accounts[1])
        print(D_pba_biod.shape)
        D_pba_biod = pd.DataFrame(D_pba_biod)

        D_pba_biod = pd.DataFrame(
            D_pba_biod.loc[:, idx[:, ['Paddy rice', 'Wheat', 'Cereal grains nec', 'Vegetables, fruit, nuts', 'Oil seeds',
                                      'Sugar cane, sugar beet', 'Plant-based fibers', 'Crops nec', 'Cattle', 'Pigs',
                                      'Poultry',
                                      'Meat animals nec', 'Animal products nec', 'Raw milk', 'Wool, silk-worm cocoons',
                                      'Products of forestry, logging and related services (02)',
                                      'Fish and other fishing products; services incidental of fishing (05)']]])  # Seggregating final consumer household demand
        column_multi_index = pd.MultiIndex.from_arrays([Column1, Column2, Column3])
        D_pba_biod = pd.DataFrame(D_pba_biod.values, index=D_pba_biod.index, columns=column_multi_index)
        TS_D_pba_biod = pd.concat([TS_D_pba_biod, D_pba_biod], axis=1).reindex(D_pba_biod.index)
        print(TS_D_pba_biod)
        print(TS_D_pba_biod.shape)

        TS_D_pba_biod.to_csv('BF_D_pba_Med_Approach_Ver01.csv')

        D_imp_biod = pd.DataFrame(new_accounts[2])
        D_imp_biod.to_csv('D_imp_biod.csv')
        print(D_pba_biod.shape)
        D_imp_biod = pd.DataFrame(D_imp_biod)

        D_imp_biod = pd.DataFrame(
            D_imp_biod.loc[:, idx[:, ['Paddy rice', 'Wheat', 'Cereal grains nec', 'Vegetables, fruit, nuts', 'Oil seeds',
                                      'Sugar cane, sugar beet', 'Plant-based fibers', 'Crops nec', 'Cattle', 'Pigs',
                                      'Poultry',
                                      'Meat animals nec', 'Animal products nec', 'Raw milk', 'Wool, silk-worm cocoons',
                                      'Products of forestry, logging and related services (02)',
                                      'Fish and other fishing products; services incidental of fishing (05)']]])  # Seggregating final consumer household demand
        column_multi_index = pd.MultiIndex.from_arrays([Column1, Column2, Column3])
        D_imp_biod = pd.DataFrame(D_imp_biod.values, index=D_imp_biod.index, columns=column_multi_index)
        TS_D_imp_biod = pd.concat([TS_D_imp_biod, D_imp_biod], axis=1).reindex(D_imp_biod.index)
        print(TS_D_imp_biod)
        print(TS_D_imp_biod.shape)

        TS_D_pba_biod.to_csv('BF_D_imp_Med_Approach_Ver01.csv')

        D_exp_biod = pd.DataFrame(new_accounts[3])
        D_exp_biod.to_csv('D_exp_biod.csv')
        print(D_exp_biod.shape)
        D_exp_biod = pd.DataFrame(D_exp_biod)

        D_exp_biod = pd.DataFrame(
            D_exp_biod.loc[:, idx[:, ['Paddy rice', 'Wheat', 'Cereal grains nec', 'Vegetables, fruit, nuts', 'Oil seeds',
                                      'Sugar cane, sugar beet', 'Plant-based fibers', 'Crops nec', 'Cattle', 'Pigs',
                                      'Poultry',
                                      'Meat animals nec', 'Animal products nec', 'Raw milk', 'Wool, silk-worm cocoons',
                                      'Products of forestry, logging and related services (02)',
                                      'Fish and other fishing products; services incidental of fishing (05)']]])  # Seggregating final consumer household demand
        column_multi_index = pd.MultiIndex.from_arrays([Column1, Column2, Column3])
        D_exp_biod = pd.DataFrame(D_exp_biod.values, index=D_exp_biod.index, columns=column_multi_index)
        TS_D_exp_biod = pd.concat([TS_D_exp_biod, D_exp_biod], axis=1).reindex(D_exp_biod.index)
        print(TS_D_exp_biod)
        print(TS_D_exp_biod.shape)

        TS_D_pba_biod.to_csv('BF_D_exp_Med_Approach_Ver01.csv')


        import os

        myfile = 'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO3/IOT_'+ year +'_pxp.zip'

        ## If file exists, delete it ##
        if os.path.isfile('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO3/IOT_'+ year +'_pxp.zip'):
            os.remove('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO3/IOT_'+ year +'_pxp.zip')
        else:  ## Show an error ##
            print("Error: file not found")
        del exiobase3



        ######################################################################################################################################################################################################################################
        '''For calculating total footprint with F_Y '''
        ######################################################################################################################################################################################################################################
        '''' 
        D_cba_total = pd.DataFrame(D_cba_biod.groupby(axis=1, level=0,
                                                      sort=False).sum())  # Changing shape of D_cba from 153x9800 to 152x49 for matrix addition with F_Y
        D_cba_total = D_cba_total.add(F_Y_biod.values)  # matrix addition
        D_cba_total.to_csv('D_cba_total_median.csv')
        D_pba_total = pd.DataFrame(D_pba_biod.groupby(axis=1, level=0,
                                                      sort=False).sum())  # Changing shape of D_pba from 153x9800 to 152x49 for matrix addition with F_Y
        D_pba_total = D_pba_total.add(F_Y_biod.values)  # matrix addition
        D_pba_total.to_csv('D_pba_total_median.csv') '''
    else:
        land_stressors = pd.DataFrame(
            S.iloc[[446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 461, 462, 463, 464, 465],
            :])  # Seperation of land use categories using indexing. Rows obtained from csv file
        print(land_stressors)
        water_stressors = pd.DataFrame(S.iloc[923:1026])  # Blue water consumption stressor rows
        print(water_stressors)
        climate_change_stressors = pd.DataFrame(S.iloc[
                                                    [23, 24, 25, 67, 68, 69, 70, 71, 72, 73, 74, 92, 93, 426, 427, 429,
                                                     435, 437, 438]])  # Climate change stressor rows
        eutrophication_stressors = pd.DataFrame(S.iloc[[432, 433, 434, 440, 443]])  # Marine and Fresh eutrophication

        # Aggregation of fodder crops in exiobase land use categories to LC-IMPACT categories

        Annual_crop_df = pd.DataFrame(land_stressors.iloc[[2, 3, 4, 5, 6], :]).sum(
            0)  # Aggregation of the annual Fodder crop categories in exiobase to a singular LC-IMPACT category for Land Use (This will be characterised by the annual crop CF values for land
        print(Annual_crop_df)
        Annual_crop_df = pd.DataFrame(
            Annual_crop_df).T  # As python outputs a column vector for a summation operation, the transpose function T is used to return the annual crop dataframe to it's original Dataframe index/column set up with countries and products as the column index and stressor as the row index.
        Pasture_crop_df = pd.DataFrame(land_stressors.iloc[[14, 15, 16], :]).sum(
            0)  # Aggregation of Pasture crop land use categories
        Pasture_crop_df = pd.DataFrame(Pasture_crop_df).T
        Urban_df = pd.DataFrame(land_stressors.iloc[[17], :]).sum(0)  # Aggregation of Urban land use categories
        Urban_df = pd.DataFrame(Urban_df).T
        Intensive_forestry_df = pd.DataFrame(land_stressors.iloc[[13], :]).sum(
            0)  # Aggregation of Intensive forestry land use stresors to LC-Impact category
        Intensive_forestry_df = pd.DataFrame(Intensive_forestry_df).T
        Extensive_forestry_df = pd.DataFrame(land_stressors.iloc[[18], :]).sum(
            0)  # Aggregation of Intensive forestry land use stresors to LC-Impact
        Extensive_forestry_df = pd.DataFrame(Extensive_forestry_df).T

        # Re-creating a combined dataframe for the individual and aggregated land use stressors

        Land_aggregated_df = land_stressors
        Land_aggregated_df.drop(Land_aggregated_df.index[[2, 3, 4, 5, 6, 13, 14, 15, 16, 17, 18]], inplace=True)
        Individual_crop_stressor_names = list(Land_aggregated_df.index.values)
        landuse_list = (Annual_crop_df, Pasture_crop_df, Urban_df, Extensive_forestry_df, Intensive_forestry_df)
        new_land_categories_index = ['Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy Rice', 'Plant-based fibers',
                                     'Sugar', 'Vegetables, fruit, nuts ', 'Wheat', 'Annual crops', 'Pasture', 'Urban',
                                     'Extensive forestry', 'Intensive forestry']
        for i in landuse_list:
            Land_aggregated_df = Land_aggregated_df.append(
                i)  # Appending Land_aggregated_df with each of the aggregated land use categories

        Land_aggregated_df.reset_index()
        Land_aggregated_df.set_axis(new_land_categories_index, inplace=True)  # Updating the index row labels
        print(Land_aggregated_df)

        # Combining the aggregated land use stressor categories with the disaggregated land use stressors, and the stressors for the other impact categories being analysed. This is the final compiled stressor matrix.
        # Not necessary to add land stressors, but nice to have for future reference if required.

        stressor_list = (climate_change_stressors, water_stressors, eutrophication_stressors)
        exiobase3.satellite.S = Land_aggregated_df  # Full_stressor_list = All required stressors (aggregated and disaggregated) for footprint calculations
        for i in stressor_list:
            exiobase3.satellite.S = exiobase3.satellite.S.append(i)

        S = pd.DataFrame(exiobase3.satellite.S)
        S.rename(columns = iso3_to_full_names_dict, inplace= True)
        S.to_csv('S_check.csv')

        ##################################################################################################################################################################################################################

        '''Segregating required stressors from S_Y tables in exactly the same fashion as what was completed above for the S tables'''

        ##################################################################################################################################################################################################################

        S_Y = pd.DataFrame(exiobase3.satellite.S_Y)
        land_stressors_S_Y = pd.DataFrame(
            S_Y.iloc[[446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 461, 462, 463, 464, 465],
            :])  # Seperation of land use categories using indexing. Rows obtained from csv file
        water_stressors_S_Y = pd.DataFrame(S_Y.iloc[923:1026])  # Blue water consumption stressor rows
        climate_change_stressors_S_Y = pd.DataFrame(S_Y.iloc[
                                                        [23, 24, 25, 67, 68, 69, 70, 71, 72, 73, 74, 92, 93, 426, 427,
                                                         429,
                                                         435, 437, 438]])  # Global warming stressor rows
        eutrophication_stressors_S_Y = pd.DataFrame(
            S_Y.iloc[[432, 433, 434, 440, 443]])  # Marine and Fresh eutrophication

        # Combining the aggregated land use stressor categories with the disaggregated land use stressors, and the stressors for the other impact categories being analysed. This is the final compiled stressor matrix.

        # Aggregation of exiobase land use categories to LC-IMPACT categories_S_Y

        Annual_crop_df_S_Y = pd.DataFrame(land_stressors_S_Y.iloc[[2, 3, 4, 5, 6], :]).sum(
            0)  # Aggregation of the annual crop categories in exiobase to the singular LC-IMPACT category for Land Use
        Annual_crop_df_S_Y = pd.DataFrame(
            Annual_crop_df_S_Y).T  # As python outputs a column vector for a sumation operation, the transpose function T is used to return the annual crop dataframe to it's original Dataframe index/column set up with countries and products as the column index and stressor as the row index.
        Pasture_crop_df_S_Y = pd.DataFrame(land_stressors_S_Y.iloc[[14, 15, 16], :]).sum(
            0)  # Aggregation of Pasture crop land use categories
        Pasture_crop_df_S_Y = pd.DataFrame(Pasture_crop_df_S_Y).T
        Urban_df_S_Y = pd.DataFrame(land_stressors_S_Y.iloc[[17], :]).sum(0)  # Aggregation of Urban land use categories
        Urban_df_S_Y = pd.DataFrame(Urban_df_S_Y).T
        Intensive_forestry_df_S_Y = pd.DataFrame(land_stressors_S_Y.iloc[[13], :]).sum(
            0)  # Aggregation of Intensive forestry land use stresors to LC-Impact category
        Intensive_forestry_df_S_Y = pd.DataFrame(Intensive_forestry_df_S_Y).T
        Extensive_forestry_df_S_Y = pd.DataFrame(land_stressors_S_Y.iloc[[18], :]).sum(
            0)  # Aggregation of Intensive forestry land use stresors to LC-Impact
        Extensive_forestry_df_S_Y = pd.DataFrame(Extensive_forestry_df_S_Y).T

        # Re-creating a combined dataframe for the aggregated land use stressors_F_Y
        Land_aggregated_df_S_Y = land_stressors_S_Y
        Land_aggregated_df_S_Y.drop(Land_aggregated_df_S_Y.index[[2, 3, 4, 5, 6, 13, 14, 15, 16, 17, 18]], inplace=True)
        landuse_list = (
            Annual_crop_df_S_Y, Pasture_crop_df_S_Y, Urban_df_S_Y, Extensive_forestry_df_S_Y,
            Intensive_forestry_df_S_Y)
        new_land_categories_index = ['Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice', 'Plant-based fibers',
                                     'Sugar', 'Vegetables, fruit, nuts ', 'Wheat', 'Annual crops', 'Pasture', 'Urban',
                                     'Extensive forestry', 'Intensive forestry']
        for i in landuse_list:
            Land_aggregated_df_S_Y = Land_aggregated_df_S_Y.append(
                i)  # Appending Land_aggregated_df with each of the aggregated land use categories

        Land_aggregated_df_S_Y.reset_index()
        Land_aggregated_df_S_Y.set_axis(new_land_categories_index, inplace=True)  # Updating the index row labels

        # Combining the aggregated land use stressor categories with the disaggregated land use stressors, and the stressors for the other impact categories being analysed. This is the final compiled stressor matrix for F_Y.

        stressor_list_S_Y = (
            climate_change_stressors_S_Y, water_stressors_S_Y, eutrophication_stressors_S_Y)
        exiobase3.satellite.S_Y = Land_aggregated_df_S_Y  # Full_stressor_list = All required stressors (aggregated and disaggregated) for footprint calculations
        for i in stressor_list_S_Y:
            exiobase3.satellite.S_Y = exiobase3.satellite.S_Y.append(i)

        exiobase3.satellite.S_Y = pd.DataFrame(exiobase3.satellite.S_Y.loc[:, idx[:,
                                                                              'Final consumption expenditure by households']])  # Seggregating final consumer househould expenditure

        S_Y = pd.DataFrame(exiobase3.satellite.S_Y)

        S_Y.rename(columns = iso3_to_full_names_dict, inplace= True)


        '''With a new Y table, S table and S_Y table, all other tables are reset to the co-efficients
        for the recalculation of new x,F,Z,M tables. Resetting of coefficients with pymrio resets all tables in EXIOBASE other than the
        A and L matrices'''

        ##################################################################################################################################################################################################################
        exiobase3.reset_all_to_coefficients()
        print(exiobase3.A)  # 9800x9800
        exiobase3.L = pymrio.calc_L(exiobase3.A)
        print(exiobase3.L)  # 9800x9800

        print(exiobase3.x)  # 0
        print(exiobase3.satellite.F)  # 0
        print(exiobase3.Z)  # 0
        print(exiobase3.satellite.M)  # 0
        exiobase3.Y = pd.DataFrame(Y)  # Setting Y tables to Y tables formed in the first section of the code
        exiobase3.satellite.S = pd.DataFrame(S)  # Setting S tables to S tables formed in the second section of the code
        exiobase3.satellite.S_Y = pd.DataFrame(
            S_Y)  # Setting S_Y tables to S_Y tables formed in third section of the code
        Y = exiobase3.Y
        exiobase3.x = pymrio.calc_x_from_L(exiobase3.L, exiobase3.Y.sum(
            1))  # Using PYMRIO functionality to calculate x from L and Y tables
        exiobase3.Z = pymrio.calc_Z(exiobase3.A,
                                    exiobase3.x)  # Using PYMRIO functionality to calculate Z from A and x tables

        exiobase3.satellite.F_Y = pd.DataFrame(pymrio.calc_F_Y(exiobase3.satellite.S_Y, exiobase3.Y.sum(0)))
        exiobase3.satellite.F = pd.DataFrame(pymrio.calc_F(exiobase3.satellite.S, exiobase3.x))
        exiobase3.M = pd.DataFrame(pymrio.calc_M(exiobase3.satellite.S, exiobase3.L))
        #####################################################################################################################################################################

        '''The next section deals with characterizing the stressor table S, with the CF factors from table 'Land_CF_tables'.
           The S table is broken out into smaller S_impact tables to match the [ various impact categories for characterization.
           The table is reformed after characterization as Char_table with units PDF per elementary flow.
           This section also calculates the characterized footprint of F_Y, which is the footprint related to household consumption or
           the impacts required for the consumption to take place.Multiplication is done via index location and for loops at different
           levels, according to indexs in the Stressor tables S_, F_Y, and Land_CF_tables. '''

        ############################################################################################################################################################################################

        for crop_type in ['Cereal grains Nec', 'Crops Nec', 'Oil seeds', 'Paddy rice', 'Plant-based fibers',
                                     'Sugar', 'Vegetables, fruit, nuts ', 'Wheat']:
            for country in []:
                exiobase3.S.loc[crop_type, idx[country, :]] = exiobase3.S.loc[crop_type, idx[country, :]] * Land_CF_tables.loc[crop_type, country]
                exiobase3.S_Y.loc[crop_type, idx[country, :]] = exiobase3.S_Y.loc[crop_type, idx[country, :]] * Land_CF_tables.loc[crop_type, country]

        for crop_type in ['Annual crops', 'Pasture', 'Urban','Extensive forestry', 'Intensive forestry']:
            for country in []:
                exiobase3.S.loc[crop_type, idx[country, :]] = exiobase3.S.loc[crop_type, idx[country, :]] * LC_Impact_CF_tables.loc[crop_type,country]
                exiobase3.S_Y.loc[crop_type, idx[country, :]] = exiobase3.S_Y.loc[crop_type, idx[country, :]] * LC_Impact_CF_tables.loc[crop_type,country]

        for water_consumption in ['Water Consumption Blue - Agriculture - wheat', 'Water Consumption Blue - Agriculture - rice', 'Water Consumption Blue - Agriculture - other cereals',
                                  'Water Consumption Blue - Agriculture - oil crops', 'Water Consumption Blue - Agriculture - sugar crops', 'Water Consumption Blue - Agriculture - fibres',
                                  'Water Consumption Blue - Agriculture - other crops', 'Water Consumption Blue - Agriculture - fodder crops']:
            for country in []:
                exiobase3.S.loc[water_consumption, idx[country, :]]  = exiobase3.S.loc[water_consumption, idx[country, :]] * Water_CF_tables.loc[water_consumption,country]
                exiobase3.S_Y.loc[water_consumption, idx[country, :]]  = exiobase3.S_Y.loc[water_consumption, idx[country, :]] * Water_CF_tables.loc[water_consumption,country]

        exiobase3.S.loc['Water Consumption Blue - Agriculture - vegetables', idx[country, :]] = exiobase3.S.loc['Water Consumption Blue - Agriculture - vegetables', idx[country, :]] * Water_CF_tables.loc['Water Consumption Blue - Agriculture - Vegetables, fruit, nuts',country]
        exiobase3.S.loc['Water Consumption Blue - Agriculture - fruits', idx[country, :]] = exiobase3.S.loc['Water Consumption Blue - Agriculture - fruits', idx[country, :]] * Water_CF_tables.loc['Water Consumption Blue - Agriculture - Vegetables, fruit, nuts',country]
        exiobase3.S.loc['Water Consumption Blue - Agriculture - nuts', idx[country, :]] = exiobase3.S.loc['Water Consumption Blue - Agriculture - nuts', idx[country, :]] * Water_CF_tables.loc['Water Consumption Blue - Agriculture - Vegetables, fruit, nuts',country]
        exiobase3.S.loc['Water Consumption Blue - Agriculture - pulses', idx[country, :]] = exiobase3.S.loc['Water Consumption Blue - Agriculture - pulses', idx[country, :]] * Water_CF_tables.loc['Water Consumption Blue - Agriculture - Vegetables, fruit, nuts',country]
        exiobase3.S_Y.loc['Water Consumption Blue - Agriculture - vegetables', idx[country, :]] = exiobase3.S_Y.loc['Water Consumption Blue - Agriculture - vegetables', idx[country, :]] * Water_CF_tables.loc['Water Consumption Blue - Agriculture - Vegetables, fruit, nuts',country]
        exiobase3.S_Y.loc['Water Consumption Blue - Agriculture - fruits', idx[country, :]] = exiobase3.S_Y.loc['Water Consumption Blue - Agriculture - fruits', idx[country, :]] * Water_CF_tables.loc['Water Consumption Blue - Agriculture - Vegetables, fruit, nuts',country]
        exiobase3.S_Y.loc['Water Consumption Blue - Agriculture - nuts', idx[country, :]] = exiobase3.S_Y.loc['Water Consumption Blue - Agriculture - nuts', idx[country, :]] * Water_CF_tables.loc['Water Consumption Blue - Agriculture - Vegetables, fruit, nuts',country]
        exiobase3.S_Y.loc['Water Consumption Blue - Agriculture - pulses', idx[country, :]] = exiobase3.S_Y.loc['Water Consumption Blue - Agriculture - pulses', idx[country, :]] * Water_CF_tables.loc['Water Consumption Blue - Agriculture - Vegetables, fruit, nuts',country]

        ### water consumption that is not agricultural ####

        Get_index_S = list(exiobase3.S.iloc[926:1026,:].index.values)
        for water_consumption_type in Get_index_S:
            for country in []:
                exiobase3.S.loc[water_consumption_type, idx[country, :]] = exiobase3.S.loc[water_consumption_type, idx[country, :]] * LC_Impact_CF_tables.loc['Water consumption - core ', country]
                exiobase3.S_Y.loc[water_consumption_type, idx[country, :]] = exiobase3.S_Y.loc[water_consumption_type, idx[country, :]] * LC_Impact_CF_tables.loc['Water consumption - core ', country]

        ### Eutrophication ###

        for eutrophication_pollution in ['P - agriculture - water', 'Pxx - agriculture - water', 'P - waste - water']:
            for country in []:
                exiobase3.S.loc[eutrophication_pollution, idx[country, :]] = exiobase3.S.loc[eutrophication_pollution, idx[country, :]] * LC_Impact_CF_tables.loc['P emission to water ', country]

        for eutrophication_pollution in ['P - agriculture - soil', 'Pxx - agriculture - soil']:
            for country in []:
                exiobase3.S.loc[eutrophication_pollution, idx[country, :]] = exiobase3.S.loc[eutrophication_pollution, idx[country, :]] * LC_Impact_CF_tables.loc['P emission to soil ', country]

        for eutrophication_pollution in ['N - agriculture - water', 'N - waste - water']:
            for country in []:
                exiobase3.S.loc[eutrophication_pollution, idx[country, :]] = exiobase3.S.loc[eutrophication_pollution, idx[country, :]] * LC_Impact_CF_tables.loc['N emissions to freshwater', country]

        ### Climate Change ###

        for CO2_stressor in ['CO2 - combustion','CO2 - non combustion - Cement production - air','CO2 - non combustion - Lime production - air', 'CO2 - waste - biogenic - air','CO2 - waste - fossil - air', 'CO2 - agriculture - peat decay - air']:
            for country in []:
                exiobase3.S.loc[CO2_stressor, idx[country, :]] = exiobase3.S.loc[CO2_stressor, idx[country, :]] * LC_Impact_CF_tables.loc['Carbon dioxide (fossil) - core', country]

        Get_index_S = list(exiobase3.S.iloc[67:75, :].index.values)
        for Fossil_CH4_stressor in ['CH4 - combustion - air']:
            for country in []:
                exiobase3.S.loc[Fossil_CH4_stressor, idx[country, :]] = exiobase3.S.loc[Fossil_CH4_stressor, idx[country, :]] * LC_Impact_CF_tables.loc['Fossil methane - core', country]

        for CH4_stressor in [Get_index_S + ['CH4 - waste - air', 'CH4 - agriculture - air'] ] :
            for country in []:
                exiobase3.S.loc[CH4_stressor, idx[country, :]] = exiobase3.S.loc[CH4_stressor, idx[country, :]] * LC_Impact_CF_tables.loc['Methane - core', country]

        for N2O_stressor in ['N2O - combustion - air', 'N2O - agriculture - air']:
            for country in []:
                exiobase3.S.loc[N2O_stressor, idx[country, :]] = exiobase3.S.loc[N2O_stressor, idx[country, :]] * LC_Impact_CF_tables.loc['Nitrous oxide - core', country]




