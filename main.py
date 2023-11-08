import json
import os
import utilities as utils

# Read the configuration settings
config = utils.read_config()
path_to_initial_file = config.get('path_to_initial_file')
path_to_update_file = config.get('path_to_update_file')
diff_file_directory = config.get('diff_file_directory')

# Define the name of the diff file
diff_file_name = 'diff_file.json'
path_to_diff_file = os.path.join(diff_file_directory, diff_file_name)


def find_new_dependencies(initial_deps, update_deps):
    """
    Identify dependencies in the update JSON that are not present in the initial JSON.
    """
    initial_dep_ids = {(dep['artifactId'], dep['sha1']) for dep in initial_deps}
    new_dependencies = [
        dep for dep in update_deps if (dep['artifactId'], dep['sha1']) not in initial_dep_ids
    ]
    return new_dependencies


def generate_diff_file():
    """
    Generate a diff file that includes the initial file structure with updated dependencies.
    """
    # Read the content of the initial and update files
    with open(path_to_initial_file, 'r') as file:
        initial_json = json.load(file)
    with open(path_to_update_file, 'r') as file:
        update_json = json.load(file)

    # Extract the dependencies list from each file
    initial_deps = initial_json.get('dependencies', [])
    update_deps = update_json.get('dependencies', [])

    # Find new dependencies to be added to the initial structure
    new_deps = find_new_dependencies(initial_deps, update_deps)

    # Update the dependencies list in the initial structure with new dependencies
    if new_deps:
        if 'dependencies' in initial_json:
            initial_json['dependencies'].extend(new_deps)
        else:
            initial_json['dependencies'] = new_deps

    # Write the updated initial structure to the diff file
    with open(path_to_diff_file, 'w') as file:
        json.dump(initial_json, file, indent=4)

    print(f"Diff file created at {path_to_diff_file}")


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
