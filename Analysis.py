__author__ = 'soroushmehraein'

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

f = open("Cleaned_LCA.csv", "r")

LCA_df = pd.read_csv(f, index_col=0)


"""
print LCA_df.describe()
print LCA_df.dtypes
# need to clean up the column types
"""

LCA_df.TOTAL_WORKERS = LCA_df.TOTAL_WORKERS.astype(int)
LCA_df.LCA_CASE_NAICS_CODE = LCA_df.LCA_CASE_NAICS_CODE.astype(object)
