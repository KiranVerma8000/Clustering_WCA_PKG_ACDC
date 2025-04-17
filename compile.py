import os
import subprocess
import pandas as pd
import shutil
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='generate-jar.log',
                    filemode='w')

logger = logging.getLogger()

projects= ['hadoop-common']

def checkout_commit(repo_path, commit_hash):
    os.chdir(repo_path)
    subprocess.run(['git', 'checkout', '--force', commit_hash], capture_output=True, text=True, check=True, timeout=60*10)
    print(f"Checked out {commit_hash}")

def copy_jar_files(repo_path, target_dir,commit_hash):
    try: 
        os.chdir(target_dir)
        output_dir = f"{commit_hash}"
        os.makedirs(output_dir, exist_ok=True)
        repo_path = os.path.join(repo_path,"hadoop-common-project","hadoop-common")
       
        for root, dirs, files in os.walk(repo_path):
            
            if 'target' in dirs:
                target_dir_path = os.path.join(root, 'target')
                print("target_dir_path",target_dir_path)
                
                for filename in os.listdir(target_dir_path):
                
                    if "test" not in filename and ".jar" in filename:
                        jar_file_path = os.path.join(target_dir_path, filename)
                        dest_file_path = os.path.join(output_dir, filename)              
                        try:
                            shutil.copy(jar_file_path, dest_file_path)
                            print(f"Copied {filename} to {target_dir}")
                        except FileNotFoundError:
                            print(f"Error: File '{filename}' not found.")
                        except Exception as e:
                            print(f"Error copying file: {e}")
    except Exception as e:
        raise RuntimeError(f"Error copying JAR files: {e}")

def compile_and_export_jar(repo_path):
                output = 0
                for i in projects:
                    project_path = repo_path
                    project_path=os.path.join(repo_path)
                    os.chdir(project_path)
                    print("project:",project_path)
                    try:
                        result = subprocess.run(['mvn', 'clean','package','-U', '--projects',':hadoop-common','--also-make', '-DskipTests'],
                                                   capture_output=True, text=True, check=True, timeout=60*2)
                        print("Maven build succeeded:", result)
                        output = output + 1
                        continue
                    except subprocess.CalledProcessError as e:
                                print("Maven build failed with error:", e.stderr)
                                error_message = e.stderr if e.stderr else e.stdout
                                logger.info('Error in generating jar for subproject: ' + i)
                                logger.error(error_message[-4000:])
                                continue
                    except subprocess.TimeoutExpired:
                                print("Maven build timed out.")
                                continue
                    except Exception as ex:
                                print("An unexpected error occurred during Maven build:", ex)
                                continue
                return output


def process_commits(repo_path, excel_file,target_dir ):
     commits_list = pd.read_excel(excel_file)
     commits_list.sort_values(by="Commit Date", inplace=True)
     i = 1
     for index, row in commits_list.iterrows():
            commit_string = row["Parent Commit Hashes"]
            commit_hash = commit_string.strip("[]'")
            print("commit_hash ",i," :::::",commit_hash,)
            i = i +1
            try:
                checkout_commit(repo_path,commit_hash)
                result = compile_and_export_jar(repo_path)
                print("before copy jar result",result)
                if result != 0:
                    copy_jar_files(repo_path, target_dir,commit_hash) 
            except Exception as e: 
                print(f"Error processing commit {commit_hash}: {e}")
                continue 

                        

if __name__ == "__main__":
    repo_path = "/home/gautam/GautamDev/DS4SE/hadooprepo/hadoop"
    target_dir = "/home/gautam/GautamDev/DS4SE/ds4se-group4/outputs/commits_jar_files/parent_commit"
    excel_file = "/home/gautam/GautamDev/DS4SE/ds4se-group4/inputs/commit_metrics.xlsx"
    process_commits(repo_path,excel_file,target_dir)
