import os
import shutil
import subprocess

def merge_jars(input_dir, output_file):
    # Create a temporary directory for merging
    temp_dir = os.path.join(input_dir, 'temp')
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # Extract contents of each JAR file into temporary directory
        for root, _, files in os.walk(input_dir):
            for file in files:
                if file.endswith('.jar'):
                    jar_file = os.path.join(root, file)
                    subprocess.run(['jar', 'xf', jar_file], cwd=temp_dir, check=True)

        # Create the merged JAR file
        subprocess.run(['jar', 'cf', output_file, '-C', temp_dir, '.'], check=True)

        print(f"Merged JAR file '{output_file}' created successfully.")

    except Exception as e:
        print(f"Error merging JAR files: {e}")

    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    # Input directory containing folders with JAR files to merge
    input_directory = 'C:/DSSE/Repo/Output directory'

    # Output directory for merged JAR files
    output_directory = 'C:/DSSE/Repo/Merged'

    # Merge JAR files in each folder
    for folder_name in os.listdir(input_directory):
        folder_path = os.path.join(input_directory, folder_name)
        if os.path.isdir(folder_path):
            output_jar_file = os.path.join(output_directory, f"{folder_name}_merged.jar")
            merge_jars(folder_path, output_jar_file)
