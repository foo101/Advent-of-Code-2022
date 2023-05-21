# goal: '([a-z])(?!.{0,2}\\1) ([a-z])(?!.?\\2) ([a-z])(?!\\3).' for target = 3

def regexgen(target, depth = 0):
    if(target - depth > 2):
        this = ''.join(["([a-z])(?!.{0,", str(target - depth - 2), "}\\\\", str(depth + 1), ")", regexgen(target, depth + 1)])
        return this
    elif(target - depth == 2):
        this = ''.join(["([a-z])(?!.?\\\\", str(depth + 1), ")", regexgen(target, depth + 1)])
        return this
    elif(target - depth == 1):
        this = ''.join(["([a-z])(?!\\\\", str(depth + 1), ")", regexgen(target, depth + 1)])
        return this
    else:
        return '.'
    
# generates regex: test for unique characters
print(regexgen(13))