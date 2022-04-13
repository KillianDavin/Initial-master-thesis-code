import pandas as pd
import numpy as np
import pymrio as py

idx = pd.IndexSlice  # Slicing of multi index columns for separating out multiindex columns
### characterised Stressor table S_RMRIO from previous step. ###

S_RMRIO = pd.read_csv(
    'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO_EORA_HYBRID/Year_2010_RMRIO/rmrio-data/Parsed_RMRIO_files/char_S_RMRIO.csv',
    header=[0, 1], index_col=[0])
Y_RMRIO = pd.read_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO_EORA_HYBRID/Year_2010_RMRIO/rmrio-data/Parsed_RMRIO_files/Y.csv',
    header=[0, 1], index_col=[0,1])


print(S_RMRIO.shape)
print(Y_RMRIO.shape)
L_RMRIO = pd.DataFrame()

### Reading
#
# print(
# in A matrix in chunk sizes of 1000 and performing Taylor series expansion to calculate L, for each chunk ###

for chunk in pd.read_csv(
        'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO_EORA_HYBRID/Year_2010_RMRIO/rmrio-data/Parsed_RMRIO_files/A.csv',
        header=[0, 1], index_col=[0, 1], dtype=object, chunksize=1000):

    A_RMRIO = pd.DataFrame(chunk)
    A_RMRIO = A_RMRIO.astype(float)
    index0 = A_RMRIO.index.get_level_values(0)
    print(index0)
    index1 = A_RMRIO.index.get_level_values(1)
    column1 = A_RMRIO.columns.get_level_values(0)
    column2 = A_RMRIO.columns.get_level_values(1)
    A_RMRIO = np.array(A_RMRIO.values)
    L1 = np.array(A_RMRIO)
    for n in range(0, 5):
        L0 = np.multiply(A_RMRIO, A_RMRIO)
        L1 = L1 + L0
        A_RMRIO = np.array(L0)

    L1 = pd.DataFrame(L1, index=[index0, index1], columns=[column1, column2])
    L_RMRIO = L_RMRIO.append(L1)
    print(L_RMRIO)

L_index0 = L_RMRIO.index.get_level_values(0)
L_index1 = L_RMRIO.index.get_level_values(1)
L_column0 = L_RMRIO.columns.get_level_values(0)
L_column1 = L_RMRIO.columns.get_level_values(1)

I = np.identity(len(L_RMRIO.columns))
L_RMRIO = np.array(L_RMRIO.values)
L_RMRIO = I + L_RMRIO
L_RMRIO = pd.DataFrame(L_RMRIO, index=[L_index0, L_index1], columns=[L_column0, L_column1])
L_RMRIO.drop(['Former USSR', 'Bermuda', 'Netherlands Antilles'], axis=1, level=0, inplace=True)
L_RMRIO.drop(['Former USSR', 'Bermuda', 'Netherlands Antilles'], axis=0, level=0, inplace=True)

L_RMRIO.rename(columns={'TFYR Macedonia': 'Macedonia', 'Brunei': 'Brunei Darussalam', 'Hong Kong S.A.R.': 'Hong Kong',
                        'Viet Nam': 'Vietnam', 'UK': 'United Kingdom', 'USA': 'United States',
                        'Gaza Strip': 'Palestine',
                        'Macao SAR': 'Macao', 'Kyrgyzstan': 'Kyrgyz Republic',
                        'Federated States of Micronesia': 'Micronesia, Fed. Sts.', 'East Timor': 'Timor-Leste',
                        'The Bahamas': 'Bahamas', 'Curaçao': 'Curacao', 'Saint Kitts and Nevis': 'St. Kitts and Nevis',
                        'Saint Lucia': 'St. Lucia',
                        'Saint Vincent and the Grenadines': 'St. Vincent and the Grenadines',
                        'Congo': 'Congo Republic', 'Cote dIvoire': "Cote d'Ivoire",
                        'Democratic Republic of the Congo': 'DR Congo', 'eSwatini': 'Swaziland',
                        'United Republic of Tanzania': 'Tanzania', 'São Tomé and Principe': 'Sao Tome and Principe',
                        'UAE': 'United Arab Emirates', 'Antigua': 'Antigua and Barbuda', 'Cape Verde': 'Cabo Verde'},
               level=0, inplace=True)

L_RMRIO.rename(index={'TFYR Macedonia': 'Macedonia', 'Brunei': 'Brunei Darussalam', 'Hong Kong S.A.R.': 'Hong Kong',
                      'Viet Nam': 'Vietnam', 'UK': 'United Kingdom', 'USA': 'United States', 'Gaza Strip': 'Palestine',
                      'Macao SAR': 'Macao', 'Kyrgyzstan': 'Kyrgyz Republic',
                      'Federated States of Micronesia': 'Micronesia, Fed. Sts.', 'East Timor': 'Timor-Leste',
                      'The Bahamas': 'Bahamas', 'Curaçao': 'Curacao', 'Saint Kitts and Nevis': 'St. Kitts and Nevis',
                      'Saint Lucia': 'St. Lucia', 'Saint Vincent and the Grenadines': 'St. Vincent and the Grenadines',
                      'Congo': 'Congo Republic', 'Cote dIvoire': "Cote d'Ivoire",
                      'Democratic Republic of the Congo': 'DR Congo', 'eSwatini': 'Swaziland',
                      'United Republic of Tanzania': 'Tanzania', 'São Tomé and Principe': 'Sao Tome and Principe',
                      'UAE': 'United Arab Emirates', 'Antigua': 'Antigua and Barbuda', 'Cape Verde': 'Cabo Verde'},
               level=0, inplace=True)
print(L_RMRIO.shape)
Y_RMRIO = Y_RMRIO.groupby(level= 0, axis = 1, sort = False).sum(1)
Y_RMRIO = pd.DataFrame(Y_RMRIO)
print(Y_RMRIO.shape)
new_accounts = py.calc_accounts(S_RMRIO, L_RMRIO, Y_RMRIO)  # Note here, we input Char_table_S rather than S for the calculation of the Biodiversity accounts

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
myfile = 'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Biodiversity Footprint/EXIO3/BF_D_cba_2010_EORA_EXIO_All_Y_categories.csv'
D_cba_biod.to_csv(myfile)
