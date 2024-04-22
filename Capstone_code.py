import pandas as pd
from scipy.stats import mannwhitneyu

# Open the csv file
accidents = pd.read_csv('/Users/sergej/Desktop/Turing/Capstone/US_Accidents_March23.csv')

# Create a list of states of interest
states_of_interest = ['CA', 'TX', 'FL', 'NY', 'PA', 'NC', 'NJ', 'VA', 'TN', 'MN', 'SC', 'AR']

# Filter the period of time and states from the general file
accidents = accidents[(accidents['Start_Time'] >= '2022-01-01') & (accidents['Start_Time'] <= '2022-12-31')]
accidents = accidents[accidents['State'].isin(states_of_interest)]

# Selecting only "State" and "ID" columns
accidents = accidents[["State", "ID"]]

# Group by "State" and count accidents
accidents = accidents.groupby("State").count()

# Add population of the states
accidents['Population'] = [3046404, 39040616, 22245521, 5714300, 10695965, 9260817, 19673200, 12972091, 5282955, 7048976, 30029848, 8679099]

# Iterate over each state
for state in states_of_interest:
    # Select data for the current state
    state_data = accidents.loc[state]

    # Perform A/B testing with other states
    for other_state in states_of_interest:
        if other_state != state:  # Skip comparing with itself
            other_state_data = accidents.loc[other_state]

            # Perform Mann-Whitney U test
            statistic, p_value = mannwhitneyu(state_data['ID'], other_state_data['ID'])

            # Print results
            print(f"A/B testing between {state} and {other_state}:")
            print(f"  - Mann-Whitney U statistic: {statistic}")
            print(f"  - p-value: {p_value}")
            if p_value < 0.05 or p_value > 0.975:
                print("  - Significant difference (p < 0.025 or p > 0.975)")
            else:
                print("  - Not significant difference (0.025 <= p <= 0.975)")
