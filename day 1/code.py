import os

os.chdir("day 1")

calories_per_elf = [] # list of elves and their calories
sum_of_calories = 0 # calory sum tracker

for str_in in open("data.txt", "rt"):
    # val = 0 # non-pythonic, can be ignored
    try:
        if(str_in[:-1]): # check if line is empty
            calories = int(str_in[:-1]) # take input, strip \n and convert to int
            # print(val)
            sum_of_calories += calories
        else:
            calories_per_elf.append(sum_of_calories)
            sum_of_calories = 0
    except ValueError:
        print("an issue occured, go fix")

calories_per_elf.sort(reverse=True) # sort elves in descending order
print("encountered calories per elf:", calories_per_elf)

print("highest calory amount:", calories_per_elf[0])

top_calories = 0
for elf in range(3):
    top_calories += calories_per_elf[elf]

print("sum of top 3 elves:", top_calories)