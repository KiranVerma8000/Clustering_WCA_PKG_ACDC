import os
import json
import re

# Function to find the first .rsf file in the first subfolder of a given directory that contains .rsf files
def get_first_rsf_file_in_subfolders(folder_path):
    """Find the first .rsf file in the first subfolder of a given directory that contains .rsf files."""
    # List and sort subdirectories in the given folder_path
    subfolders = [os.path.join(folder_path, f) for f in sorted(os.listdir(folder_path)) if os.path.isdir(os.path.join(folder_path, f))]
    
    # Iterate through each subfolder to find .rsf files
    for subfolder in subfolders:
        # Sort files in the current subfolder
        files = sorted(os.listdir(subfolder))
        for file in files:
            if file.endswith(".rsf"):
                # Return the full path to the first .rsf file found
                return os.path.join(subfolder, file)
    
    # Return None if no .rsf files are found in any subfolders
    return None

# Function to parse clustering output files and count entities for each cluster
def parse_clusters(output_file_path):
    try:
        with open(output_file_path, 'r') as file:
            # Read the lines from the RSF file
            lines = file.readlines()
            cluster_entities = {}  # Dictionary to store entities for each cluster
            # Iterate through each line to parse cluster entities
            for line in lines:
                parts = line.split()
                cluster_number = parts[1]
                # Count each entity within its respective cluster
                cluster_entities.setdefault(cluster_number, 0)
                cluster_entities[cluster_number] += 1
                    
            return cluster_entities
    except Exception as e:
        print(f"Error reading file {output_file_path}: {e}")
        return {}

# Function to analyze clustering results
def analyze_clustering_results(clustering_output_dir):
    clustering_metrics = {}
    for commit_hash_folder in os.listdir(clustering_output_dir):
        commit_hash = commit_hash_folder.strip()
        if commit_hash:
            folder_path = os.path.join(clustering_output_dir, commit_hash_folder)
            if os.path.isdir(folder_path):  # Check if it's a directory
                clustering_metrics[commit_hash] = {}
                # Get the path of the first .rsf file in the commit hash folder
                rsf_file_path = get_first_rsf_file_in_subfolders(folder_path)
                if rsf_file_path:
                    algorithm_name = os.path.splitext(os.path.basename(rsf_file_path))[0]  # Extract algorithm name
                    cluster_entities = parse_clusters(rsf_file_path)
                    clustering_metrics[commit_hash][algorithm_name] = {"number of entities": cluster_entities}
    return clustering_metrics

# Main function
if __name__ == "__main__":
    # Define output directories
    output_dirs = [
        "./outputs/wca_uemnm_output",
        "./outputs/wca_uem_output",
        "./outputs/limbo_outputs",
        
    ]
    folder_name1 = "Cluster_metrics"
    os.makedirs(folder_name1, exist_ok= True)
    # Process each output directory
    for output_dir in output_dirs:
        clustering_metrics = analyze_clustering_results(output_dir)
        file_path = os.path.join(folder_name1, f"clustering_metrics_{os.path.basename(output_dir)}.json")
        with open(file_path, 'w') as json_file:
            json.dump(clustering_metrics, json_file, indent=4)
