import os
import subprocess
import pandas as pd
import json

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

def list_commit_pairs_and_cvg_metrics(commit_pairs, folders):
    metrics = {}
    for algo, folder_path in folders.items():
        for commit, parent_commits in commit_pairs:
            commit_folder_path = os.path.join(folder_path, commit)

            for parent_commit in parent_commits:
                parent_commit_folder_path = os.path.join(folder_path, parent_commit)

                current_rsf = get_first_rsf_file_in_subfolder(commit_folder_path)
                parent_rsf = get_first_rsf_file_in_subfolder(parent_commit_folder_path)

                if current_rsf and parent_rsf:
                    metric = calculate_cvg_metric(current_rsf, parent_rsf)
                    if metric:
                        metrics[f"{commit} -- {parent_commit}"] = metric[-1]  # Assuming the metric value is the last element
        # Write metrics to JSON file for the current algorithm folder
        file_path = os.path.join("CVG_metrics", f"cvg_metric_{algo}.json")
        with open(file_path, 'w') as file:
            json.dump(metrics, file, indent=4)

if __name__ == "__main__":
    folders = {
        "wca_uemnm": "./outputs/wca_uemnm_output",
        "pkg": "./outputs/pkg_outputs",
        "acdc": "./outputs/ACDC output",
        "wca_uem": "./outputs/wca_uem_output",
        "limbo": "./outputs/limbo_outputs"
    }

    excel_file_path = 'inputs/commits_for_issues.xlsx'
    data = pd.read_excel(excel_file_path, sheet_name=0)
    
    commit_pairs = []
    for index, row in data.iterrows():
        commit_hash = row['Commit Hash']
        parent_commit_hashes = eval(row['Parent Commit Hashes'])  # Convert string representation to list
        commit_pairs.append((commit_hash, parent_commit_hashes))
    
    list_commit_pairs_and_cvg_metrics(commit_pairs, folders)
