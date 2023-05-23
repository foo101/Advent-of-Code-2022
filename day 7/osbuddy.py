# osbuddy.py module: File and Directory objects, cmd_cd and cmd_ls functions, with some type hinting practice (PEP 483, PEP 484, PEP 526) and docstring practice (PEP 257)

"""
    This module consists of two classes and two functions: Directory and File, and cmd_cd and cmd_ls
    The classes are intended to model an operating system directory tree.
    The functions are intended to model the OS console commands ls and cd
"""

__author__ = 'Hielke Kuipers'
__version__ = "22 May 2023"

from typing import overload # this module uses @overload to type-check some its inputs, and give proper docstring documentation for each supported input

class File:
    def __init__(self, name: str, size: int, parent: 'Directory' = None) -> None:
        self.name: str = name
        self.size: int = size
        self.parent: Directory = parent

    def __repr__(self):
        return self.name

class Directory:
    '''
    simulates an OS directory, with subdirectories, directory name, size and a reference to parent directory   
    '''
    
    def __init__(self, name: str = '', parent: 'Directory' = None) -> None:
        self.name = name
        self.parent = parent

        self.directories: list[Directory] = [] # a list of Directory 
        self.files: list[File] = []

    def __repr__(self):
        return self.name

    @property
    def size(self) -> int:
        '''returns the sum of all subdirectory and file sizes'''
        sub_dir_size = sum([dir.size for dir in self.directories])
        file_size = sum([f.size for f in self.files])
        return sub_dir_size + file_size
    
    @overload # type hinting for add_directory(Directory) -> None
    def add_directory(self, sub_dir: 'Directory') -> None: 
        '''takes a Directory object, sets its parent to this directory and adds it to the directories list'''

    @overload # type hinting for add_directory(str) -> None
    def add_directory(self, name: str = '') -> None: 
        '''creates a new directory and adds it to the directories list'''
    # overloaded methods get overridden by the interpreter during runtime, so these are purely for type-checking
    # Since these get overridden during runtime, stubs are used and the type checking during runtime is done in the full 

    # due to a bug in IntelliSense it only shows the docstring of the first instance of add_directory when hovering over the object's method
    # when calling help(Directory.add_directory), or printing Directory.add_directory.__doc__, it shows the proper docstring

    def add_directory(self, value = '') -> None: 
        '''adds directories to its directories list''' 
        
        if isinstance(value, Directory):
            value.parent = self
            self.directories.append(value)
            return
        
        if isinstance(value, str):
            sub_dir = Directory(value, self)
            self.directories.append(sub_dir)
            return
        
        raise TypeError("value must by of type str or Directory")

    @overload
    def add_file(self, file: File) -> None:
        '''takes a File object, sets its parent to this directory and adds it to the directories list'''

    @overload
    def add_file(self, name: str, size: int = 0) -> None:
        '''creates a new file and adds it to the files list'''

    def add_file(self, value, size = 0):
        '''adds files to its files list'''
        if isinstance(value, File):
            value.parent = self
            self.files.append(value)
            return
        
        if isinstance(value, str):
            self.files.append(File(value, size, self))
            return
        
        raise TypeError("value must by of type str or File")

def cmd_ls(cwd: Directory, expected_directories: list[str], expected_files: list[tuple[str, int]]) -> None:
    '''fills the list of files and directories in current working directory with Directory and File objects based on expected directory and file names
        parameters:
            cwd -> Directory: current working directory, this object gets filled with new files and directories
            expected_directories -> list[str]: a list with names of all expected directories
            expected_files -> list[tuple[str, int]]: a list of tuples with all expected file names and sizes
    '''
    known_dirs = [dir.name for dir in cwd.directories]
    for dir_name in expected_directories:
        if dir_name in known_dirs:
            pass
        cwd.add_directory(dir_name)
    
    known_files = [file.name for file in cwd.files]
    for file_name, file_size in expected_files:
        if(file_name in known_files):
            pass
        cwd.add_file(file_name, file_size)

def __get_root_dir(dir):
    root = dir if dir.parent is None else __get_root_dir(dir.parent)
    return root

def cmd_cd(cwd: Directory, dir_name: str) -> Directory:
    '''searches for dir_name in current working directory and returns it if there is any, returns parent directory if dir_name = .. or root directory if dir_name = /'''
    if(dir_name == '..'): # get parent directory
        if cwd.parent is None:
            return cwd
        return cwd.parent
    
    if(dir_name == '/'): # get root directory
        return __get_root_dir(cwd)

    for dir in cwd.directories: # get child directory
        if dir.name == dir_name:
            return dir
        
    raise IndexError("no directory found with name {0 in directory {1}".format(dir_name, cwd))

if __name__ == '__main__':
    # module testing, gets ignored when imported as module: docstring overloading on type-checked Directory.add_directory(...)
    dir_a = Directory('dir A')
    dir_b = Directory('dir B')
    dir_a.add_directory(dir_b)
    dir_a.add_directory('dir C') # the same function is called with 2 different parameter types, since this function is overloaded it shows the docstring of the specific called function
    dir_a.add_file('a_file.py', 10000)

    print(dir_a)
    print(dir_a.directories)
    print(dir_a.files)
    print(dir_a.size)
    #help(Directory)
    
    