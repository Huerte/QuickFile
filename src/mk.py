from pathlib import Path
import json
import sys
import os

CURRENT_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = CURRENT_SCRIPT_PATH + "config.json"

def create_file(prename='hello', file_extension='txt'):
    count = 1

    file_name = Path(f"{prename}{count}" + '.' + file_extension)
    while file_name.exists():
        file_prename = f"{prename}{count}"
        file_name = Path(file_prename + '.' + file_extension)
        count += 1

    file_name.touch(exist_ok=True)


def generate_file(filename, config):
    if not filename:
        return False
    
    if '.' not in filename:
        create_file(prename=config.get('prename', 'file'), file_extension=filename)
    else:
        file_name, extension = filename.split('.')
        create_file(prename=file_name, file_extension=extension)
    return True


def read_config():
    with open(CONFIG_PATH, 'r') as file:
        content = json.load(file)

    return content


def initiate_config():

    if not Path(CONFIG_PATH).exists():

        DEFAULT_CONFIG = {
            "prename": "file"
        }

        with open(CONFIG_PATH, 'a') as file:
            json.dump(DEFAULT_CONFIG, file, indent=4)

        return DEFAULT_CONFIG

    return read_config()


if __name__ == '__main__':

    CONFIG = initiate_config()

    if len(sys.argv) < 2:
        print('Invalid arguments!!!')
        sys.exit(1)

    arguments = sys.argv[1:]

    if len(arguments) > 2:
        print('Invalid arguments!!!')
        sys.exit(1)
    
    if len(arguments) == 1:
        generate_file(filename=arguments[0], config=CONFIG)
    else: 
        if arguments[0] == '-s':
            VALID_CONFIG_VAR = ["prename"]
            VALID_SET = {
                'prename': type('str')
            }
            config_set = arguments[1].split('=')
            if config_set[0] in VALID_CONFIG_VAR:
                # ISSUE: Value Type Misconfiguration
                if type(config_set[1]) != VALID_SET[config_set[0]]:
                    print('The value had invalid variable type!!!')
                    sys.exit(1)

                CONFIG[config_set[0]] = config_set[1]

                with open(CONFIG_PATH, 'w') as file:
                    json.dump(CONFIG, file, indent=4)

            else:
                print('Invalid configuration variable!!!')
                sys.exit(1)

        elif arguments[1].isdigit() and int(arguments[1]) > 0:

            for _ in range(int(arguments[1])):
                generate_file(filename=arguments[0], config=CONFIG)
        
        else:
            print('Invalid arguments!!!')
            sys.exit(1)

