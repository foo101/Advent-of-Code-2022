import os
import operator
from typing import overload

os.chdir("day 11")

class Monkey:
    @overload
    def __init__(self, id:int, starting_items:list[int], op:str, val:int, test_val:int, if_true:int, if_false:int) -> None: 
        '''a monkey with operation: new = op(old, old)'''
    @overload
    def __init__(self, id:int, starting_items:list[int], op:str, is_input:bool, test_val:int, if_true:int, if_false:int) -> None:
        '''a monkey with operation: new = old(old, val)'''
    def __init__(self, id:int, starting_items:list[int], op:str, val, test_val:int, if_true:int, if_false:int) -> None: 
        '''a monkey with operation: new = old(old, val)'''
        self.id = id
        self.items = starting_items[:] #make a shallow copy of starting_items
        self.test_val = test_val
        
        if type(val) == bool:
            self.grant_worry = self.__worry_factory_bool(op)
        else:
            self.grant_worry = self.__worry_factory_val(op, val)
        self.throw_item = self.__monkey_factory(test_val, if_true, if_false)
        
    # worry factories, returns make_worry function functions
    def __worry_factory_bool(self, op):
        '''takes a worry level and returns '''
        def grant_worry() -> int:
            item_to_worry_about = self.items[0]
            return op(item_to_worry_about, item_to_worry_about)
        return grant_worry

    def __worry_factory_val(self, op, val):
        def grant_worry() -> int:
            '''takes a worry level and returns a new worry level based on '''
            item_to_worry_about = self.items[0]
            return op(item_to_worry_about, val)
        return grant_worry
    
    def __monkey_factory(self, test, if_true, if_false):
        def next_monkey(worry: int) -> tuple[int, int]:
            '''takes a worry level and returns the ID of the next monkey, and the item it throws'''
            item = self.items.pop(0)
            return (worry, if_true) if worry % test == 0 else (worry, if_false)
        return next_monkey
        
# input format
# Monkey 0:
#   Starting items: 79, 98
#   Operation: new = old * 19
#   Test: divisible by 23
#     If true: throw to monkey 2
#     If false: throw to monkey 3
def str_to_monkey(monkey_str: list[str]) -> Monkey:
    id = int(monkey_str[0][7:-1])
    starting_items = list(map(int, monkey_str[1][18:].split(', ')))
    match(monkey_str[2][23]):
        case '+':
            op = operator.add
        case '-': # not in dataset
            op = operator.sub
        case '*':
            op = operator.mul
        case '/': # not in dataset
            op = operator.floordiv
        case _:
            op = None
        
    try: # I can't be bothered to type-check this
        val = int(monkey_str[2][25:])
    except:
        val = True

    test_val = int(monkey_str[3][21:])
    if_true = int(monkey_str[4][29:])
    if_false = int(monkey_str[5][30:])
    print('monkey', id, starting_items, op, val, test_val, if_true, if_false, sep=' - ')
    # no need to keep track of huge worry numbers, strip worry with common product
    return Monkey(id, starting_items, op, val, test_val, if_true, if_false)
    
# monke = Monkey(0, [1, 2, 3, 4], operator.add, True, 3, 1, 2) # monke
# print('monkey ID:', monke.id)

# for i in range(len(monke.items)):
#    worry = monke.grant_worry()
#     print('worry:', worry)
#     next_monkey, item = monke.throw_item(worry)
#     print('next monkey:', next_monkey, 'thrown item:', item)        

# load file into list
# file has the following format:
# Money <id>:int                                        => monkey has id:int
#   Starting items: <*val>:List[int]                    => monkey has items:List[int]
#   Operation: new = old:int <op>:operator <val>:int    => monkey has operation:Lambda op, val = op(old, val)
#   Test: divisible by <val>:int                        => monkey has test:Lambda statement, if_true, if_false = if_true if statement else if_false
#       If true: throw to monkey <id>:int               => monkey has if_true:int
#       If false: throw to monkey <id>:int              => monkey has if_false:int
# Monkey 0:
#   Starting items: 79, 98
#   Operation: new = old * 19
#   Test: divisible by 23
#     If true: throw to monkey 2
#     If false: throw to monkey 3

data_list = []
for str_in in open("data.txt", "rt"):
    result = str_in[:-1]
    data_list.append(result)

monkey_str_list = [data_list[n:n+6] for n in range(0, len(data_list), 7)]
monkey_list = [str_to_monkey(monkey_str) for monkey_str in monkey_str_list]

def let_em_throw(common_product:int) -> list[int]:
    inspected_items_per_monkey = []
    for monkey in monkey_list:
        inspected_items = 0
        for item in range(len(monkey.items)):
            inspected_items += 1
            worry = monkey.grant_worry()
            new_item = worry % common_product # //3 for part 1, causes overflows for part 2 -> % product of test_vals (to keep worry values manageable), uses product to keep common denominators
            thrown_item, monkey_id = monkey.throw_item(new_item) # get monkey id the item is thrown to
            monkey_list[monkey_id].items.append(thrown_item)
        inspected_items_per_monkey.append(inspected_items)
    return inspected_items_per_monkey

for monkey in monkey_list:
    print('monkey {0}:'.format(monkey.id), monkey.items)

# part 1: get the evaluated amount of items per monkey for a total of 20 rounds, then take the top 2 monkeys and multiply their total evaluated items
#part 2: same thing, but for 10000 rounds! worry spirals out of control, use common product to keep your worries down
common_product = 1
for monkey in monkey_list:
    common_product *= monkey.test_val

monkey_list_len = len(monkey_list)
total_inspected_items_per_monkey = [0 for i in range(monkey_list_len)] # populate total_inspected_items
for round in range(1, 10001): # (1, 21) for part 1, (1, 10001) for part 2
    # print('round', i)
    inspected_items_per_monkey = let_em_throw(common_product)
    
    for i in range(monkey_list_len):
        total_inspected_items_per_monkey[i] += inspected_items_per_monkey[i]
    if round % 1000 == 0: # get status every 100 rounds
        print('Round {0}: {1}'.format(round, total_inspected_items_per_monkey))
        # for monkey in monkey_list: # printing these is just slow, also crashes after 300 or so rounds because of worry
        #     print('monkey {0}:'.format(monkey.id), monkey.items)

first, second = sorted(total_inspected_items_per_monkey, reverse=True)[:2]
print('sum of top:', first * second)


