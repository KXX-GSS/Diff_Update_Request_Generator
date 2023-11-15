import sys
from os.path import exists
import yaml
from yaml import SafeLoader



def config_file_generator():
    """Generate the template of config file"""
    with open('config.yml', 'w', encoding="utf8") as f:
        f.write("""# ++--------------------------------++
# | Update_request_different         |
# | Made by KXX (MIT License)        |
# ++--------------------------------++

# The path to the initial file
# default: The current directory
path_to_initial_file : ''

# The path to the update file
# default: The current directory
path_to_update_file : ''

# The path to the directory where the diff file will be saved
# default: The current directory
diff_file_directory : ''

# The name of the diff file
# default: diff_update_request_name
diff_update_request_name : ''

#-------------------------------------


"""
                )
    sys.exit()


def read_config():
    """Read the config file.
    Check if the config file exists, if not, create one.
    If it exists, read the config file and return the configuration as a dictionary.
    :rtype: dict
    """
    if not exists('./config.yml'):
        print("Config file not found, creating one by default.\nPlease finish filling config.yml")
        config_file_generator()

    try:
        with open('config.yml', 'r', encoding="utf8") as f:
            data = yaml.load(f, Loader=SafeLoader)
            config = {
                'path_to_initial_file': data['path_to_initial_file'],
                'path_to_update_file': data['path_to_update_file'],
                'diff_file_directory': data['diff_file_directory'],
                'diff_update_request_name': data['diff_update_request_name']
            }
            return config
    except (KeyError, TypeError):
        print(
            "An error occurred while reading config.yml. Please check if the file is correctly filled.\n"
            "If the problem can't be solved, consider deleting config.yml and restarting the program.\n")
        sys.exit()
