path = "config.gytc"
DEBUG = True

def print(*args, **kwargs):
    if kwargs.get("debug") and not DEBUG: return
    # Remove debug from kwargs
    if "debug" in kwargs: del kwargs["debug"]
    __builtins__.print(*args, **kwargs)

def stalker_decorator(wrappee):
    def wrapper(*args, **kwargs):
        # print("STALKED:",*args)
        return wrappee(*args, **kwargs)
    return wrapper

@stalker_decorator
def read_config():
    try:
        with open(path, "r") as file:
            data = file.readlines()
            return data
    except:
        print("Error reading config file")

config_data = read_config()

@stalker_decorator
def parse_var(line, *_):
    name, value = line.split(" > ")
    vars[name] = value

def parse_condition(line, depth=0):
    # pattern = ">"*depth + " "*(not not depth) + "\{.*\}"
    pattern = "\{.*\}"

    match = re.search(pattern, line)
    if match:
        result = match.group()
        # Strip the curly braces
        result = result[1:-1]
        # Substitute the variables
        for key in vars: result = result.replace(key, vars[key])
        return eval(result)
    else:
        print("No match found.")

@stalker_decorator
def parse_if(line, index, depth):
    condition = parse_condition(line, depth)
    if condition:
        print("Command is True")
        return begin(start=index+1, end=len(config_data), depth=depth+1)
    else:
        print("Condition is False")
        current_index = index
        while current_index < len(config_data):
            current_line = config_data[current_index]
            if re.match(f"(> *){{{depth-1}}}(> *|< *).*", current_line):
                if re.match(f"(> *){{{depth-1}}}< *", current_line):
                    break
            current_index += 1
        
        return begin(start=current_index-1, end=len(config_data), depth=depth+1)


@stalker_decorator
def parse_command(line, index, depth=0):
    print("Command:", line)
        
arg_binds = {
    "\n": lambda *_ : None,                           # Parse NL 
    "\.[a-z]+ > .": parse_var,                                   # Parse VAR
    "([ ]*|> |>\t|> )*\? {.*\}": parse_if,      # Parse IF
    "(> *|< *).{1,}": parse_command
}



import re

vars = dict()

def begin(start=0,end=0,depth=0):
    y_cursor = start
    print("Entering begin() at depth", depth)
    while y_cursor < end:
        line = config_data[y_cursor].strip()
        if depth > 0:
            correct_depth = re.match(f"(> *){{{depth-1}}}(> *|< *).*", line)
            if not correct_depth: break
            # Strip the match from line
            line = line.lstrip(">")
        print(f"{depth} | y_cursor=", y_cursor, " | ", config_data[y_cursor][:-1] , debug=True)
        for key in arg_binds:
            if re.match(key, line):
                y_cursor = arg_binds[key](line, y_cursor, depth) or y_cursor
                break
        y_cursor += 1
    return y_cursor

try:
    begin(end=len(config_data))
except Exception as e:
    print(e)
    # print("that didnt work")
