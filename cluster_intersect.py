import json
import matplotlib.pyplot as plt

# Function to load JSON data
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to compute intersection of clusters
def compute_cluster_intersection(data1, data2):
    intersection = {}
    for data in [data1, data2]:
        for commit, algorithms in data.items():
            for algorithm, clusters in algorithms.items():
                cluster_entities = clusters.get("number of entities", {})
                for cluster_id, entities_count in cluster_entities.items():
                    if cluster_id not in intersection:
                        intersection[cluster_id] = {}
                    if commit not in intersection[cluster_id]:
                        intersection[cluster_id][commit] = entities_count
                    else:
                        intersection[cluster_id][commit] += entities_count
    return intersection

# Function to visualize cluster intersection using box plots
def visualize_cluster_intersection_boxplot(intersection):
    for cluster_id, commit_entities in intersection.items():
        entities = list(commit_entities.values())
        plt.figure(figsize=(10, 6))
        plt.boxplot(entities)
        plt.title(f'Box Plot of Cluster {cluster_id} across Commits')
        plt.xlabel('Cluster')
        plt.ylabel('Number of Entities')
        plt.xticks([1], [f'Cluster {cluster_id}'])
        plt.tight_layout()
        plt.show()

# Main function
def main():
    # Load JSON data
    file_path1 = './Cluster_metrics/clustering_metrics_limbo_outputs.json'
    file_path2 = './Cluster_metrics/clustering_metrics_wca_uemnm_output.json'
    data1 = load_json(file_path1)
    data2 = load_json(file_path2)

    # Compute cluster intersection
    intersection = compute_cluster_intersection(data1, data2)

    # Visualize cluster intersection using box plots
    visualize_cluster_intersection_boxplot(intersection)

if __name__ == "__main__":
    main()
