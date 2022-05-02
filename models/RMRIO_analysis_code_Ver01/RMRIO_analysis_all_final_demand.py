import pandas as pd
import numpy as np
import pymrio as py

idx = pd.IndexSlice  # Slicing of multi index columns for separating out multiindex columns

'''

Characterised Stressor table S_RMRIO from previous step. Endpoint stressor matrix consists of
land related biodiversity impacts and water consumption related biodiversity impacts.

'''

### Read in S_RMRIO & Y_RMRIO files here ###

S_RMRIO = pd.read_csv(
    'C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO_EORA_HYBRID/Year_2010_RMRIO/rmrio-data/Parsed_RMRIO_files/char_S_RMRIO.csv',
    header=[0, 1], index_col=[0])
S_RMRIO = S_RMRIO.as_type(float)

Y_RMRIO = pd.read_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO_EORA_HYBRID/Year_2010_RMRIO/rmrio-data/Parsed_RMRIO_files/Y.csv',
    header=[0, 1], index_col=[0,1])
Y_RMRIO = Y_RMRIO.as_type(float)

### Reading in A matrix, and cleaning country names ###

A_RMRIO = pd.read_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO_EORA_HYBRID/Year_2010_RMRIO/rmrio-data/Parsed_RMRIO_files/A.csv',
        header=[0, 1], index_col=[0, 1], dtype=object)
A_RMRIO = A_RMRIO.as_type(float)
A_RMRIO.drop(['Former USSR', 'Bermuda', 'Netherlands Antilles'], axis=1, level=0, inplace=True)
A_RMRIO.drop(['Former USSR', 'Bermuda', 'Netherlands Antilles'], axis=0, level=0, inplace=True)

A_RMRIO.rename(columns={'TFYR Macedonia': 'Macedonia', 'Brunei': 'Brunei Darussalam', 'Hong Kong S.A.R.': 'Hong Kong',
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

A_RMRIO.rename(index={'TFYR Macedonia': 'Macedonia', 'Brunei': 'Brunei Darussalam', 'Hong Kong S.A.R.': 'Hong Kong',
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

### Grouping all consumption categories together for facilitating footprint calculations via PYMRIO ###

Y_RMRIO = pd.DataFrame(Y_RMRIO.groupby(level=0, axis=1, sort=False).sum(1))

### Calculating L matrix, via matrix inversion, using PYMRIO ###

L_RMRIO = py.calc_L(A_RMRIO)

new_accounts = py.calc_accounts(S_RMRIO, L_RMRIO, Y_RMRIO)  # Note here, we input Characterised table S_RMRIO rather than elementary stressor table S for the calculation of the Biodiversity accounts

D_cba_biod = pd.DataFrame(new_accounts[0])
D_cba_biod = pd.DataFrame(D_cba_biod)

D_cba_biod = pd.DataFrame(
D_cba_biod.loc[:, idx[:, ['Paddy rice', 'Wheat', 'Cereal grains nec', 'Vegetables, fruit, nuts', 'Oil seeds',
                          'Sugar cane, sugar beet', 'Plant-based fibers', 'Crops nec', 'Cattle', 'Pigs', 'Poultry',
                          'Meat animals nec', 'Animal products nec', 'Raw milk',
                          'Fish and other fishing products; services incidental of fishing (05)', 'Food products nec','Beverages', 'Sugar', 'Fish products', 'Dairy products',
                          'Products of meat cattle', 'Products of meat pigs', 'Products of meat poultry', 'Meat products nec', 'products of Vegetable oils and fats', 'Processed rice']]])  # Seggregating final consumer household demand

D_cba_biod.to_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Biodiversity Footprint/EXIO3/BF_D_cba_2010_EORA_EXIO_All_Y_categories.csv')

D_pba_biod = pd.DataFrame(new_accounts[1])
D_pba_biod = pd.DataFrame(D_pba_biod)

D_pba_biod = pd.DataFrame(
D_pba_biod.loc[:, idx[:, ['Paddy rice', 'Wheat', 'Cereal grains nec', 'Vegetables, fruit, nuts', 'Oil seeds',
                          'Sugar cane, sugar beet', 'Plant-based fibers', 'Crops nec', 'Cattle', 'Pigs', 'Poultry',
                          'Meat animals nec', 'Animal products nec', 'Raw milk',
                          'Fish and other fishing products; services incidental of fishing (05)', 'Food products nec','Beverages', 'Sugar', 'Fish products', 'Dairy products',
                          'Products of meat cattle', 'Products of meat pigs', 'Products of meat poultry', 'Meat products nec', 'products of Vegetable oils and fats', 'Processed rice']]])  # Seggregating final consumer household demand

D_pba_biod.to_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Biodiversity Footprint/EXIO3/BF_D_pba_2010_EORA_EXIO_All_Y_categories.csv')

D_imp_biod = pd.DataFrame(new_accounts[2])
D_imp_biod = pd.DataFrame(D_imp_biod)

D_imp_biod = pd.DataFrame(
D_imp_biod.loc[:, idx[:, ['Paddy rice', 'Wheat', 'Cereal grains nec', 'Vegetables, fruit, nuts', 'Oil seeds',
                          'Sugar cane, sugar beet', 'Plant-based fibers', 'Crops nec', 'Cattle', 'Pigs', 'Poultry',
                          'Meat animals nec', 'Animal products nec', 'Raw milk',
                          'Fish and other fishing products; services incidental of fishing (05)', 'Food products nec','Beverages', 'Sugar', 'Fish products', 'Dairy products',
                          'Products of meat cattle', 'Products of meat pigs', 'Products of meat poultry', 'Meat products nec', 'products of Vegetable oils and fats', 'Processed rice']]])  # Seggregating final consumer household demand

D_imp_biod.to_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Biodiversity Footprint/EXIO3/BF_D_imp_2010_EORA_EXIO_All_Y_categories.csv')

D_exp_biod = pd.DataFrame(new_accounts[3])
D_exp_biod = pd.DataFrame(D_exp_biod)

D_exp_biod = pd.DataFrame(
D_exp_biod.loc[:, idx[:, ['Paddy rice', 'Wheat', 'Cereal grains nec', 'Vegetables, fruit, nuts', 'Oil seeds',
                          'Sugar cane, sugar beet', 'Plant-based fibers', 'Crops nec', 'Cattle', 'Pigs', 'Poultry',
                          'Meat animals nec', 'Animal products nec', 'Raw milk',
                          'Fish and other fishing products; services incidental of fishing (05)', 'Food products nec','Beverages', 'Sugar', 'Fish products', 'Dairy products',
                          'Products of meat cattle', 'Products of meat pigs', 'Products of meat poultry', 'Meat products nec', 'products of Vegetable oils and fats', 'Processed rice']]])  # Seggregating final consumer household demand

D_exp_biod.to_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/processed/Biodiversity Footprint/EXIO3/BF_D_exp_2010_EORA_EXIO_All_Y_categories.csv')