import subprocess
import os

class JavaParser:
    def __init__(self, jar_path, input_path, rsf_output_path, fv_output_path, package_prefix):
        self.jar_path = jar_path
        self.input_path = input_path
        self.rsf_output_path = rsf_output_path
        self.fv_output_path = fv_output_path
        self.package_prefix = package_prefix

    def run(self):
        command = [
            "java",
            "-jar",
            self.jar_path,
            self.input_path,
            self.rsf_output_path,
            self.fv_output_path,
            self.package_prefix
        ]
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                print("Error occurred:", result.stderr)
            else:
                print("JavaParser executed successfully. Output:")
                print(result.stdout)
        except Exception as e:
            print("An error occurred while executing JavaParser:", str(e))

def process_directory(directory, java_parser_jar, rsf_output_directory, fv_output_directory, package_prefix):
    for filename in os.listdir(directory):
        if filename.endswith(".jar"):
            input_path = os.path.join(directory, filename)
            base_name = os.path.splitext(filename)[0]
            rsf_output_path = os.path.join(rsf_output_directory, f"{base_name}.rsf")
            fv_output_path = os.path.join(fv_output_directory, f"{base_name}.fv")
            
            parser = JavaParser(
                jar_path=java_parser_jar,
                input_path=input_path,
                rsf_output_path=rsf_output_path,
                fv_output_path=fv_output_path,
                package_prefix=package_prefix
            )
            parser.run()

# Usage example
if __name__ == "__main__":
    jar_directory = "./outputs/commits_jar_files/parent_commit"  # Adjust this to where your JAR files are located
    rsf_output_directory = "./outputs/Extracted_dependency/rsf"  # Adjust for where you want to store RSF files
    fv_output_directory = "./outputs/Extracted_dependency/fv"  # Adjust for where you want to store FV files
    java_parser_jar = "./assets/jars/arcade_core_JavaParser.jar"  # Adjust this to the location of JavaParser
    package_prefix = "org.apache.hadoop"  # Customize as needed
    for folders in os.listdir(jar_directory):
        if folders == '.DS_Store':
            continue 
        jar_filer_folder = os.path.join(jar_directory,folders)
        print("jar_directory",jar_filer_folder)
        if os.path.exists(jar_filer_folder):
            rsf_output_folder = os.path.join(rsf_output_directory, folders)
            fv_output_folder = os.path.join(fv_output_directory, folders)
            os.makedirs(rsf_output_folder, exist_ok=True)
            os.makedirs(fv_output_folder, exist_ok=True)
            process_directory(jar_filer_folder, java_parser_jar, rsf_output_folder, fv_output_folder, package_prefix)
