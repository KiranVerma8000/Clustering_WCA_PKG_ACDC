import os
import subprocess

class JavaClusterRunner:
    def __init__(self, jar_path, max_memory="14024m", algo="ACDC", language="java",
                 deps_path="", measure="", proj_name="", proj_version="",
                 proj_path="", stop_threshold=50, package_prefix=""):
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

    def run(self):
        command = [
            "java", f"-Xmx{self.max_memory}", "-jar", self.jar_path,
            f"algo={self.algo}", f"language={self.language}", f"deps={self.deps_path}",
            f"measure={self.measure}", f"projname={self.proj_name}",
            f"projversion={self.proj_version}", f"projpath={self.proj_path}",
            f"stopthreshold={self.stop_threshold}", f"packageprefix={self.package_prefix}"
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

def run_acdc(input_directory, output_directory):
    for filename in os.listdir(input_directory):
        if filename.endswith(".rsf"):
            proj_name = os.path.splitext(filename)[0]  # Extract the base name of the file
            rsf_input_path = os.path.join(input_directory, filename)  # Full path to the input RSF file
            rsf_output_path = os.path.join(output_directory, f"{proj_name}_ACDC.rsf")  # Construct the output file path with the modified name
            
            print("Processing:", proj_name)
            print("Input RSF file:", rsf_input_path)
            print("Output RSF file:", rsf_output_path)
            
            command = [
                "java", "-jar", "assets/jars/arcade_core-ACDC.jar",
                rsf_input_path,
                rsf_output_path
            ]
            
            try:
                subprocess.run(command, check=True)  # Execute the command with error checking
                print("Clustering completed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"An error occurred while running ACDC: {e}")

# Usage example
if __name__ == "__main__":
    input_rsf_directory = "C:/DSSE/Hadoop repo/ds4se-group4/outputs/Extracted_dependency/rsf"  # Directory where the RSF files are located
    output_clustering_directory_acdc = "C:/DSSE/Hadoop repo/ds4se-group4/outputs/ACDC output"
    
    for folders in os.listdir(input_rsf_directory):
        input_rsf_file_folder = os.path.join(input_rsf_directory,folders)
        print("jar_directory",input_rsf_file_folder)
        if os.path.exists(input_rsf_file_folder):
            clustering_output_folder = os.path.join(output_clustering_directory_acdc, folders)
            os.makedirs(clustering_output_folder, exist_ok=True)
            run_acdc(input_rsf_file_folder, clustering_output_folder)
