import json
import numpy as np
from scipy.stats import shapiro
import os

try:
    # Initialize an empty dictionary to store test results
    test_results = {}

    # Get a list of directories containing JSON files
    directories = ["./cvg_metrics/", "./cvg_for_same_commit/", "./A2A_metrics/"] 
    for directory in directories:
        json_files = [f for f in os.listdir(directory) if f.endswith('.json')]

        for json_file in json_files:
            # Construct the full path to the JSON file
            file_path = os.path.join(directory, json_file)

            # Attempt to open the JSON file
            with open(file_path, 'r') as file:
                json_data = json.load(file)

            values = np.array([float(value) for value in json_data.values()]).reshape(-1, 1)

            statistic, p_value = shapiro(values)

            # Store the test results in the dictionary
            test_results[json_file] = {
                "Test Statistic": statistic,
                "p-value": p_value,
                "Gaussian": p_value < 0.05  # True if p-value < 0.5, indicating data looks Gaussian
            }

    # Save the test results to a JSON file
    with open("shapiro_test_results.json", 'w') as json_file:
        json.dump(test_results, json_file, indent=4)

    print("Test results saved to 'shapiro_test_results.json'.")

except FileNotFoundError:
    # Handle the case where the input directories or files don't exist
    print("Input directories or files not found.")
except Exception as e:
    # Handle other exceptions
    print("An error occurred:", e)
