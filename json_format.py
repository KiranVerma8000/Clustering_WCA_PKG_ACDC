import os
import json

# Function to replace NaN values with "NaN" in a JSON object
def replace_nan(json_data):
    for key, value in json_data.items():
        if isinstance(value, float) and value != value:
            json_data[key] = "NaN"
    return json_data

# Function to process JSON files in a directory
def process_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            with open(file_path, "r") as file:
                json_data = json.load(file)
            json_data = replace_nan(json_data)
            with open(file_path, "w") as file:
                json.dump(json_data, file, indent=4)

# Replace NaN values in JSON files in all three directories
directories = ["./Normalized_data_A2A_metrics", "./Normalized_data_cvg_for_same_commit", "./Normalized_data_cvg_metrics"]
for directory in directories:
    process_directory(directory)
