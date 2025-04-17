import os
import json

# Function to find the first .rsf file in a given directory and its subdirectories
def find_rsf_file(root_dir):
    """Find the first .rsf file in a given directory and its subdirectories."""
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".rsf"):
                return os.path.join(root, file)
    return None

# Function to parse clusters from an RSF file
def parse_clusters(rsf_file_path):
    try:
        with open(rsf_file_path, 'r') as file:
            lines = file.readlines()
            cluster_entities = {}
            for line in lines:
                parts = line.split()
                if len(parts) >= 2:
                    entity = parts[0]
                    cluster_name = parts[1]
                    cluster_entities.setdefault(cluster_name, [])
                    cluster_entities[cluster_name].append(entity)
            num_clusters = len(cluster_entities)
            for cluster_name in cluster_entities:
                cluster_entities[cluster_name] = len(cluster_entities[cluster_name])
            return num_clusters, cluster_entities
    except Exception as e:
        print(f"Error reading file {rsf_file_path}: {e}")
        return 0, {}

# Function to analyze clustering results in a directory
def analyze_clustering_results(output_dir):
    clustering_metrics = {}
    for commit_hash_folder in os.listdir(output_dir):
        commit_hash_path = os.path.join(output_dir, commit_hash_folder)
        if os.path.isdir(commit_hash_path):
            clustering_metrics[commit_hash_folder] = {}
            rsf_file_path = find_rsf_file(commit_hash_path)
            if rsf_file_path:
                algorithm_name = os.path.splitext(os.path.basename(rsf_file_path))[0]
                num_clusters, cluster_entities = parse_clusters(rsf_file_path)
                clustering_metrics[commit_hash_folder][algorithm_name] = {"number of clusters": num_clusters, "cluster entities": cluster_entities}
    return clustering_metrics

# Main function
if __name__ == "__main__":
    output_dirs = [
        "./outputs/pkg_outputs",
        "./outputs/ACDC output"
    ]
    folder_name1 = "Cluster_metrics"
    os.makedirs(folder_name1, exist_ok=True)
    for output_dir in output_dirs:
        clustering_metrics = analyze_clustering_results(output_dir)
        file_path = os.path.join(folder_name1, f"clustering_metrics_{os.path.basename(output_dir)}.json")
        with open(file_path, 'w') as json_file:
            json.dump(clustering_metrics, json_file, indent=4)
