"""Pandas import of the RMRIO database.
Cabernard, Livia, and Stephan Pfister. 2021. ‘A Highly Resolved MRIO Database
for Analyzing Environmental Footprints and Green Economy Progress’.
Science of The Total Environment 755 (February): 142587.
https://doi.org/10.1016/j.scitotenv.2020.142587.
Download the RMRIO database via: https://zenodo.org/record/3993659
Author of this script is jonas.bunsen@tu-berlin.de
Github page: https://github.com/jbnsn/RMRIO-database-py-import
Version: 1.0
"""

import numpy as np
import os

import rmrio  # See file pyrmrio/rmrio.py  \RMRIO_main_run.py

# %% Change working directory (optional)

if False:  # Change flag to set working directory

    os.chdir("C:/Users/Cillian/WorkingDirectory/")

# %% Load RMRIO class

# The class rmrio.rmrio_import() imports the *.mat files from the folders
# /rmrio-data/Labels_RMRIO/Labels_RMRIO/
# /rmrio-data/Year_YYYY_RMRIO/Year_YYYY_RMRIO/

rmrio_db_importer = rmrio.rmrio_import(
    rmrio_file_path="C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO_EORA_HYBRID/Year_2010_RMRIO/rmrio-data",  # Default: "rmrio-data/"
    rmrio_year=2010  # Default: 2015
)

# %% Import RMRIO database indices

if True:
    RMRIO_IDX = rmrio_db_importer.idx
    RMRIO_IDX_sectors = rmrio_db_importer.sector_idx
    RMRIO_IDX_exensions = rmrio_db_importer.extension_idx
    RMRIO_IDX_final_demand = rmrio_db_importer.y_idx

# %% Import RMRIO database elements

if True:

    # Total output
    #RMRIO_x = rmrio_db_importer.import_x()
    #RMRIO_x.to_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO_EORA_HYBRID/Year_2010_RMRIO/rmrio-data/Parsed_RMRIO_files/x.csv')
    # Final demand
    #RMRIO_Y = rmrio_db_importer.import_Y()
    #RMRIO_Y.to_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO_EORA_HYBRID/Year_2010_RMRIO/rmrio-data/Parsed_RMRIO_files/Y.csv')
    # Extensions (households)
    #RMRIO_ext_hh = rmrio_db_importer.import_extensions_hh()
    #RMRIO_ext_hh.to_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO_EORA_HYBRID/Year_2010_RMRIO/rmrio-data/Parsed_RMRIO_files/ext_hh.csv')
    # Extensions
    #RMRIO_ext = rmrio_db_importer.import_extensions()
    #RMRIO_ext.to_csv('C:/Users/Cillian/PycharmProjects/Master-Thesis/data/Raw/EXIO_EORA_HYBRID/Year_2010_RMRIO/rmrio-data/Parsed_RMRIO_files/ext.csv')
    # Technical coefficients
    RMRIO_A = rmrio_db_importer.import_A()
    # Identity matrix
    #RMRIO_I = np.identity(RMRIO_A.shape[0])

    # Get data heads
    if True:
        head_len = 100

        #RMRIO_x_head = RMRIO_x[:head_len]
        #RMRIO_Y_head = RMRIO_Y.iloc[:head_len, :head_len]
        #RMRIO_ext_hh_head = RMRIO_ext_hh.iloc[:, :head_len]
        #RMRIO_ext_hh_head = RMRIO_ext_hh.iloc[:, :head_len]
        #RMRIO_ext_head = RMRIO_ext.iloc[:, :head_len]
        RMRIO_A_head = RMRIO_A.iloc[:head_len, :head_len]

        del head_len

print(RMRIO_A_head)