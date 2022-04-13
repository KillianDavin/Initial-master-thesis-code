import pandas as pd
import numpy as np
import pymrio as py

''' 

May require to calculate proxy LC-IMPACT CF for Bermuda and Netherland Antilles (Land Use) - set ROW regional CF for these maybe? 

'''

''' 
Notes:
  
Countries in Exiobase ROW regions but not in Exiobase-Eora = {'Anguilla', 'St. Vincent and the Grenadines', 'Grenada', 'Cook Islands', 'Nauru', 'Guinea-Bissau', 'Sint Maarten', 'Dominica', 'Zanzibar', 'Equatorial Guinea', 'Curacao', 'Turks and Caicos Islands', 'Puerto Rico', 'Marshall Islands', 'St. Kitts and Nevis', 'Kiribati', 'Solomon Islands', 'Kosovo', 'Micronesia, Fed. Sts.', 'Montserrat', 'Palau', 'Comoros', 'Tonga', 'Timor-Leste', 'Tuvalu', 'St. Lucia'}

# no crops grown in Anguilla, Cook Island, Sint Maarten, Curacao, Turks and Caicos Islands, Marshall Islands, Palau, Comoros, Tuvalu

# Nauru, Zanzibar not included in MapSpam
    
#crops grown in Saint Vincent and the Grenadines, Grenada,Guinea-Bissau, Equatorial Guinea, Dominica, Puerto Rcio, St Kitts, Kiribatti,kosovo, Solomon Isls, Micronesia, Montserrat, 'Tonga', 'Timor-Leste', 'St. Lucia'

Countries in Eora-Exiobase but not in the Water-GAP-LC-IMPACT-CFS  = {'Maldives', 'Cayman Islands', 'Hong Kong', 'Seychelles', 'French Polynesia', 'Macao', 'Bermuda'} but note** according to MapSPam Hong Kong, French Polynesia, Maldives, Cayman Islands, Macao and Seychelles have no irrigated or normal crop production. Therefore can be removed from analysis or set to zero.
Countriees in Eora-Exiobase but not in LC-IMPACT = {}
Countries in Eora-Exiobase but not in Land_Use_CF = {'Bermuda', 'Netherlands Antilles'}

'''

#### First analysing and normalising country names in Exiobase_Eora, Exiobase and LC-IMPACT ####

'''

x_RMRIO = pd.read_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO_EORA_HYBRID/Year_2010_RMRIO/rmrio-data/Parsed_RMRIO_files/x.csv', index_col = [0,1], header = [0])

x_RMRIO.rename(index={'TFYR Macedonia':'Macedonia', 'Brunei':'Brunei Darussalam', 'Hong Kong S.A.R.':'Hong Kong','Viet Nam': 'Vietnam','UK': 'United Kingdom', 'USA':'United States','Gaza Strip': 'Palestine',
                                           'Macao SAR':'Macao', 'Kyrgyzstan':'Kyrgyz Republic', 'Federated States of Micronesia': 'Micronesia, Fed. Sts.', 'East Timor':'Timor-Leste',
                                           'The Bahamas':'Bahamas', 'Curaçao': 'Curacao','Saint Kitts and Nevis':'St. Kitts and Nevis','Saint Lucia':'St. Lucia', 'Saint Vincent and the Grenadines':'St. Vincent and the Grenadines',
                                           'Congo': 'Congo Republic', 'Cote dIvoire': "Cote d'Ivoire", 'Democratic Republic of the Congo': 'DR Congo', 'eSwatini':'Swaziland',
                                           'United Republic of Tanzania': 'Tanzania', 'São Tomé and Principe': 'Sao Tome and Principe', 'UAE': 'United Arab Emirates', 'Antigua': 'Antigua and Barbuda', 'Cape Verde': 'Cabo Verde' },level = 0, inplace=True)

x_RMRIO.drop(['Former USSR','Bermuda','Netherlands Antilles'], axis = 0, level = 0, inplace= True)

x_RMRIO.to_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO_EORA_HYBRID/Year_2010_RMRIO/rmrio-data/Parsed_RMRIO_files/x.csv')


Y_RMRIO = pd.read_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO_EORA_HYBRID/Year_2010_RMRIO/rmrio-data/Parsed_RMRIO_files/Y.csv',header = [0,1], index_col= [0,1])

Y_RMRIO.rename(index={'TFYR Macedonia':'Macedonia', 'Brunei':'Brunei Darussalam', 'Hong Kong S.A.R.':'Hong Kong','Viet Nam': 'Vietnam','UK': 'United Kingdom', 'USA':'United States','Gaza Strip': 'Palestine',
                                           'Macao SAR':'Macao', 'Kyrgyzstan':'Kyrgyz Republic', 'Federated States of Micronesia': 'Micronesia, Fed. Sts.', 'East Timor':'Timor-Leste',
                                           'The Bahamas':'Bahamas', 'Curaçao': 'Curacao','Saint Kitts and Nevis':'St. Kitts and Nevis','Saint Lucia':'St. Lucia', 'Saint Vincent and the Grenadines':'St. Vincent and the Grenadines',
                                           'Congo': 'Congo Republic', 'Cote dIvoire': "Cote d'Ivoire", 'Democratic Republic of the Congo': 'DR Congo', 'eSwatini':'Swaziland',
                                           'United Republic of Tanzania': 'Tanzania', 'São Tomé and Principe': 'Sao Tome and Principe', 'UAE': 'United Arab Emirates', 'Antigua': 'Antigua and Barbuda', 'Cape Verde': 'Cabo Verde' },level = 0, inplace=True)

Y_RMRIO.rename(columns = {'TFYR Macedonia':'Macedonia', 'Brunei':'Brunei Darussalam', 'Hong Kong S.A.R.':'Hong Kong','Viet Nam': 'Vietnam','UK': 'United Kingdom', 'USA':'United States','Gaza Strip': 'Palestine',
                                           'Macao SAR':'Macao', 'Kyrgyzstan':'Kyrgyz Republic', 'Federated States of Micronesia': 'Micronesia, Fed. Sts.', 'East Timor':'Timor-Leste',
                                           'The Bahamas':'Bahamas', 'Curaçao': 'Curacao','Saint Kitts and Nevis':'St. Kitts and Nevis','Saint Lucia':'St. Lucia', 'Saint Vincent and the Grenadines':'St. Vincent and the Grenadines',
                                           'Congo': 'Congo Republic', 'Cote dIvoire': "Cote d'Ivoire", 'Democratic Republic of the Congo': 'DR Congo', 'eSwatini':'Swaziland',
                                           'United Republic of Tanzania': 'Tanzania', 'São Tomé and Principe': 'Sao Tome and Principe', 'UAE': 'United Arab Emirates', 'Antigua': 'Antigua and Barbuda', 'Cape Verde': 'Cabo Verde' },level = 0, inplace=True )

#Y_RMRIO.drop(['Former USSR','Bermuda','Netherlands Antilles'], axis = 0, level = 0, inplace= True)
#Y_RMRIO.drop(['Former USSR','Bermuda','Netherlands Antilles'], axis = 1, level = 0, inplace= True)
#Y_RMRIO.to_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO_EORA_HYBRID/Year_2010_RMRIO/rmrio-data/Parsed_RMRIO_files/Y.csv')

S_Y_RMRIO = pd.read_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO_EORA_HYBRID/Year_2010_RMRIO/rmrio-data/Parsed_RMRIO_files/S_Y_RMRIO.csv',header = [0,1], index_col= [0,1])


S_Y_RMRIO.rename(columns = {'TFYR Macedonia':'Macedonia', 'Brunei':'Brunei Darussalam', 'Hong Kong S.A.R.':'Hong Kong','Viet Nam': 'Vietnam','UK': 'United Kingdom', 'USA':'United States','Gaza Strip': 'Palestine',
                                           'Macao SAR':'Macao', 'Kyrgyzstan':'Kyrgyz Republic', 'Federated States of Micronesia': 'Micronesia, Fed. Sts.', 'East Timor':'Timor-Leste',
                                           'The Bahamas':'Bahamas', 'Curaçao': 'Curacao','Saint Kitts and Nevis':'St. Kitts and Nevis','Saint Lucia':'St. Lucia', 'Saint Vincent and the Grenadines':'St. Vincent and the Grenadines',
                                           'Congo': 'Congo Republic', 'Cote dIvoire': "Cote d'Ivoire", 'Democratic Republic of the Congo': 'DR Congo', 'eSwatini':'Swaziland',
                                           'United Republic of Tanzania': 'Tanzania', 'São Tomé and Principe': 'Sao Tome and Principe', 'UAE': 'United Arab Emirates', 'Antigua': 'Antigua and Barbuda', 'Cape Verde': 'Cabo Verde' },level = 0, inplace=True )


S_Y_RMRIO.drop(['Bermuda','Netherlands Antilles'], axis = 1, level = 0, inplace= True)
S_Y_RMRIO.to_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO_EORA_HYBRID/Year_2010_RMRIO/rmrio-data/Parsed_RMRIO_files/S_Y_RMRIO.csv')

'''

####################################

'Characterising the stressor table S. Note the Eora-Exio base already has a pre characterised row for land use related Biodiversity impact, so therefore Blue water ' \
'Consumption is the only stressor that needs to be treated in the S_RMRIO table. This stressor is multiplied by the country LC-IMPACT CF factors for water stress given in  ' \
'C:/Users/Cillian/OneDrive - NTNU/Documents/NTNU project documents/CF sheets/CFs_water_consumption_ecosystems_20150917.xlsx'

#####################################
'''
countries_eora = set(list(x_RMRIO.index.get_level_values(0)))
print(countries_eora)
'''
LC_impact_national_CF = pd.ExcelFile('C:/Users/Cillian/OneDrive - NTNU/Documents/NTNU project documents/CF sheets/CFs_water_consumption_ecosystems_20150917.xlsx')

for n in LC_impact_national_CF.sheet_names:
    if n == 'Country level':
        Country_level_CF = LC_impact_national_CF.parse(sheet_name=n)
        Columns = Country_level_CF.iloc[1,1:].values
        index = Country_level_CF.iloc[2:,0]
        Country_level_CF = pd.DataFrame(Country_level_CF.iloc[2:,1:].values, index = index, columns= Columns)
        Country_level_CF.rename(index={"Ivory Coast":"Cote d'Ivoire", 'Gambia, The': 'Gambia',
                                           'St. Vincent & the G':'St. Vincent and the Grenadines', 'Solomon Is.': 'Solomon Islands', 'Saint Vincent and the Grenadines':'St. Vincent and the Grenadines'
                                           , 'Congo': "Congo Republic", 'Central African Rep': 'Central African Republic', 'Congo DRC': 'DR Congo', 'Kyrgyzstan':'Kyrgyz Republic',
                                           'Brunei':'Brunei Darussalam', 'Sao Tome & Principe': 'Sao Tome and Principe', 'Cape Verde': 'Cabo Verde', 'Bosnia & Herzegovin': 'Bosnia and Herzegovina',
                       'Bahamas, The':'Bahamas','Antigua & Barbuda' : 'Antigua and Barbuda', 'Netherlands Antille': 'Netherlands Antilles', 'Myanmar (Burma)': 'Myanmar', 'Falkland Islands (Islas Malvinas)': 'Falkland Islands', 'West Bank': 'Palestine', 'Tanzania, United Republic of': 'Tanzania'} ,inplace=True)
        index = Country_level_CF.index.values

        #Missing_countries_LC_water_impact = list(set(countries_eora) - set(index))
        #Missing_countries_LC_water_impact2 = list(set(index) - set(countries_eora))


S_RMRIO = pd.read_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO_EORA_HYBRID/Year_2010_RMRIO/rmrio-data/Parsed_RMRIO_files/S_RMRIO.csv', header = [0,1], index_col= [0])
S_RMRIO.rename(columns ={'TFYR Macedonia':'Macedonia', 'Brunei':'Brunei Darussalam', 'Hong Kong S.A.R.':'Hong Kong','Viet Nam': 'Vietnam','UK': 'United Kingdom', 'USA':'United States','Gaza Strip': 'Palestine',
                                           'Macao SAR':'Macao', 'Kyrgyzstan':'Kyrgyz Republic', 'Federated States of Micronesia': 'Micronesia, Fed. Sts.', 'East Timor':'Timor-Leste',
                                           'The Bahamas':'Bahamas', 'Curaçao': 'Curacao','Saint Kitts and Nevis':'St. Kitts and Nevis','Saint Lucia':'St. Lucia', 'Saint Vincent and the Grenadines':'St. Vincent and the Grenadines',
                                           'Congo': 'Congo Republic', 'Cote dIvoire': "Cote d'Ivoire", 'Democratic Republic of the Congo': 'DR Congo', 'eSwatini':'Swaziland',
                                           'United Republic of Tanzania': 'Tanzania', 'São Tomé and Principe': 'Sao Tome and Principe', 'UAE': 'United Arab Emirates', 'Antigua': 'Antigua and Barbuda', 'Cape Verde': 'Cabo Verde' },level = 0, inplace=True)
S_RMRIO = S_RMRIO.astype(float)
S_RMRIO.drop(['Bermuda','Netherlands Antilles'], axis = 1, level = 0, inplace= True)
countries_eora = set(list(S_RMRIO.columns.get_level_values(0)))
for country in countries_eora:
    print(country)
    print(S_RMRIO.loc['Blue water consumption', (country,)])
    S_RMRIO.loc['Blue water consumption', (country,)] = S_RMRIO.loc['Blue water consumption', (country,)].values * Country_level_CF.loc[country, 'CF core \n[PDF·yr/m3]']
    print(S_RMRIO.loc['Blue water consumption', (country,)])
S_RMRIO.to_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO_EORA_HYBRID/Year_2010_RMRIO/rmrio-data/Parsed_RMRIO_files/char_S_RMRIO.csv')


##################################

### characterised Stressor table S_RMRIO from above step. ###
'''
S_RMRIO = pd.read_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO_EORA_HYBRID/Year_2010_RMRIO/rmrio-data/Parsed_RMRIO_files/char_S_RMRIO.csv', header = [0,1], index_col= [0])

L_RMRIO = pd.DataFrame()

### Reading in A matrix in chunk sizes of 1000 and performing Taylor series expansion to calculate L, for each chunk ###

for chunk in pd.read_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO_EORA_HYBRID/Year_2010_RMRIO/rmrio-data/Parsed_RMRIO_files/A.csv',header= [0,1], index_col= [0,1], dtype= object , chunksize = 1000):
                
    A_RMRIO = pd.DataFrame(chunk)
    A_RMRIO = A_RMRIO.astype(float)
    index0 = A_RMRIO.index.get_level_values(0)
    print(index0)
    index1 = A_RMRIO.index.get_level_values(1)
    column1 = A_RMRIO.columns.get_level_values(0)
    column2 = A_RMRIO.columns.get_level_values(1)
    A_RMRIO = np.array(A_RMRIO.values)
    L1 = np.array(A_RMRIO)
    for n in range (0,5):
        L0 =  np.multiply(A_RMRIO, A_RMRIO)
        L1 = L1 + L0
        A_RMRIO = np.array(L0)

    L1 = pd.DataFrame(L1, index = [index0, index1], columns = [column1, column2])
    L_RMRIO = L_RMRIO.append(L1)
    print(L_RMRIO)

L_index0 = L_RMRIO.index.get_level_values(0)
L_index1 = L_RMRIO.index.get_level_values(1)
L_column0 = L_RMRIO.columns.get_level_values(0)
L_column1 = L_RMRIO.columns.get_level_values(1)

I = np.identity(len(L_RMRIO.columns))
L_RMRIO = np.array(L_RMRIO.values)
L_RMRIO = I + L_RMRIO
L_RMRIO = pd.DataFrame(L_RMRIO, index = [L_index0, L_index1], columns= [L_column0, L_column1])
L_RMRIO.drop(['Former USSR','Bermuda','Netherlands Antilles'], axis = 1, level = 0, inplace= True)
L_RMRIO.drop(['Former USSR','Bermuda','Netherlands Antilles'], axis = 0, level = 0, inplace= True)

L_RMRIO.rename(columns ={'TFYR Macedonia':'Macedonia', 'Brunei':'Brunei Darussalam', 'Hong Kong S.A.R.':'Hong Kong','Viet Nam': 'Vietnam','UK': 'United Kingdom', 'USA':'United States','Gaza Strip': 'Palestine',
                                           'Macao SAR':'Macao', 'Kyrgyzstan':'Kyrgyz Republic', 'Federated States of Micronesia': 'Micronesia, Fed. Sts.', 'East Timor':'Timor-Leste',
                                           'The Bahamas':'Bahamas', 'Curaçao': 'Curacao','Saint Kitts and Nevis':'St. Kitts and Nevis','Saint Lucia':'St. Lucia', 'Saint Vincent and the Grenadines':'St. Vincent and the Grenadines',
                                           'Congo': 'Congo Republic', 'Cote dIvoire': "Cote d'Ivoire", 'Democratic Republic of the Congo': 'DR Congo', 'eSwatini':'Swaziland',
                                           'United Republic of Tanzania': 'Tanzania', 'São Tomé and Principe': 'Sao Tome and Principe', 'UAE': 'United Arab Emirates', 'Antigua': 'Antigua and Barbuda', 'Cape Verde': 'Cabo Verde' },level = 0, inplace=True)

L_RMRIO.rename(index = {'TFYR Macedonia':'Macedonia', 'Brunei':'Brunei Darussalam', 'Hong Kong S.A.R.':'Hong Kong','Viet Nam': 'Vietnam','UK': 'United Kingdom', 'USA':'United States','Gaza Strip': 'Palestine',
                                           'Macao SAR':'Macao', 'Kyrgyzstan':'Kyrgyz Republic', 'Federated States of Micronesia': 'Micronesia, Fed. Sts.', 'East Timor':'Timor-Leste',
                                           'The Bahamas':'Bahamas', 'Curaçao': 'Curacao','Saint Kitts and Nevis':'St. Kitts and Nevis','Saint Lucia':'St. Lucia', 'Saint Vincent and the Grenadines':'St. Vincent and the Grenadines',
                                           'Congo': 'Congo Republic', 'Cote dIvoire': "Cote d'Ivoire", 'Democratic Republic of the Congo': 'DR Congo', 'eSwatini':'Swaziland',
                                           'United Republic of Tanzania': 'Tanzania', 'São Tomé and Principe': 'Sao Tome and Principe', 'UAE': 'United Arab Emirates', 'Antigua': 'Antigua and Barbuda', 'Cape Verde': 'Cabo Verde' },level = 0, inplace=True)



Y_RMRIO = pd.read_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO_EORA_HYBRID/Year_2010_RMRIO/rmrio-data/Parsed_RMRIO_files/Y.csv', low_memory= False)
F_RMRIO = pd.read_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO_EORA_HYBRID/Year_2010_RMRIO/rmrio-data/Parsed_RMRIO_files/ext.csv')
F_Y_RMRIO = pd.read_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO_EORA_HYBRID/Year_2010_RMRIO/rmrio-data/Parsed_RMRIO_files/ext_hh.csv')

Exiobase_regions = pd.ExcelFile('C:/Users/Cillian/OneDrive - NTNU/Documents/NTNU project documents/CF sheets/Exiobase_3rx_data.xlsx')

for n in Exiobase_regions.sheet_names:
    if n == 'Countries':
        Exiobase_countries = Exiobase_regions.parse(sheet_name = n)
        Exiobase_regions.close()

columns_exio = list(Exiobase_countries.columns)
columns_exio.pop(0)
Exiobase_countries = pd.DataFrame(Exiobase_countries.iloc[:,1:].values, index = Exiobase_countries.iloc[:,0].values, columns= columns_exio)
Exiobase_countries = set(list(Exiobase_countries.index.values))

#x_RMRIO.set_index('region', inplace =True)


Land_CF = pd.read_csv('C:/Users/Cillian/OneDrive - NTNU/Documents/NTNU project documents/ArcGIS_shapefiles_MT2022/GIS_layers_output/Final_sheets_for_Exiobase/land_characterization_factors_ver02.csv')
Land_CF.set_index('ADMIN', inplace =True)

Water_CF = pd.read_csv('C:/Users/Cillian/OneDrive - NTNU/Documents/NTNU project documents/ArcGIS_shapefiles_MT2022/GIS_layers_output/Final_sheets_for_Exiobase/Watershed_aggregated_national_level_characterisation_factors_ver01.csv')
Water_CF.set_index('Unnamed: 0', inplace = True)

Land_CF.rename(index={'Republic of Serbia':'Serbia', 'North Macedonia':'Macedonia', 'Brunei':'Brunei Darussalam', 'Hong Kong S.A.R.':'Hong Kong','United States of America': 'United States',
                                           'Macao S.A.R':'Macao', 'Kyrgyzstan':'Kyrgyz Republic', 'Federated States of Micronesia': 'Micronesia, Fed. Sts.', 'East Timor':'Timor-Leste',
                                           'The Bahamas':'Bahamas', 'Curaçao': 'Curacao','Saint Kitts and Nevis':'St. Kitts and Nevis','Saint Lucia':'St. Lucia', 'Saint Vincent and the Grenadines':'St. Vincent and the Grenadines',
                                           'Republic of the Congo': 'Congo Republic', 'Ivory Coast': "Cote d'Ivoire", 'Democratic Republic of the Congo': 'DR Congo', 'eSwatini':'Swaziland',
                                           'United Republic of Tanzania': 'Tanzania', 'São Tomé and Principe': 'Sao Tome and Principe', 'Czechia' : 'Czech Republic' },inplace=True)
Water_CF.rename(index={"Ivory Coast":"Cote d'Ivoire", 'The Gambia': 'Gambia',
                                           'St. Vincent & the G':'St. Vincent and the Grenadines', 'Solomon Is.': 'Solomon Islands', 'Saint Vincent and the Grenadines':'St. Vincent and the Grenadines'
                                           , 'Congo': "Congo Republic", 'Central African Rep': 'Central African Republic', 'Congo DRC': 'DR Congo', 'Kyrgyzstan':'Kyrgyz Republic',
                                           'Brunei':'Brunei Darussalam', 'Sao Tome & Principe': 'Sao Tome and Principe', 'Cape Verde': 'Cabo Verde', 'Bosnia & Herzegovin': 'Bosnia and Herzegovina',
                       'The Bahamas':'Bahamas','Antigua & Barbuda' : 'Antigua and Barbuda', 'Netherlands Antille': 'Netherlands Antilles'} ,inplace=True)

### Cleaning x, A, Y, F, and F_Y matrices before manipulation ###

### Cleaning x ###

x_RMRIO.rename(index={'TFYR Macedonia':'Macedonia', 'Brunei':'Brunei Darussalam', 'Hong Kong S.A.R.':'Hong Kong','Viet Nam': 'Vietnam','UK': 'United Kingdom', 'USA':'United States','Gaza Strip': 'Palestine',
                                           'Macao SAR':'Macao', 'Kyrgyzstan':'Kyrgyz Republic', 'Federated States of Micronesia': 'Micronesia, Fed. Sts.', 'East Timor':'Timor-Leste',
                                           'The Bahamas':'Bahamas', 'Curaçao': 'Curacao','Saint Kitts and Nevis':'St. Kitts and Nevis','Saint Lucia':'St. Lucia', 'Saint Vincent and the Grenadines':'St. Vincent and the Grenadines',
                                           'Congo': 'Congo Republic', 'Cote dIvoire': "Cote d'Ivoire", 'Democratic Republic of the Congo': 'DR Congo', 'eSwatini':'Swaziland',
                                           'United Republic of Tanzania': 'Tanzania', 'São Tomé and Principe': 'Sao Tome and Principe', 'UAE': 'United Arab Emirates', 'Antigua': 'Antigua and Barbuda', 'Cape Verde': 'Cabo Verde' },level = 0, inplace=True)

x_RMRIO.drop('Former USSR', axis = 0, inplace= True)
print(x_RMRIO)
### Cleaning Y ###

A_RMRIO_column0 = Y_RMRIO.iloc[2:, 0].values  #list of countries length = 30807
Y_RMRIO_column0 = list(Y_RMRIO.iloc[2:,0].values) #list of countries length = 30807
Y_RMRIO_column0 = sorted(set(Y_RMRIO_column0), key=Y_RMRIO_column0.index) #set of countries in order
new_list = []
for n in range(0,len(Y_RMRIO_column0)):
    new_list += [Y_RMRIO_column0[n]]*6
Y_RMRIO_column0 = new_list   #list of countries (x6 entries per country/final demand category) length = 1134
Y_RMRIO_column1 = Y_RMRIO.iloc[0,2:].values #list of final demand categories (6), length = 1134
Y_RMRIO_index0 = Y_RMRIO.iloc[2:,0].values #list of countries length = 30807
Y_RMRIO_index1 = Y_RMRIO.iloc[2:,1].values #list of commodities/industries, length = 3807
Y_RMRIO = Y_RMRIO.iloc[2:,2:]  # shape: 30807 x 1134
Y_RMRIO = pd.DataFrame(Y_RMRIO.values, index = [Y_RMRIO_index0,Y_RMRIO_index1], columns = [Y_RMRIO_column0, Y_RMRIO_column1])
Y_RMRIO.drop('Former USSR', axis = 1, level = 0, inplace= True)
Y_RMRIO.drop('Former USSR', axis = 0, level = 0, inplace= True)
print(Y_RMRIO)
### Cleaning A ####

A_RMRIO.set_index(['region'], inplace =True)
A_RMRIO_index1 = A_RMRIO.iloc[3:,0 ].values # list of commodites according to size of row portion of A matrix read in.

A_RMRIO_column1 = A_RMRIO.iloc[0,1:].values #list of commodities by country, length = 3807
A_RMRIO = A_RMRIO.iloc[3:,1:]  # 30807 x 30807 (note: in reality row size = number of rows read in from csv)
A_RMRIO_index0 = list(A_RMRIO.index.values) #list of countries according to size of row portion of A matrix read in.
A_RMRIO = pd.DataFrame(A_RMRIO.values, index = [A_RMRIO_index0, A_RMRIO_index1], columns = [A_RMRIO_column0, A_RMRIO_column1])
print(list(A_RMRIO.index.get_level_values(0)))
A_RMRIO.drop('Former USSR', axis = 1, level = 0, inplace= True)
print(A_RMRIO)

'''
'''
### Cleaning F and forming S ###

F_RMRIO = pd.read_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO_EORA_HYBRID/Year_2010_RMRIO/rmrio-data/Parsed_RMRIO_files/ext.csv', index_col = [0], header = [0,1])
F_Y_RMRIO = pd.read_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO_EORA_HYBRID/Year_2010_RMRIO/rmrio-data/Parsed_RMRIO_files/ext_hh.csv', index_col = [0], header = [0,1])

F_RMRIO.drop('Former USSR', axis = 1, level = 0, inplace= True)
F_Y_RMRIO.drop('Former USSR', axis = 1, level = 0, inplace = True)
F_RMRIO = F_RMRIO.loc[['Land-use area', 'Blue water consumption', 'Land-use related biodiversity loss'],:]
F_RMRIO.to_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO_EORA_HYBRID/Year_2010_RMRIO/rmrio-data/Parsed_RMRIO_files/F_RMRIO.csv')
F_Y_RMRIO = F_Y_RMRIO.loc[['Land-use area', 'Blue water consumption', 'Land-use related biodiversity loss'],:]
F_Y_RMRIO.to_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO_EORA_HYBRID/Year_2010_RMRIO/rmrio-data/Parsed_RMRIO_files/F_Y_RMRIO.csv')
F_Y_RMRIO = F_Y_RMRIO.astype(float)
Y_RMRIO = Y_RMRIO.astype(float)
#S_RMRIO = py.calc_S(F_RMRIO,x_RMRIO)
#S_RMRIO.to_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO_EORA_HYBRID/Year_2010_RMRIO/rmrio-data/Parsed_RMRIO_files/S_RMRIO.csv')
print(pd.DataFrame(Y_RMRIO.sum(0)))
S_Y_RMRIO = py.calc_S_Y(F_Y_RMRIO, pd.DataFrame(Y_RMRIO.sum(0)))
S_Y_RMRIO.to_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO_EORA_HYBRID/Year_2010_RMRIO/rmrio-data/Parsed_RMRIO_files/S_Y_RMRIO.csv')
'''