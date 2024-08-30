"""
File name: predictive_model.py
Author: <Kerlyn>
About:
File to create predictive model, specifically with a linear regression model. Will predict how numbers will grow
from 2021-2030 (2020 data is what we have).
"""

# Imports
import pandas as pd
import numpy as np
import sqlite3
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Connect to the SQLITE Database
connection = sqlite3.connect('../nychealthsurvey.sqlite')

# Select the Table from the Dataframe & put it in a panda frame
query = "SELECT * FROM nyc_health_survey"
nyc_health_survey = pd.read_sql_query(query, connection)

# Filter the data frame for only the prevalence
nyc_health_survey_filtered = nyc_health_survey[nyc_health_survey.iloc[:, 0].str.contains('Prevalence')]
# iloc (index location) all rows, only the first column that contains 'Prevalence'

# Drop the prevalence column
nyc_data_filtered = nyc_health_survey_filtered.drop(nyc_health_survey_filtered.columns[[0]], axis=1)

# Convert Year column to datetime dtype
nyc_data_filtered['Year'] = pd.to_datetime(nyc_data_filtered['Year'], format='%Y')
nyc_data_filtered.set_index('Year', inplace=True)

# Split the Data into a training set
train_data = nyc_data_filtered[:2020]

# Independent & Dependant variables
X = train_data.index.year.values.reshape(-1, 1) # Independent Variable (years)
y = train_data.values # Dependant Values (columns)

# Train model for each column
model_dict = {}
for i, column in enumerate(train_data.columns):
    # For loop to train the model on each column in the train data set
    model = LinearRegression() # Model
    model.fit(X, y[:, i]) # Once for our independent, i for all columns
    model_dict[column] = model # Place the data in our dict

# Create Future Years
future_years = np.arange(2021, 2030).reshape(-1, 1) # Numpy 1d array

# Predictions for each column using trained model
future_predictions = {}
for column, model in model_dict.items():
    # Adds the prediction of each year to the columns of the dict
    future_predictions[column]= model.predict(future_years)

# Create Dataframe of predictions
predictions_df = pd.DataFrame(future_predictions, index=future_years.flatten())
predictions_df.index.name = 'Year'
predictions_df.to_sql('nyc_health_survey_predictions', connection, if_exists='replace', index=True)

# Plot to visualize trends (Not very good)
#predictions_df.plot(kind='line', marker='o', figsize=(10,6))
#plt.title('NYC Health Survey Predictions 2021-2029')
#plt.xlabel('Year')
#plt.ylabel('Values')
#plt.grid(True)
#plt.legend(loc='lower right')
#plt.show()