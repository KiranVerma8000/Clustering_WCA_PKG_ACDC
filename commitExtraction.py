from pydriller import Repository
import re
import pandas as pd
import os
import networkx as nx

def extract_issue_ids(commit_message):
    return re.findall(r'HADOOP-\d+', commit_message)


def determine_commits_for_issues(repo_path, issue_ids, issue_classes):
    commits_for_issues = [] 

    for commit in Repository(repo_path).traverse_commits():
        commit_message = commit.msg
        commit_issue_ids = extract_issue_ids(commit_message)

        for issue_id in commit_issue_ids:
            if issue_id in issue_ids:
                parent_hashes = commit.parents
                if not parent_hashes:
                    parent_hashes = [None] 
                issue_data = {
                    'Issue ID': issue_id,
                    'Commit Hash': commit.hash,
                    'Parent Commit Hashes': parent_hashes,
                    'Associated Classes': issue_classes[issue_id],
                    'Commit message': commit.msg,
                    'Modified Files Added': len(commit.modified_files),
                    'Modified Files Deleted': 0 
                }
                commits_for_issues.append(issue_data)

    return commits_for_issues

def extract_code_metrics(file_path):
    lines_of_code = 0
    num_classes = 0
    num_methods = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            in_comment_block = False

            for line in lines:
                line = line.strip()
                if line.startswith("/*"):
                    in_comment_block = True
                if in_comment_block:
                    if "*/" in line:
                        in_comment_block = False
                    continue
                if line.startswith("//"):
                    continue
                if line and not line.startswith(("import ", "package ", "/*", "*/", "//")):
                    lines_of_code += 1

                if line.startswith("class "):
                    num_classes += 1
                elif line.startswith("interface "):
                    num_classes += 1
                elif line.startswith("enum "):
                    num_classes += 1
                elif line.startswith("public class "):
                    num_classes += 1
                elif line.startswith("public interface "):
                    num_classes += 1
                elif line.startswith("public enum "):
                    num_classes += 1
                elif line.startswith("private class "):
                    num_classes += 1
                elif line.startswith("private interface "):
                    num_classes += 1
                elif line.startswith("private enum "):
                    num_classes += 1
                elif line.startswith("public void "):
                    num_methods += 1
                elif line.startswith("private void "):
                    num_methods += 1

    except FileNotFoundError:
        print(f"File not found: {file_path}")

    except UnicodeDecodeError:
        print(f"Error decoding file: {file_path}")

    return lines_of_code, num_classes, num_methods

def calculate_commit_metrics(repo_path, commit_hash):
    metrics = {
        'Commit Hash': commit_hash,
        'Commit Date': None,
        'Lines Added': 0,
        'Lines Deleted': 0,
        'Lines Edited': 0,
        'Classes Added': 0,
        'Classes Deleted': 0,
        'Methods Added': 0,
        'Methods Deleted': 0,
        'DMM Unit Size': 0,
        'DMM Unit Complexity': 0,
        'DMM Unit Interfacing': 0,
        'Complexity': 0,  
        'Parent Commit Hashes': [],  
    }

    for commit in Repository(repo_path).traverse_commits():
        if commit.hash == commit_hash:
            commit_date = commit.committer_date 
            metrics['Commit Date'] = commit_date.strftime("%Y-%m-%d %H:%M:%S") if commit_date else None

            for modified_file in commit.modified_files:
                if modified_file.new_path is not None:  
                    added_lines, deleted_lines = modified_file.added_lines, modified_file.deleted_lines
                    metrics['Lines Added'] += added_lines
                    metrics['Lines Deleted'] += deleted_lines

                    if added_lines > 0 or deleted_lines > 0:
                        new_file_path = os.path.join(repo_path, modified_file.new_path)
                        edited_lines, edited_classes, edited_methods = extract_code_metrics(new_file_path)
                        metrics['Lines Edited'] += edited_lines
                        metrics['Classes Added'] += edited_classes
                        metrics['Methods Added'] += edited_methods

                    if deleted_lines > 0:   
                        old_file_path = os.path.join(repo_path, modified_file.old_path)
                        deleted_classes, deleted_methods = extract_code_metrics(old_file_path)[1:]
                        metrics['Classes Deleted'] += deleted_classes
                        metrics['Methods Deleted'] += deleted_methods

            metrics['DMM Unit Size'] = commit.dmm_unit_size
            metrics['DMM Unit Complexity'] = commit.dmm_unit_complexity
            metrics['DMM Unit Interfacing'] = commit.dmm_unit_interfacing
            
            if commit.modified_files:
                metrics['Complexity'] = modified_file.complexity
            metrics['Parent Commit Hashes'] = commit.parents
            
            return metrics
    return None

excel_file_path = 'assets/Issues_assignment1.xlsx'
data = pd.read_excel(excel_file_path, sheet_name=2)
issue_classes = data.set_index('Key').T.to_dict('list')

repo_path = "D:/hadoop"
issue_ids = list(issue_classes.keys())

commits_for_issues = determine_commits_for_issues(repo_path, issue_ids, issue_classes)

df = pd.DataFrame(commits_for_issues)
df.to_excel('./inputs/commit_metrics.xlsx', index=False)
print("Commits data saved to Excel file.")

commit_metrics_list = []
for commit_data in commits_for_issues:
    commit_hash = commit_data['Commit Hash']
    commit_metrics = calculate_commit_metrics(repo_path, commit_hash)
    if commit_metrics:
        commit_metrics_list.append(commit_metrics)

metrics_df = pd.DataFrame(commit_metrics_list)

metrics_df.to_excel('./inputs/commit_metrics.xlsx', index=False)

print("Commit metrics saved to Excel file.")
