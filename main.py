import json
import os
import time
from datetime import datetime
import utilities as utils

config = utils.read_config()
path_to_initial_file = config.get('path_to_initial_file')
path_to_update_file = config.get('path_to_update_file')
diff_file_directory = config.get('diff_file_directory') or os.getcwd()
today = datetime.now().strftime('%Y%m%d')

update_request_name = config.get('diff_update_request_name') or f'diff_update_request.txt'
update_request_project_name = config.get('diff_update_request_project_name') or f'diff_update_request_{today}'
path_to_diff_file = os.path.join(diff_file_directory, update_request_name)


def find_new_dependencies(initial_deps, update_deps):
    """
    Find the new dependencies that are not in the initial file.
    :param initial_deps:
    :param update_deps:
    :return:
    """
    initial_dep_ids = {(dep.get('artifactId'), dep.get('sha1')) for dep in initial_deps}
    # TODO: 待確認這個判斷機制是否有誤
    new_dependencies = [dep for dep in update_deps if (dep.get('artifactId'), dep.get('sha1')) not in initial_dep_ids]

    return new_dependencies


def generate_diff_file():
    """
    Generate the diff file.
    :return:
    """
    # TODO: 待確認若遇到systemPath路徑出現中文該怎麼處理
    with open(path_to_initial_file, 'r', encoding='cp950', errors='ignore') as file:
        initial_json = json.load(file)
    with open(path_to_update_file, 'r', encoding='cp950', errors='ignore') as file:
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
    initial_json['projects'][0]['coordinates']['artifactId'] = update_request_project_name
    print("projectName: " + initial_json['projects'][0]['coordinates']['artifactId'])
    print("fileName: " + update_request_name)
    with open(path_to_diff_file, 'w') as file:
        file.write(json.dumps(initial_json, indent=4))
    print(f"Diff file generated: {path_to_diff_file}")


def check_files():
    """
    Check if the paths for the initial and update files are valid and if the files exist.
    """
    print("Welcome to Update_request_different!")
    print("This program is made by KXX (MIT License)")
    print("The program will compare the initial file and the update file, and generate a diff file.")
    print("--------------------------------------------------------------")
    print("Checking files...")
    if not os.path.isfile(path_to_initial_file):
        raise FileNotFoundError(f"The initial file path is invalid or the file does not exist: {path_to_initial_file}")
    if not os.path.isfile(path_to_update_file):
        raise FileNotFoundError(f"The update file path is invalid or the file does not exist: {path_to_update_file}")
    if not os.path.isdir(diff_file_directory):
        raise NotADirectoryError(f"The diff file directory does not exist: {diff_file_directory}")


if __name__ == '__main__':
    try:
        check_files()
        generate_diff_file()
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        input("Press Enter to exit.")
