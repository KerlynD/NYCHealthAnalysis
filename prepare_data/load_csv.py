"""
This file loads the most recent NYC Health Community Survey into the SQLite Database using Pandas & SQLite3.
First the Data will be read, then cleaned for consistency.
No functions since the data is so small.
"""
# Imports
import pandas as pd
import sqlite3

# Load CSV into a Dataframe
nyc_health_survey = pd.read_csv('nyc_survey/New_York_City_Community_Health_Survey_20240823.csv')

# Remove any Null Values
nyc_health_survey_cleaned = nyc_health_survey.dropna()

# Connect the SQLite Database
connection = sqlite3.connect('../nychealthsurvey.sqlite')

# Write the Dataframe to a new table in SQLite
nyc_health_survey_cleaned.to_sql('nyc_health_survey', connection, if_exists='replace', index=False)

# Close Connection
connection.close()