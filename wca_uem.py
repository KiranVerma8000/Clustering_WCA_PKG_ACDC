import subprocess
import os

class JavaClusterRunner:
    def __init__(self, jar_path, max_memory="14024m", algo="WCA", language="java",
                 deps_path="", measure="UEM", proj_name="", proj_version="",
                 proj_path="", stop_threshold=50, package_prefix="",stop="preselected", serial_threshold=12, serial="archsize"):
        
        self.jar_path = jar_path
        self.max_memory = max_memory
        self.algo = algo
        self.language = language
        self.deps_path = deps_path
        self.measure = measure
        self.proj_name = proj_name
        self.proj_version = proj_version
        self.proj_path = proj_path
        self.stop_threshold = stop_threshold
        self.package_prefix = package_prefix
        self.stop = stop
        self.serial_threshold = serial_threshold
        self.serial = serial

    def run(self):
        command = [
            "java", f"-Xmx{self.max_memory}", "-jar", self.jar_path,
            f"algo={self.algo}", f"language={self.language}", f"deps={self.deps_path}",
            f"measure={self.measure}", f"projname={self.proj_name}",
            f"projversion={self.proj_version}", f"projpath={self.proj_path}",
            f"stopthreshold={self.stop_threshold}", f"packageprefix={self.package_prefix}", f"stop={self.stop}", f"serial={self.serial}", f"serialthreshold={self.serial_threshold}"
        ]
        print("Running command:", ' '.join(command))
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                print("Error occurred:", result.stderr)
            else:
                print("Clustering executed successfully.")
        except Exception as e:
            print("An error occurred while executing the Java clustering tool:", str(e))

def process_rsf_files(input_directory, output_directory, cluster_runner_template):
    for filename in os.listdir(input_directory):
        if filename.endswith(".rsf"):
            deps_path = os.path.join(input_directory, filename)
            proj_name = os.path.splitext(filename)[0]  # Assuming project name is the base of the filename
            proj_path = os.path.join(output_directory, proj_name+'.rsf')  # Separate output directory for each project
            os.makedirs(proj_path, exist_ok=True)  # Ensure the output directory exists

            # Create a new runner instance for each RSF file with updated paths and project name
            runner = JavaClusterRunner(
                jar_path=cluster_runner_template.jar_path,
                max_memory=cluster_runner_template.max_memory,
                algo=cluster_runner_template.algo,
                language=cluster_runner_template.language,
                deps_path=deps_path,
                measure=cluster_runner_template.measure,
                proj_name=proj_name,
                proj_version=cluster_runner_template.proj_version,
                proj_path=proj_path,
                stop_threshold=cluster_runner_template.stop_threshold,
                package_prefix=cluster_runner_template.package_prefix
            )
            runner.run()

# Usage example
if __name__ == "__main__":
    input_rsf_directory = "./outputs/Extracted_dependency/rsf"  # Directory where the RSF files are located
    output_clustering_directory = "./outputs/wca_uem_output"  # Separate output directory for clustering results
    cluster_runner_template = JavaClusterRunner(
        jar_path="./assets/jars/arcade_core_clusterer.jar",
        max_memory="10240m",
        algo="WCA",
        language="java",
        measure="UEM",
        proj_version="3.5.0-SNAPSHOT",
        stop_threshold=12.0,
        package_prefix="org.apache.hadoop",
        serial_threshold=12.0,
        serial="archsize",
        stop="preselected"
    )
    for folders in os.listdir(input_rsf_directory):
        input_rsf_file_folder = os.path.join(input_rsf_directory,folders)
        print("jar_directory",input_rsf_file_folder)
        if os.path.exists(input_rsf_file_folder):
            clustering_output_folder = os.path.join(output_clustering_directory, folders)
            os.makedirs(clustering_output_folder, exist_ok=True)
            process_rsf_files(input_rsf_file_folder, clustering_output_folder, cluster_runner_template)
