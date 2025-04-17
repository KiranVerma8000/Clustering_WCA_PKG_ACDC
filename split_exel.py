import os
import pandas as pd

# Read the Excel file
excel_file_path = 'inputs/commit_metrics.xlsx'

# Open the Excel file to preserve the first sheet
with pd.ExcelFile(excel_file_path) as xls:
    # Read the first sheet
    first_sheet_df = pd.read_excel(xls)

# Filter rows based on the 'EXISTENCE', 'PROPERTY', and 'EXECUTIVE' columns
existence_true_df = first_sheet_df[first_sheet_df['EXISTENCE'] == True]
property_true_df = first_sheet_df[first_sheet_df['PROPERTY'] == True]
executive_true_df = first_sheet_df[first_sheet_df['EXECUTIVE'] == True]

# Get the directory of the original Excel file
output_dir = os.path.dirname(excel_file_path)

# Create a Pandas Excel writer using xlsxwriter as the engine
output_file_path = os.path.join(output_dir, 'filtered_' + os.path.basename(excel_file_path))
with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
    # Write the first sheet as it is
    first_sheet_df.to_excel(writer, sheet_name='Original_Sheet', index=False)
    
    # Write each filtered DataFrame to a separate sheet
    existence_true_df.to_excel(writer, sheet_name='Existence_True', index=False)
    property_true_df.to_excel(writer, sheet_name='Property_True', index=False)
    executive_true_df.to_excel(writer, sheet_name='Executive_True', index=False)

print(f"Data written to Excel file: {output_file_path}")
