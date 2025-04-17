import pandas as pd
import ast

# Read the existing Excel file
excel_file_path = 'inputs/commits_for_issues.xlsx'
df = pd.read_excel(excel_file_path)

# Function to determine Architecture Design Decisions
def determine_architecture_decisions(associated_classes):
    # Split the string representation of the list into individual boolean values
    existence_str, property_str, executive_str = associated_classes.strip('[]').split()

    return {
        'Existence': existence_str,
        'Property': property_str,
        'Executive': executive_str
    }

commit_metric = 'inputs/commit_metrics.xlsx'
df2 = pd.read_excel(commit_metric)
df2['ADD'] = df['Associated Classes'].apply(determine_architecture_decisions)
df2['EXISTENCE'] = df2['ADD'].apply(lambda x: x['Existence'])
df2['PROPERTY'] = df2['ADD'].apply(lambda x: x['Property'])
df2['EXECUTIVE'] = df2['ADD'].apply(lambda x: x['Executive'])

# Save the modified DataFrame to the same Excel file named "commit_metrics.xlsx"
output_excel_file_path = 'inputs/commit_metrics.xlsx'
df2.to_excel(output_excel_file_path, index=False)
print("Data saved to 'commit_metrics.xlsx' with a single column 'ADD' containing architecture design decisions.")
