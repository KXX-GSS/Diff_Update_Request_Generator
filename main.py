import json
import os
import time

import utilities as utils


config = utils.read_config()
path_to_initial_file = config.get('path_to_initial_file')
path_to_update_file = config.get('path_to_update_file')
diff_file_directory = config.get('diff_file_directory')


diff_update_request_name = 'diff_update_request.json'
path_to_diff_file = os.path.join(diff_file_directory, diff_update_request_name)


def find_new_dependencies(initial_deps, update_deps):
    """
    Find the new dependencies that are not in the initial file.
    :param initial_deps:
    :param update_deps:
    :return:
    """
    initial_dep_ids = {(dep['artifactId'], dep['sha1']) for dep in initial_deps}
    new_dependencies = [
        dep for dep in update_deps if (dep['artifactId'], dep['sha1']) not in initial_dep_ids
    ]
    return new_dependencies


def generate_diff_file():
    """
    Generate the diff file.
    :return:
    """
    with open(path_to_initial_file, 'r') as file:
        initial_json = json.load(file)
    with open(path_to_update_file, 'r') as file:
        update_json = json.load(file)

    initial_deps = initial_json.get('projects')[0].get('dependencies')
    update_deps = update_json.get('projects')[0].get('dependencies')


    new_deps = find_new_dependencies(initial_deps, update_deps)
    if new_deps:
        if 'dependencies' in initial_json:
            initial_json['projects'][0]['dependencies'].extend(new_deps)
        else:
            initial_json['projects'][0]['dependencies'] = new_deps

    initial_json['timeStamp'] = str(int(time.time() * 1000))

    with open(path_to_diff_file, 'w') as file:
        json.dump(initial_json, file, indent=4)

    print(new_deps)
    print(f"Diff file created at {path_to_diff_file}")


    with open(path_to_diff_file, 'r') as file:
        diff_update_request = json.load(file)
        print(diff_update_request)


def check_files():
    """
    Check if the paths for the initial and update files are valid and if the files exist.
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
