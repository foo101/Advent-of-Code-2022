import os

os.chdir("day 2")

rps_results = []
rps_sum_of_results = {"wins":0, "draws":0, "losses":0}

rps_table_of_score_bonus_per_outcome = {"wins":6, "draws":3, "losses":0}
rps_table_of_score_bonus_per_play = {"X":1, "Y":2, "Z":3}

rps_score = 0 # score tracker

for str_in in open("data.txt", "rt"):
    result = str_in[:-1].split(sep=' ')
    # print(result) # result is a list with opponent's play and own play
    rps_results.append(result)

rps_score_bonus_per_play = {"X":1, "Y":2, "Z":3}

for result in rps_results:
    rps_suggested_play = result[1]
    outcome = (ord(result[1]) - ord(result[0]) - 23) % 3 # 0 if draw, 1 if win, 2 if loss
    # per outcome, calculate score for win/loss/draw
    if(outcome == 1):
        rps_sum_of_results["wins"] += 1
        rps_score += rps_table_of_score_bonus_per_outcome["wins"]
    elif(outcome == 2):
        rps_sum_of_results["losses"] += 1
        rps_score += rps_table_of_score_bonus_per_outcome["losses"]
    elif(outcome == 0):
        rps_sum_of_results["draws"] += 1
        rps_score += rps_table_of_score_bonus_per_outcome["draws"]
    else:
        print("Something went wrong at parsing the outcome of", result)

    # per outcome, calculate score for play
    if(result[1] in rps_score_bonus_per_play.keys()):
        rps_score += rps_score_bonus_per_play[rps_suggested_play]
    else:
        print("something went wrong at parsing the result of", str_in)

# scores if you follow the plan
print("score after the match (complex plan):", rps_score)


# scores with X = loss, Y = draw, Z = win
rps_suggested_plays = {
    "A":{"X":"Z", "Y":"X", "Z":"Y"}, 
    "B":{"X":"X", "Y":"Y", "Z":"Z"}, 
    "C":{"X":"Y", "Y":"Z", "Z":"X"}}

rps_score = 0
rps_sum_of_results = {"wins":0, "draws":0, "losses":0}
rps_sum_of_plays = {"X":0, "Y":0, "Z":0}

for result in rps_results:
    rps_suggested_play = rps_suggested_plays[result[0]][result[1]]
    rps_score_this_match = 0
    if(result[1] == 'X'):
        rps_sum_of_results["wins"] += 1
        rps_score_this_match += rps_table_of_score_bonus_per_outcome["wins"]
    elif(result[1] == 'Z'):
        rps_sum_of_results["losses"] += 1
        rps_score_this_match += rps_table_of_score_bonus_per_outcome["losses"]
    elif(result[1] == 'Y'):
        rps_sum_of_results["draws"] += 1
        rps_score_this_match += rps_table_of_score_bonus_per_outcome["draws"]
    else:
        print("something went wrong at parsing the result of", result)
    
    rps_score_this_match += rps_score_bonus_per_play[rps_suggested_play]
    rps_sum_of_plays[rps_suggested_play] += 1
    # print("result:", result, "play:", rps_suggested_play, "score:", rps_score_this_match)
    rps_score += rps_score_this_match

# print(rps_sum_of_results)
# print(rps_sum_of_plays)

print("score after the match (complex plan, play determines outcome):", rps_score)

# print("amount of results:", len(rps_results))

rps_score = 0
for res in rps_sum_of_results.keys():
    rps_score += rps_table_of_score_bonus_per_outcome[res] * rps_sum_of_results[res]

for res in rps_sum_of_plays.keys():
    rps_score += rps_score_bonus_per_play[res] * rps_sum_of_plays[res]

print("score after the match (complex plan, play determines outcome):", rps_score)