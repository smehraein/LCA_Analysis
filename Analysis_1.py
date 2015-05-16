__author__ = 'soroushmehraein'

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Open file and read to dataframe.
f = open("Prepped_LCA.csv", "r")
LCA_df = pd.read_csv(f, index_col=0)
f.close()

# Fix hourly wages.
for index, row in LCA_df.iterrows():
    if row[20] == "Hour":
        if row[19] > 10000:  # "Hourly" wages greater than $10,000 are probably yearly.
            LCA_df.loc[index, "PW_UNIT_1"] = "Year"
        elif row[19] > 1000:  # Wages greter than $1000, but less than $10,000 are missing a decimal.
            LCA_df.loc[index, "PW_1"] = row[19]/100.

# Filter by certified applications.
certified_LCA_df = LCA_df[LCA_df.STATUS.str.contains("CERTIFIED")][LCA_df["PW_1"] < LCA_df["PW_1"].quantile(.99)]

# Open national and state files and read to dataframes.
f_national = open("National_2014_Wages.xlsx", "r")
f_state = open("State_2014_Wages.xlsx", "r")
national_df = pd.read_excel(f_national, na_values=["*"])  # These datasets use "*" for null values
state_df = pd.read_excel(f_state, na_values=["*", "#"])  # This one also uses "#" for extremely high values

# Filter state and national dataframes to columns I need, then rename columns.
national_columns = ["OCC_CODE", "H_MEAN", "A_MEAN"]
state_columns = ["ST", "OCC_CODE", "H_MEAN", "A_MEAN"]

national_df = national_df[national_columns]
state_df = state_df[state_columns]

national_df.columns = ["SOC_CODE", "NATIONAL_H_MEAN", "NATIONAL_A_MEAN"]
state_df.columns = ["STATE", "SOC_CODE", "STATE_H_MEAN", "STATE_A_MEAN"]

# Create the delta dataframe and initialize delta columns to NaN.
delta_df = pd.merge(certified_LCA_df, national_df, left_on="LCA_CASE_SOC_CODE", right_on="SOC_CODE")
delta_df = pd.merge(delta_df, state_df, left_on=["LCA_CASE_WORKLOC1_STATE", "LCA_CASE_SOC_CODE"],
                 right_on=["STATE", "SOC_CODE"])

delta_df["NATIONAL_DELTA"] = np.nan  # add two columns to fill in
delta_df["STATE_DELTA"] = np.nan

# Calculate deltas.
delta_df["NATIONAL_DELTA"][delta_df["PW_UNIT_1"] == "Hour"] = delta_df["PW_1"]/delta_df["NATIONAL_H_MEAN"] - 1
delta_df["NATIONAL_DELTA"][delta_df["PW_UNIT_1"] == "Year"] = delta_df["PW_1"]/delta_df["NATIONAL_A_MEAN"] - 1
delta_df["STATE_DELTA"][delta_df["PW_UNIT_1"] == "Hour"] = delta_df["PW_1"]/delta_df["STATE_H_MEAN"] - 1
delta_df["STATE_DELTA"][delta_df["PW_UNIT_1"] == "Year"] = delta_df["PW_1"]/delta_df["STATE_A_MEAN"] - 1

# Drop suspicious value (see ipython notebook for context).
delta_df = delta_df[delta_df["NATIONAL_DELTA"] < 3]

# Write to csv.
delta_df.to_csv("Delta_LCA.csv", encoding="utf-8")

