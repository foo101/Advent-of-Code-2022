import os

os.chdir("day 2")



rps_results = []
for str_in in open("data.txt", "rt"):
    result = str_in[:-1].split(sep=' ')
    # print(result) # result is a list with opponent's play and own play
    rps_results.append(result)

rps_table_of_score_bonus_per_outcome = {"wins":6, "draws":3, "losses":0}
rps_table_of_score_bonus_per_play = {"X":1, "Y":2, "Z":3}

# part 1: play whatever the guide tells you

def calc_score_by_play(plays: list[list[str]]) -> int:
    rps_outcome_per_play = {
        "A":{"X":"draws", "Y":"wins", "Z":"losses"}, 
        "B":{"X":"losses", "Y":"draws", "Z":"wins"}, 
        "C":{"X":"wins", "Y":"losses", "Z":"draws"}}
    
    score = 0
    for play in plays:
        their_play = play[0]
        my_play = play[1]
        outcome = rps_outcome_per_play[their_play][my_play]

        score += rps_table_of_score_bonus_per_play[my_play]
        score += rps_table_of_score_bonus_per_outcome[outcome]

        # print(play, outcome, rps_table_of_score_bonus_per_play[my_play], rps_table_of_score_bonus_per_outcome[outcome])
    return score

print(calc_score_by_play(rps_results)) # TODO: apply to full dataset

#part 2: play whatever the guide tells you is the outcome
def calc_score_by_outcome(plays: list[list[str]]) -> int:
    rps_translate_outcome = {
        "X":"losses", 
        "Y":"draws", 
        "Z":"wins"}
    
    rps_play_per_outcome = {
        "A":{"wins":"Y", "draws":"X", "losses":"Z"}, 
        "B":{"wins":"Z", "draws":"Y", "losses":"X"}, 
        "C":{"wins":"X", "draws":"Z", "losses":"Y"}}
    
    score = 0
    for play in plays:
        their_play = play[0]
        outcome = rps_translate_outcome[play[1]]
        my_play = rps_play_per_outcome[their_play][outcome]

        score += rps_table_of_score_bonus_per_play[my_play]
        score += rps_table_of_score_bonus_per_outcome[outcome]

        # print(play, outcome, rps_table_of_score_bonus_per_play[my_play], rps_table_of_score_bonus_per_outcome[outcome])
    return score

print(calc_score_by_outcome(rps_results)) # TODO: apply to full dataset