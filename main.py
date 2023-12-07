import json
import os
import time
from datetime import datetime
import utilities as utils

# Read configuration settings
config = utils.read_config()
path_to_initial_file = config.get('path_to_initial_file')
path_to_update_file = config.get('path_to_update_file')
# Set the directory for the diff file, defaulting to the current working directory
diff_file_directory = config.get('diff_file_directory') or os.getcwd()
today = datetime.now().strftime('%Y%m%d')

# Set the names for the update request and project, with defaults based on the current date
update_request_name = config.get('diff_update_request_name') or 'update_request'
update_request_project_name = config.get('diff_update_request_project_name') or f'diff_update_request_{today}'
path_to_diff_file = os.path.join(diff_file_directory, update_request_name)


def find_new_dependencies(initial_deps, update_deps):
    """
    Find new dependencies that are present in the update_deps but not in the initial_deps.

    :param initial_deps: A list of dependency dictionaries from the initial file.
    :param update_deps: A list of dependency dictionaries from the update file.
    :return: A list of new dependencies found only in update_deps.
    """
    initial_dep_ids = {(dep.get('artifactId'), dep.get('sha1')) for dep in initial_deps}
    new_dependencies = [dep for dep in update_deps if (dep.get('artifactId'), dep.get('sha1')) not in initial_dep_ids]
    return new_dependencies


def generate_diff_file():
    """
    Generate a diff file that contains the dependencies found in the update file but not in the initial file.
    """
    with open(os.path.normpath(path_to_initial_file), 'r', encoding='utf-8', errors='ignore') as file:
        initial_json = json.load(file)

    with open(os.path.normpath(path_to_update_file), 'r', encoding='utf-8', errors='ignore') as file:
        update_json = json.load(file)

    initial_deps = initial_json.get('projects')[0].get('dependencies', [])
    update_deps = update_json.get('projects')[0].get('dependencies', [])

    new_deps = find_new_dependencies(initial_deps, update_deps)
    if new_deps:
        initial_json['projects'][0]['dependencies'] = new_deps

    initial_json['timeStamp'] = str(int(time.time() * 1000))
    initial_json['projects'][0]['coordinates']['artifactId'] = update_request_project_name

    with open(path_to_diff_file + '.txt', 'w', encoding="utf8") as file:
        file.write(json.dumps(initial_json, indent=4))
    print(f"Diff file generated: {path_to_diff_file}.txt")


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
    check_files()
    generate_diff_file()
