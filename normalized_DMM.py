import json
import numpy as np
from scipy.stats import shapiro
from sklearn.preprocessing import StandardScaler
import os
import pandas as pd

try:
    # Load the Excel file into a DataFrame
    excel_file = "./inputs/commit_metrics.xlsx" 
    commits_list = pd.read_excel(excel_file)

    column_values = commits_list["DMM Unit Interfacing"].values.astype(float).reshape(-1, 1)
    statistic, p_value = shapiro(column_values)
        
    alpha = 0.5
    if p_value > alpha:
            print("Sample looks Gaussian (fail to reject H0)")
    else:
           scaler = StandardScaler()
           column_values_normalized = scaler.fit_transform(column_values)
           column_values_normalized_str = np.where(np.isnan(column_values_normalized), 'NaN', column_values_normalized)
           new_column_name = "Normalized DMM Unit Interfacing"
           commits_list[new_column_name] = column_values_normalized
           

    commits_list.to_excel(excel_file, index=False)
    normalized_data = {index: value[0] for index, value in enumerate(column_values_normalized)}
    normalized_data2 = {key: val[0] for key, val in zip(commits_list["Commit Hash"].values, column_values_normalized)}
    json_file_path = "./DMM normalized data/Normalized DMM Unit Interfacing.json"

    with open(json_file_path, 'w') as json_file:
        json.dump(normalized_data2, json_file, indent=4)       
    print("Normalized Data saved back to:", excel_file)

except FileNotFoundError:
    print("Input Excel file not found.")
except Exception as e:
    print("An error occurred:", e)
