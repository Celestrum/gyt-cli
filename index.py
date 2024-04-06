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




# --- CONFIGURATION FILE PARSER ---

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
    "\n": lambda x : print("NL"),
    "\.[a-z]+ > .": lambda x : print("VAR", x),
    "(> |>\t|> )*\?{.*\}": lambda x : print("IF", x),
    # ? {}
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



# --- COMMANDS ---
# gyt register NAME
# gyt list REGISTEREDNAME

"""
Subcommands:
- register #1name
- list [-n <amount>]  #1registeredname  will try to display n repos for the user or all if n is too large. default 10.
- pull #1reponame                       tries to find a repo with the name in it's state and clone it.
- build                                 builds the repo from the current directory looking for a gytc.file
"""

import argparse
import sys
from typing import List
import pickle



parser = argparse.ArgumentParser(
    prog='gyt',
    description='A new age code management tool'
    epilog='We hate to see you go, but we love to watch you leave'
)

parser.add_argument('list', nargs='1', type=str,
    help='10 of the most')

parser.add_argument('--log', default=sys.stdout, type=argparse.FileType('w'),
    help='the file where the logs should be written')
args = parser.parse_args()



def list_repos(username: str):
    url = f"https://github.com/{username}?tab=repositories"
    response = requests.get(url)




def main(args: List[str]):
    args.log.write('%s' % "beginning gyt\n")
    parsed_args = parser.parse_args(args)
    match parsed_args:
        case args.list:
            list_repos(parsed_args.list)
        case _:
            parser.print_help()
            
    args.log.close()

if __name__ == "__main__":
    args = sys.argv[1:]