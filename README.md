# LCA_Analysis
Analysis of Labor Condition Applications from 2014.

This repository contains a series of iPython notebooks outlining the steps I took to prepare and analyze data on United States Labor Condition Applications from 2014. Note that the data files (excel and csv) mentioned in the notebooks are too large to upload here.

### Data Source
This data was sourced from the US Department of Labor's Foreign Labor Certification disclosure data (found <a href="http://www.foreignlaborcert.doleta.gov/performancedata.cfm#dis">here</a>). The specific file is listed as *H1B_FY2014.xls* under the **LCA Programs** table.

### Description of Files in this Repository

* **H1B_FY14_Record_Layout.doc:** From the Department of Labor. Provides information about the source data (column descriptions).

* **LCA Analysis Initial Filtering.ipynb:** iPython notebook covering how I initially filtered and formatted the raw data for analysis. This filtering and cleanup is expanded upon in the next notebook. Takes the raw data and produces "Prepped_LCA.csv".

* **Initial_Filter.py:** Produces "Prepped_LCA.csv" from the raw data. Contains only the required code to perform this operation. A streamlined version of "LCA Analysis Initial Filtering.ipynb" without the exploration.

* **LCA Exploratory Analysis 1.ipynb:** Exploratory analysis focused on wages of LCA submissions. Also performs a second round of formatting (appends some additional data from other sources - see this file for more info). Generates "Delta_LCA.csv" from "Prepped_LCA.csv".

* **Analysis_1.py:** Generates "Delta_LCA.csv" from "Prepped_LCA.csv". This is "LCA Exploratory Analysis 1.ipynb" without the fluff. The file generated here is what's used for the final report.

* **LCA Exploratory Analysis 2.ipynb:** Exploratory analysis focused on applicant density (which companies/industries are submitting the most LCAs, which states are most popular, etc.).

* **LCA Exploratory Analysis 3.ipynb:** Exploratory analysis focused on LCA rejections. This was not included in the final report - see this file for more info.

* **Blank_US_Map.svg:** US map svg used to create choropleths in the final report.

* **Labor Condition Applications Analysis.ipynb:** Final analysis. Contains a write-up of all my findings from exploratory analysis. Note that the actual code in this notebook is hidden for readability purposes (can be unhidden using a button near the top of the report).

* **Labor Condition Applications Analysis.html:** HTML version of the final report.
