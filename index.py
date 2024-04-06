# April 6 2024
# Description: CLI

# USAGE:


# gyt REGISTERED_NAME
# -f| --file FILENAME

# gyt pull NAME
# gyt  build NAME
# gyt run NAME

# gyt do NAME

# gyt list

# gyt sys ls
# gyt sys set NAME VALUE


# READ THE config.gytc file
path = "config.gytc"

def read_config():
    try:
        with open(path, "r") as file:
            data = file.readlines()
            return data
    except:
        print("Error reading config file")

config_data = read_config()


arg_binds = {
    "\n": lambda x : print("W", x),
    "\.[a-z]+ > .": lambda x : print(x),
}

import re
def begin():
    y_cursor = 0
    while y_cursor < len(config_data):
        line = config_data[y_cursor]
        # Match via Regex
        for key in arg_binds:
            if re.match(key, line):
                arg_binds[key](line)
        y_cursor += 1

try:
    begin()
except:
    print("that didnt work")