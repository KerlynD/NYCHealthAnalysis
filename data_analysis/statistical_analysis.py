"""
File to query the data from the Database & conduct the statistical analysis on prevalence data
Definitions to remember:
Pearson Correlation Coefficient: is a correlation coefficient that measures linear
correlation between two sets of data.
It is the ratio between the covariance of two variables and the product of their standard deviations;
thus, it is essentially a normalized measurement of the covariance,
such that the result always has a value between −1 and 1.
"""
# Imports
import pandas as pd
import numpy as np
import sqlite3

# Connect to the SQLITE Database
connection = sqlite3.connect('../nychealthsurvey.sqlite')

# Select the Table from the Dataframe & put it in a panda frame
query = "SELECT * FROM nyc_health_survey"
nyc_health_survey = pd.read_sql_query(query, connection)

"""Calculate Mean for each year"""
# Filter the data frame for only the prevalence
nyc_health_survey_filtered = nyc_health_survey[nyc_health_survey.iloc[:, 0].str.contains('Prevalence')]
# Drop the prevalence column & year
column_names = nyc_health_survey_filtered.drop(nyc_health_survey_filtered.columns[[0, 1]], axis=1)
# Mean
column_means = column_names.mean()
#Saving mean results to a new table
column_means.to_sql('nyc_health_survey_means', connection, if_exists='replace', index=True)

"""Calculate Median for each year"""
# Median
column_median = column_names.median()
#Saving median results to a new table
column_median.to_sql('nyc_health_survey_median', connection, if_exists='replace', index=True)

"""Calculate the Mode for each year"""
# Mode
column_mode = column_names.mode()
#Saving mode results to a new table
column_mode.to_sql('nyc_health_survey_mode', connection, if_exists='replace', index=True)

"""Calculate the Standard Deviation for each year"""
# Standard Deviation
column_stddev = column_names.std()
#Saving STDDEV results to a new table
column_stddev.to_sql('nyc_health_survey_stddev', connection, if_exists='replace', index=True)

"""Calculate the Variance for each year"""
# Variance
column_var = column_names.var()
#Saving variance results to a new table
column_var.to_sql('nyc_health_survey_var', connection, if_exists='replace', index=True)

"""Calculate the Correlation"""
# Using Pearson Correlation, find any correlation between no health insurance & other values
correlation_matrix = column_names.corr()
no_health_insurance_corr = correlation_matrix["No Health Insurance"]
# Saving health insurance correlation results to a new table
no_health_insurance_corr.to_sql('health_insurance_correlation', connection, if_exists='replace', index=True)

# Correlation between No Personal Doctor & other values (Mainly care about 'bad' columns, i.e., Smoking, Obesity, etc.)
no_doctor_corr = correlation_matrix["No Personal Doctor"]
# Saving no personal doctor correlation results to new table
no_doctor_corr.to_sql('no_doctor_correlation', connection, if_exists='replace', index=True)

"""Find Patterns of each year within each column"""
# Calculate the differences
pattern_differences = column_names.diff()
# Store the patterns
pattern_differences.to_sql('pattern_differences', connection, if_exists='replace', index=True)