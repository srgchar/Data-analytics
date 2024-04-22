import pandas as pd
from scipy.stats import chi2_contingency

# Open the csv file
accidents = pd.read_csv('/Users/sergej/Desktop/Turing/Capstone/US_Accidents_March23.csv')

# Create a list of states of interest
states_of_interest = ['CA', 'TX', 'FL', 'NY', 'PA', 'NC', 'NJ', 'VA', 'TN', 'MN', 'SC', 'AZ']

# Filter the period of time and states from the general file
accidents_filtered = accidents[(accidents['Start_Time'] >= '2022-01-01') & (accidents['Start_Time'] <= '2022-12-31')]
accidents_filtered = accidents_filtered[accidents_filtered['State'].isin(states_of_interest)]

# Group by "State" and count accidents
accidents_count = accidents_filtered.groupby("State").size().reset_index(name='number_of_accidents')

# Add population of the states
population_data = {
    'CA': 39040616, 'TX': 39040616, 'FL': 22245521, 'NY': 19673200, 'PA': 12972091,
    'NC': 10695965, 'NJ': 9260817, 'VA': 8679099, 'TN': 7048976, 'MN': 5714300,
    'SC': 5282955, 'AZ': 7365684}

accidents_count['population_data'] = accidents_count['State'].map(population_data)

# Calculate accident rates
accidents_count['accident_rate'] = accidents_count['number_of_accidents'] / accidents_count['population_data']

# Iterate over each pair of states
for i in range(len(states_of_interest)):
    for j in range(i+1, len(states_of_interest)):
        state1 = states_of_interest[i]
        state2 = states_of_interest[j]

        # Extract data for the two states
        data_state1 = accidents_count[accidents_count['State'] == state1][['number_of_accidents', 'population_data']].values.flatten()
        data_state2 = accidents_count[accidents_count['State'] == state2][['number_of_accidents', 'population_data']].values.flatten()

        # Set up the contingency table
        contingency_table = [data_state1, data_state2]

        # Perform chi-square test
        chi2_stat, p_val, dof, expected = chi2_contingency(contingency_table)

        # Show results
        print(f"Chi-square statistic for comparing {state1} and {state2}: {chi2_stat}")
        print(f"P-value: {p_val}")
        if p_val < 0.05:
            print("There is a significant difference in accident rates between states.")
        else:
            print("There is no significant difference in accident rates between states.")
        print()
