import os

os.chdir("day 10")

class cathode_cpu:
    def __init__(self, instruction_list: list[str]):
        self.__instruction_list = instruction_list
        self.instruction_ptr: int = 0
        self.__instruction = iter(())
        self.__x: int = 1

    def __iter__(self):
        return self
    
    def __next__(self):
        return self.next()

    # noop takes 1 cycle to run -> yields 1 value
    def __noop(self):
        yield self.__x

    # addx takes 2 cycles to run -> yields 2 values
    def __addx(self, x):
        yield self.__x
        yield self.__x
        self.__x += x

    def __eval_op(self, op_str: str):
        op = op_str.split(' ')
        if op[0] == 'noop':
            return self.__noop()
        if op[0] == 'addx':
            return self.__addx(int(op[1]))
        raise ValueError('{0} is not a valid operation'.format(op_str))

    def next(self):
        try:
            return self.__instruction.__next__()
        except StopIteration:
            # attempt to load next instruction, if it fails: stop iterating
            try:
                instruction_str = self.__instruction_list[self.instruction_ptr]
                self.__instruction = self.__eval_op(instruction_str)
                self.instruction_ptr += 1

                return self.next()
            except IndexError:
                raise StopIteration()


# load file into list
instruction_list = []
for str_in in open("data.txt", "rt"):
    result = str_in[:-1]
    instruction_list.append(result)

# part 1: combine values of CPU cycle 20, 60, 100, 140, 180, 220 (or cycle % 40 = 20)

cpu = cathode_cpu(instruction_list)

sum = 0
for cycle, x in enumerate(cpu, start = 1):
    sig_strength = cycle * x
    print(cycle, x, sig_strength)
    if cycle % 40 == 20:
        sum += sig_strength

print('sum: ', sum)

#part 2: draw a sprite with crt based on x value and cycle
# sprite is 3 pixels wide, x register sets the middle of the sprite..?
# each cycle, crt draws 1 pixel
# screen size is 40 x 6 pixels (240 total cycles)

cpu = cathode_cpu(instruction_list)

# returns pixel to draw
def pix_to_draw(pix_x, x):
    # if x - pix_x is within range of drawing the sprite (sprite is 3 pixels centered on x):
    dx = x - pix_x
    sprite = {-1:'#', 0:'#', 1:'#'}
    if dx in sprite:
        return sprite[dx]
    return '.'

# bad crt test code
for cycle, x in enumerate(cpu, start = 1):
    pix_x = (cycle - 1) % 40 # x position of current pixel being drawn
    if (cycle % 40 > 0):
       print(pix_to_draw(pix_x, x), end = '')
    else: # if end of line
        print(pix_to_draw(pix_x, x))

    #print(cycle, pix_x, x, pix_to_draw(pix_x, x))

#print("something something answer to problem")