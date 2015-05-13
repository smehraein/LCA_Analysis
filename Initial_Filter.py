__author__ = 'soroushmehraein'

import pandas as pd

# Massive amount of data here. Need to filter out stuff ASAP for usability.
# Also convert to CSV for easier access. Need "utf-8" encoding, however.
# Room for improvement with Hadoop to use multiple year's worth of data?

f = open("2014_H1B.xlsx", "r")

print "reading"
raw_df = pd.read_excel(f)

f.close()

"""
From looking at the raw data and my own intuition, I assume that the following columns are not needed:
"VISA_CLASS" - These are all H1B
"OTHER_WAGE_SOURCE_1" - Wage info source
"LCA_CASE_WORKLOC2_CITY" - 2nd location info is generally very sparse. Will ignore.
"LCA_CASE_WORKLOC2_STATE"
"PW_2"
"PW_UNIT_2"
"PW_SOURCE_2"
"OTHER_WAGE_SOURCE_2"
"YR_SOURCE_PUB_2"

"""
unwanted_columns = ["VISA_CLASS", "OTHER_WAGE_SOURCE_1", "LCA_CASE_WORKLOC2_CITY", "LCA_CASE_WORKLOC2_CITY",
                    "LCA_CASE_WORKLOC2_STATE", "PW_2", "PW_UNIT_2", "PW_SOURCE_2", "OTHER_WAGE_SOURCE_2",
                    "YR_SOURCE_PUB_2"]

raw_df = raw_df.drop(unwanted_columns, axis=1)

# Furthermore, let's remove rows with STATUS = WITHDRAWN.
# These rows provide no useful classification data.

raw_df = raw_df[raw_df.STATUS != "WITHDRAWN"]


# On the flip-side, STATUS = CERTIFIED-WITHDRAWN is just as useful as CERTIFIED

raw_df = raw_df.replace("CERTIFIED-WITHDRAWN", "CERTIFIED")

print "Writing"
raw_df.to_csv("Filtered_H1B.csv", encoding="utf-8")