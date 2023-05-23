import os
from osbuddy import *

os.chdir("day 7")
root = Directory('/')
cwd = root

def cmd_execute_ls(cwd: Directory, reply: list[str]) -> None:
    # unsafe casting but it's late and I want an answer
    if reply[0] == 'dir':
        cwd.add_directory(reply[1])
    else:
        cwd.add_file(reply[1], int(reply[0]))

def get_root_dir(dir):
    '''recursively search through parents and returns root'''
    root = dir if dir.parent is None else get_root_dir(dir.parent)
    return root

def cmd_execute_cd(cwd: Directory, dir_name: str) -> Directory:
    '''searches for dir_name in current working directory and returns it if there is any, returns parent directory if dir_name = .. or root directory if dir_name = /'''
    if(dir_name == '..'): # get parent directory
        if cwd.parent is None:
            return cwd
        return cwd.parent
    
    if(dir_name == '/'): # get root directory
        return get_root_dir(cwd)

    for dir in cwd.directories: # get child directory
        if dir.name == dir_name:
            return dir
        
    raise IndexError("no directory found with name {0 in directory {1}".format(dir_name, cwd))

is_executing_ls = False
current_line = -1
with open("data.txt", "rt") as fs:
    while fs.readable():
        # read 1 line from fs
        result = fs.readline()
        if result == '': break # EOF

        current_line += 1
        if result.startswith('$'):
            # check if line is a command or reply
            cmd = result[2:-1].split(' ') # remove prefix '$ ' and suffix '\n'
            # print(cmd)
            
            # if current command is ls, start passing result to cmd_execute_ls 
            if cmd[0] == 'ls':
                is_executing_ls = True
            # if current command is cd, execute cmd_execute_cd
            elif cmd[0] == 'cd':
                cwd = cmd_execute_cd(cwd, cmd[1])

        elif is_executing_ls:
            #check if next line starts with '$'
            next_char = fs.read(1)
            
            # pass result to execute_cmd_ls
            reply = result[:-1].split(' ') # remove suffix, split into 2
            # print(reply)
            cmd_execute_ls(cwd, reply)

            # stop executing ls if next line is a command or EOF
            if  next_char == '$' or next_char == '':
                is_executing_ls = False

            if(next_char == ''): # test if at end of file
                pass
            else:
                fs.seek(fs.tell() - 1) # go back 1 char

        else:
            pass
            # raise Exception("unable to parse {0} on line {1}".format(reply, current_line))


# OOP solution attempt: A Directory object contains a list of Directory objects, a list of File objects, a name, a size (sum of File and Directory sizes) and a reference to parent Directory
# a File object contains a name and a size

# part 1: find all directories with a total size of at most 10000

dir_size_list = []
def dump_size(dir: Directory, dir_size_list: list[int]) -> None: # recursive tree stuff
    dir_size_list.append(dir.size)
    for child in dir.directories:
        dump_size(child, dir_size_list)
dump_size(root, dir_size_list)

size_delimiter = 100000
print('sum of directories with size smaller than', size_delimiter, ':', sum(filter(lambda x: x <= size_delimiter, dir_size_list)))

#part 2: find the smallest directory with a size over a minimum limit

total_space = 70000000
free_space = total_space - root.size
required_space = 30000000
space_to_free = required_space - free_space

print('space to free up:', space_to_free)
print("size of smallest directory over", space_to_free, ' : ', sorted(list(filter(lambda x: x >= space_to_free, dir_size_list)))[0])