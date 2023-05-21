import os
from copy import copy, deepcopy

class Stack:
    def __init__(self, start_list:list[str] = []):
        self.__idx = 0
        self.__stack_list = start_list

    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            return self.__stack_list[self.__idx]
        except IndexError:
            self.__idx = 0
            raise StopIteration
        
    def __repr__(self):
        return str(self.__stack_list)

    def __len__(self):
        return len(self.__stack_list)
    
    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result
    
    def _deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def push(self, val: str) -> None: # adds a value at the end of the list
        self.__stack_list.append(val)

    def push_many(self, val: list[str]) -> None: # adds a value at the end of the list
        self.__stack_list.extend(val)

    def pop(self) -> str: # returns the last value in the list, then removes that value
        val = self.__stack_list[-1]
        del(self.__stack_list[-1])
        return val
    
    def pop_many(self, cnt: int) -> list[str]: # returns the last value in the list, then removes that value
        val = self.__stack_list[-cnt:]
        del(self.__stack_list[-cnt:])
        return val
    
    def get_val(self) -> str:
        if len(self.__stack_list):
            return self.__stack_list[-1]
        return '0'

def create_stack_list(stack_str_list: list[str]) -> list[Stack]:
    # read stack_str_list from bottom up, only keep letters and empty spaces
    str_repr_list = list(stack_str[1::4] for stack_str in stack_str_list[::-1])

    # rotate 2d list, filter empty values, create stacks
    stack_list = list(Stack(list(filter(lambda x: x != ' ', ch_arr))) for ch_arr in zip(*str_repr_list))
    return stack_list

def create_command_list(command_str_list: list[str]) -> list[tuple]: # create a list of tuples with 3 variables: (amount, src, dest)
    command_list = list(tuple(map(int, filter(lambda x: x.isnumeric(), command_str.split(' ')))) for command_str in command_str_list)
    return command_list

os.chdir("day 5")

# load file into list
data_list = []
for str_in in open("data.txt", "rt"):
    result = str_in[:-1]
    data_list.append(result)

stack_str_list = data_list[:8] # grab first couple rows for start values
stack_list = create_stack_list(stack_str_list)
command_str_list = data_list[10:] # grab from 11 onward for commands to execute
command_list = create_command_list(command_str_list)


# the data file consists of a visual representation of the stacks
# total of 9 stacks, largest stack is 8 items

# part 1: the crane can move 1 box at a time, reversing order whenever boxes are moved
stack_list_1 = deepcopy(stack_list) # the Stack object has a list, which is mutable. deepcopy makes sure every parameter of the instance gets copied properly
for cnt, src, dst in command_list:
    # print("moving", cnt, "from", src, "to", dst)
    # print("current stack:", list(map(len, stack_list_1)))

    for i in range(cnt):
        val = stack_list_1[src - 1].pop()
        stack_list_1[dst - 1].push(val)
    
    # print("new stack:    ", list(map(len, stack_list_1)))

print("solution to part 1:", ''.join(stck.get_val() for stck in stack_list_1))

#part 2: crane can now move multiple boxes, keeping order intact when boxes are moved
stack_list_2 = deepcopy(stack_list) # copying objects is a bih
for cnt, src, dst in command_list:
    # print("moving", cnt, "from", src, "to", dst)
    # print("current stack:", stack_list_2)

    val = stack_list_2[src - 1].pop_many(cnt)
    stack_list_2[dst - 1].push_many(val)

    # print("new stack:    ", stack_list_2)

print("solution to part 2:", ''.join(stck.get_val() for stck in stack_list_2))