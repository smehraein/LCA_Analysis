__author__ = 'soroushmehraein'

import pandas as pd


# Open file and read to dataframe.
f = open("2014_LCA.xlsx", "r")

print "Reading"  # This takes a while...
raw_df = pd.read_excel(f)
print "Done Reading"
f.close()


# Drop unwanted columns.
unwanted_columns = ["VISA_CLASS", "LCA_CASE_WAGE_RATE_TO", "PW_SOURCE_1", "OTHER_WAGE_SOURCE_1", "YR_SOURCE_PUB_1",
                    "LCA_CASE_WORKLOC2_CITY", "LCA_CASE_WORKLOC2_CITY", "LCA_CASE_WORKLOC2_STATE",
                    "PW_2", "PW_UNIT_2", "PW_SOURCE_2","OTHER_WAGE_SOURCE_2", "YR_SOURCE_PUB_2"]

raw_df = raw_df.drop(unwanted_columns, axis=1)

# Drop na rows.
raw_df = raw_df.dropna()

# Truncate ZIP codes to 5 numbers.
raw_df["LCA_CASE_EMPLOYER_POSTAL_CODE"] = [str(t)[:5] for t in raw_df["LCA_CASE_EMPLOYER_POSTAL_CODE"]]

# Remove formatting from EMPLOYER_NAME column.
raw_df["LCA_CASE_EMPLOYER_NAME"] = raw_df["LCA_CASE_EMPLOYER_NAME"].str.replace(",", "")  # remove ","
raw_df["LCA_CASE_EMPLOYER_NAME"] = raw_df["LCA_CASE_EMPLOYER_NAME"].str.replace(".", "")  # remove "."
raw_df["LCA_CASE_EMPLOYER_NAME"] = raw_df["LCA_CASE_EMPLOYER_NAME"].str.replace(" - ", "-")  # remove whitespace
raw_df["LCA_CASE_EMPLOYER_NAME"] = raw_df["LCA_CASE_EMPLOYER_NAME"].str.replace("  ", " ")  # remove double spaces

# Fix ZIP codes
postcode = "LCA_CASE_EMPLOYER_POSTAL_CODE"

raw_df = raw_df[raw_df[postcode].astype(str).str.isdigit()]  # remove rows with invalid ZIP
raw_df[postcode] = raw_df[postcode].astype(int)  # convert to int
raw_df = raw_df[raw_df[postcode] > 500]  # remove rows with invalid ZIP

# Update status column.
raw_df = raw_df[raw_df.STATUS != "INVALIDATED"]
raw_df = raw_df.replace("REJECTED", "DENIED")

# Remove rows with obvious errors.
raw_df = raw_df[raw_df.PW_1 != 0]
raw_df = raw_df[raw_df.TOTAL_WORKERS != 2013]

# Drop TOTAL_WORKERS column
raw_df = raw_df.drop("TOTAL_WORKERS", axis=1)

# Write to .csv
raw_df.to_csv("Prepped_LCA.csv", encoding="utf-8")