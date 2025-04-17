import os
import subprocess

def run_pkg(input_directory, output_directory):
    # Define the command to run Pkg
    language = "java"
    filelevel = "false"
    projectname = "common"
    
    for filename in os.listdir(input_directory):
        if filename.endswith(".rsf"):
            proj_name = os.path.splitext(filename)[0]  # Extract the base name of the file
            rsf_input_path = os.path.join(input_directory, filename)  # Full path to the input RSF file
            rsf_output_path = os.path.join(output_directory, proj_name)  # Construct the output file path with the modified name
            
            print("Processing:", proj_name)
            print("Input RSF file:", rsf_input_path)
            print("Output RSF file:", rsf_output_path)
            
            command = [
                   "java", "-jar", "./assets/jars/arcade_core-Pkg.jar",
                   f"depspath={rsf_input_path}",
                   f"projectpath={rsf_output_path}",
                   f"projectname={projectname}",
                   f"projectversion={proj_name}",
                   f"language={language}",
                   f"filelevel={filelevel}"
               ]
            try:
                subprocess.run(command, check=True)  # Execute the command with error checking
                print("Clustering completed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"An error occurred while running ACDC: {e}")
    

if __name__ == "__main__":
    input_rsf_directory = "./outputs/Extracted_dependency/rsf"  # Directory where the RSF files are located
    output_clustering_directory = "./outputs/pkg_outputs"  # Separate output directory for pkg results
    for folders in os.listdir(input_rsf_directory):
        input_rsf_file_folder = os.path.join(input_rsf_directory,folders)
        print("jar_directory",input_rsf_file_folder)
        if os.path.exists(input_rsf_file_folder):
            pkg_output_folder = os.path.join(output_clustering_directory, folders)
            os.makedirs(pkg_output_folder, exist_ok=True)
            run_pkg(input_rsf_file_folder, pkg_output_folder)
