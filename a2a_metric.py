import os
import subprocess
import json
import pandas as pd

def calculate_a2a_metric(folder_path_1, folder_path_2):
    try:
        result = subprocess.run(["java", "-jar", "./assets/jars/arcade_core_A2a.jar", folder_path_1, folder_path_2], capture_output=True, text=True)
        a2a_metric = result.stdout.strip()
        return a2a_metric.split()
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running A2A: {e}")
        return []

def get_first_rsf_file_in_subfolder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".rsf"):
                return os.path.join(root, file)
    return None

def list_commit_pairs_and_a2a_metrics(commit_pairs, folders):
    metrics = {}
    for commit, parent_commits in commit_pairs:
        for algo, folder_path in folders.items():
            commit_folder_path = os.path.join(folder_path, commit)

            for parent_commit in parent_commits:
                parent_commit_folder_path = os.path.join(folder_path, parent_commit)

                current_rsf = get_first_rsf_file_in_subfolder(commit_folder_path)
                parent_rsf = get_first_rsf_file_in_subfolder(parent_commit_folder_path)

                if current_rsf and parent_rsf:
                    metric = calculate_a2a_metric(current_rsf, parent_rsf)
                    if metric:
                        metrics[f"{algo}: {commit} -- {parent_commit}"] = metric[0]  # Assuming the metric value is the first element
    return metrics

if __name__ == "__main__":
    excel_file_path = './inputs/commits_for_issues.xlsx'
    data = pd.read_excel(excel_file_path, sheet_name=0)
    
    commit_pairs = []
    for index, row in data.iterrows():
        commit_hash = row['Commit Hash']
        parent_commit_hashes = eval(row['Parent Commit Hashes'])  # Convert string representation to list
        commit_pairs.append((commit_hash, parent_commit_hashes))
    
    folders = {
        "uca_uemnm": "./outputs/wca_uemnm_output",
        "pkg": "./outputs/pkg_outputs",
        "acdc": "./outputs/ACDC output",
        "wca_uem": "./outputs/wca_uem_output",
        "limbo": "./outputs/limbo_outputs" 
    }

    folder_name1 = "A2A_metrics"
    os.makedirs(folder_name1, exist_ok=True)

    for algo, folder_path in folders.items():
        metrics = list_commit_pairs_and_a2a_metrics(commit_pairs, {algo: folder_path})

        # Write metrics to JSON file in the created folder
        file_path = os.path.join(folder_name1, f"a2a_metric_{algo}.json")
        with open(file_path, 'w') as file:
            json.dump(metrics, file, indent=4)
