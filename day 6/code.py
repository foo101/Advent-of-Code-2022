import os

import re

#gloriously stupid regex: match first letter [a-z], second leter is not first letter. second letter [a-z], third letter is not first or 2nd letter etc
marker_finder = "([a-z])(?!.{0,2}\\1)([a-z])(?!.?\\2)([a-z])(?!\\3)."
message_marker_finder = "([a-z])(?!.{0,11}\\1)([a-z])(?!.{0,10}\\2)([a-z])(?!.{0,9}\\3)([a-z])(?!.{0,8}\\4)([a-z])(?!.{0,7}\\5)([a-z])(?!.{0,6}\\6)([a-z])(?!.{0,5}\\7)([a-z])(?!.{0,4}\\8)([a-z])(?!.{0,3}\\9)([a-z])(?!.{0,2}\\10)([a-z])(?!.{0,1}\\11)([a-z])(?!.?\\12)([a-z])(?!\\13)."
# can't be arsed, works well enough

def find_marker(stream: str, index: int = 0, marker_len:int = 4) -> int:
    stream_len = len(stream)
    mat = re.search(marker_finder, stream)
    index = mat.end()
    return index

def find_message_marker(stream: str, index: int = 0, marker_len:int = 4) -> int:
    stream_len = len(stream)
    mat = re.search(message_marker_finder, stream)
    index = mat.end()
    return index

os.chdir("day 6")

# load file into list
datastream = []
for str_in in open("data.txt", "rt"):
    result = str_in[:-1]
    datastream = result

# part 1: searching for a start-of-packet marker; four consecutive unique characters
index = find_marker(datastream)
print("The index of of the marker is:", index, str(datastream[index-4:index]))

#part 2: searching for start-of-message marker; same thingbut with 14 characters
index = find_message_marker(datastream)
print("The index of of the message marker is:", index, str(datastream[index-14:index]))