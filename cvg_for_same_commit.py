import os
import subprocess
import json
from itertools import combinations


def calculate_cvg_metric(folder_path_1, folder_path_2):
    try:
        result = subprocess.run(["java", "-jar", "./assets/jars/arcade_core_Cvg.jar", folder_path_1, folder_path_2], capture_output=True, text=True)
        cvg_metric = result.stdout.strip()
        return cvg_metric.split()
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running Cvg: {e}")
        return []

def get_first_rsf_file_in_subfolder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".rsf"):
                return os.path.join(root, file)
    return None

def list_folders_and_next(folder1, folder2):
    metrics = {}
    
    # Get list of subfolders in folder1 and folder2
    subfolders1 = [f.path for f in os.scandir(folder1) if f.is_dir()]
    subfolders2 = [f.path for f in os.scandir(folder2) if f.is_dir()]

    # Sort subfolders
    subfolders1.sort()
    subfolders2.sort()

    for subfolder1, subfolder2 in zip(subfolders1, subfolders2):
        current_rsf = get_first_rsf_file_in_subfolder(subfolder1)
        next_rsf = get_first_rsf_file_in_subfolder(subfolder2)

        if current_rsf and next_rsf:
            metric = calculate_cvg_metric(current_rsf, next_rsf)
            if metric:
                # Extract folder names from paths
                folder_name1 = os.path.basename(subfolder1)
                folder_name2 = os.path.basename(subfolder2)
                metrics[f"{folder_name1} -- {folder_name2}"] = metric[-1]  # Assuming the metric value is the last element

    return metrics

if __name__ == "__main__":
    folders = {
        "clustering_folders": "./outputs/wca_uemnm_output",
        "pkg_folders": "./outputs/pkg_outputs",
        "acdc_folders": "./outputs/ACDC output",
        "wca_uem_folders": "./outputs/wca_uem_output",
        "limbo_folders": "./outputs/limbo_outputs" 
    }

    folder_combinations = combinations(folders.values(), 2)

    # Create the folder if it doesn't exist
    folder_name = "cvg_for_same_commit"
    os.makedirs(folder_name, exist_ok=True)

    for folder_path_1, folder_path_2 in folder_combinations:
        folder_name_1 = os.path.basename(folder_path_1)
        folder_name_2 = os.path.basename(folder_path_2)

        # Compute metrics between each pair of folders
        metrics = list_folders_and_next(folder_path_1, folder_path_2)

        # Write metrics to JSON file in the created folder
        file_path = os.path.join(folder_name, f"cvg_metric_{folder_name_1}_vs_{folder_name_2}.json")
        with open(file_path, 'w') as file:
            json.dump(metrics, file, indent=4)