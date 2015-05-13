__author__ = 'soroushmehraein'

import pandas as pd

f = open("Filtered_H1B.csv", "r")

"""
# Let's take a look at what we have.

sample_df = pd.read_csv(f, nrows=10)
print sample_df

Seems ok. Let's look at everything.
"""

full_df = pd.read_csv(f, index_col=0)
# This loads MUCH faster than an xlsx.

print full_df.shape
# Even with STATUS = WITHDRAWN filtered out, we have over half a million rows.
# Plenty to work with!

print full_df.columns

# Out of curiosity, let's see the top employers applying for H1Bs.

grouped_by_employer_df = full_df.groupby("LCA_CASE_EMPLOYER_NAME")

print grouped_by_employer_df.size().order(ascending=False)
# Interesting... the top three companies (by a pretty wide margin) are Indian.
# Does this ranking stay similar if you only count accepted H1Bs?

certified_df = full_df[full_df.STATUS == "CERTIFIED"]

grouped_by_employer_certified_df = certified_df.groupby("LCA_CASE_EMPLOYER_NAME")
print grouped_by_employer_certified_df.size().order(ascending=False)
# Not really. I also wonder how many applications weren't approved in total.

print "No visa for you:", len(full_df) - len(certified_df)
# Nearly 12,000.

# Also, I just noticed something annoying:
# "MIDMICHIGAN MEDICAL CENTER-MIDLAND" and "MIDMICHIGAN MEDICAL CENTER - MIDLAND" are two different employers...
# This data needs more cleaning, it seems.

# So some companies are being counted twice due to punctuation.
# I'm sure there are other inconsistencies, but let's go for the low-hanging fruit for now.
# Best way to deal with this is to remove or replace the most questionable marks.

# So some companies are being counted twice due to punctuation.
# I'm sure there are other inconsistencies, but let's go for the low-hanging fruit for now.
# Best way to deal with this is to remove or replace the most questionable marks.

full_df_cleaned = full_df.replace(",", "", regex=True)
full_df_cleaned["LCA_CASE_EMPLOYER_NAME"] = full_df_cleaned["LCA_CASE_EMPLOYER_NAME"].str.replace(".", "")
full_df_cleaned["LCA_CASE_EMPLOYER_NAME"] = full_df_cleaned["LCA_CASE_EMPLOYER_NAME"].str.replace(" - ", "-")

print full_df_cleaned.describe()

# There's a row listing TOTAL_WORKERS as 2013. That's got to be an error.
full_df_cleaned = full_df_cleaned[full_df_cleaned.TOTAL_WORKERS != 2013]

print full_df_cleaned.isnull().sum()
# Should clear some NaN rows out, at least for employer so we don't worry about indexing over a NaN.
# Furthermore, employer city and state when we have zip code. Let's drop these too.
# The actual address isn't really valuable either. Neither is YR_SOURCE_PUB_1
# LCA_CASE_WAGE_RATE_TO is also pretty sparse so let's also drop that.

cols_to_drop = ["LCA_CASE_WAGE_RATE_TO", "LCA_CASE_EMPLOYER_ADDRESS", "LCA_CASE_EMPLOYER_CITY",
                "LCA_CASE_EMPLOYER_STATE", "YR_SOURCE_PUB_1"]

full_df_cleaned = full_df_cleaned.drop(cols_to_drop, axis=1)


# A lot of the SOC_NAMES are null compared to the SOC_CODE. We can probably fill in the correct values.
soc_null_codes = full_df_cleaned.LCA_CASE_SOC_CODE[full_df_cleaned.LCA_CASE_SOC_NAME.isnull()].unique()

"""
# Let's take a look at which codes have non-null names

for code in soc_null_codes:
    print code, full_df_cleaned.LCA_CASE_SOC_NAME[full_df_cleaned.LCA_CASE_SOC_CODE == code].unique()

# Well I guess all that data is missing.
# Considering how we have half a million data points, we can afford to drop rows with any NAs at this point.
"""

full_df_cleaned = full_df_cleaned.dropna()

print len(full_df_cleaned), full_df_cleaned.dtypes

# I found out later that there are a few rows with statuses other than CERTIFIED or REJECTED.
# I'll remove these now.

full_df_cleaned = full_df_cleaned[full_df_cleaned.STATUS != "INVALIDATED"]
full_df_cleaned = full_df_cleaned[full_df_cleaned.STATUS != "REJECTED"]

# Looks good. Time to write this to another csv.
full_df_cleaned.to_csv("Cleaned_LCA.csv", encoding="utf-8")