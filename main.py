import json
import os
import time
from datetime import datetime
import pandas as pd
import utilities as utils

# Read configuration settings
config = utils.read_config()
path_to_initial_file = config.get('path_to_initial_file')
path_to_update_file = config.get('path_to_update_file')
# Set the directory for the diff file, defaulting to the current working directory
diff_file_directory = config.get('diff_file_directory') or os.getcwd()
today = datetime.now().strftime('%Y%m%d')

# Set the names for the update request and project, with defaults based on the current date
update_request_name = config.get('diff_update_request_name') or 'update-request'
update_request_project_name = config.get('diff_update_request_project_name') or f'diff_update_request_{today}'
path_to_diff_file = os.path.join(diff_file_directory, update_request_name)


def find_dependencies_with_action(deps, action):
    """
    Recursive function to find all dependencies and sub-dependencies with a specific action.
    """
    all_deps = []
    for dep in deps:
        if dep.get('action') == action:
            all_deps.append(dep)
        children = dep.get('children', [])
        all_deps.extend(find_dependencies_with_action(children, action))
    return all_deps


def find_new_or_updated_dependencies(initial_deps, update_deps):
    """
    Find new or updated dependencies and label them as 'Added' or 'Change Version'.
    """
    initial_dep_dict = {(dep.get('artifactId'), dep.get('groupId')): dep for dep in initial_deps}
    update_dep_dict = {(dep.get('artifactId'), dep.get('groupId')): dep for dep in update_deps}

    # Process direct dependencies
    for dep_key, dep in update_dep_dict.items():
        if dep_key not in initial_dep_dict:
            dep['action'] = 'Added'
        elif dep.get('version') != initial_dep_dict[dep_key].get('version'):
            dep['action'] = 'Change Version'

    # Find all new or updated dependencies including sub-dependencies
    new_or_updated_deps = find_dependencies_with_action(update_deps, 'Added') + \
                          find_dependencies_with_action(update_deps, 'Change Version')

    return new_or_updated_deps, len(initial_deps), len(update_deps)


def generate_diff_file():
    """
    Generate a diff file (in .txt format) based on the initial file, updating only the dependencies,
    file name, timestamp, and preserving specific fields from the update file.
    """
    with open(os.path.normpath(path_to_initial_file), 'r', encoding='utf-8', errors='ignore') as file:
        initial_json = json.load(file)

    with open(os.path.normpath(path_to_update_file), 'r', encoding='utf-8', errors='ignore') as file:
        update_json = json.load(file)

    # Find new or updated dependencies
    initial_deps = initial_json.get('projects')[0].get('dependencies', [])
    update_deps = update_json.get('projects')[0].get('dependencies', [])

    new_or_updated_deps, initial_deps_count, update_deps_count = find_new_or_updated_dependencies(initial_deps,
                                                                                                  update_deps)

    # Create a copy of the initial JSON to avoid modifying it directly
    updated_json = initial_json.copy()

    # Update dependencies in the copy
    updated_json['projects'][0]['dependencies'] = new_or_updated_deps

    # Update the timestamp and file name
    updated_json['timeStamp'] = str(int(time.time() * 1000))
    updated_json['projects'][0]['coordinates']['artifactId'] = update_request_project_name

    # Writing the updated JSON to the diff file
    with open(path_to_diff_file + '.txt', 'w', encoding="utf8") as file:
        file.write(json.dumps(updated_json, indent=4))
    print(f"Diff file generated: {path_to_diff_file}.txt")

    return initial_deps_count, update_deps_count


def generate_excel_report():
    """
    Generate an Excel report for the new or updated dependencies with 'Action' information.
    """
    with open(path_to_diff_file + '.txt', 'r', encoding="utf8") as file:
        diff_json = json.load(file)

    new_or_updated_deps = diff_json['projects'][0]['dependencies']

    excel_data = [{'artifactId': dep.get('artifactId'), 'groupId': dep.get('groupId'), 'version': dep.get('version'),
                   'action': dep.get('action')}
                  for dep in new_or_updated_deps]
    df = pd.DataFrame(excel_data)
    excel_path = os.path.join(diff_file_directory, 'dependency_changes.xlsx')
    df.to_excel(excel_path, index=False)
    print(f"Excel report generated: {excel_path}")


def check_files():
    """
    Check if the paths for the initial and update files are valid and if the files exist.
    This function raises FileNotFoundError if paths are invalid or files do not exist.
    """
    if not os.path.isfile(path_to_initial_file):
        raise FileNotFoundError(f"The initial file path is invalid or the file does not exist: {path_to_initial_file}")
    if not os.path.isfile(path_to_update_file):
        raise FileNotFoundError(f"The update file path is invalid or the file does not exist: {path_to_update_file}")
    if not os.path.isdir(diff_file_directory):
        raise NotADirectoryError(f"The diff file directory does not exist: {diff_file_directory}")


if __name__ == '__main__':
    check_files()  # Check if the files exist
    initial_count, update_count = generate_diff_file()  # Generate diff file and get library counts
    generate_excel_report()  # Generate Excel report

    # Report the change in dependencies count
    print(f"Initial dependencies count: {initial_count}")
    print(f"Updated dependencies count: {update_count}")
    if initial_count != update_count:
        print(f"Dependencies count changed. Difference: {update_count - initial_count}")
    else:
        print("No change in dependencies count.")
