# -*- coding: utf-8 -*-

# Class for calculating scores. This was used in the first iteration, when participant seating places were
# sorted by genetic algorithm. This creates a 2d table where participant are scored based on their wishes
# and gender. This code can be used to benchmark new algorithm against old one or used as a fitness score
# for different machine learning or hand crafted algorithms. NOTE: before using, set so that score on gender
# is not used.
class ScoreCalculation(object):
    def __init__(self, anonymous_list, male_first_names):
        self.anonymous_list = anonymous_list
        self.male_first_names = male_first_names.tolist()
        self.baseline_score = 0 # Generated ny shuffling the perfect order list
        self.final_score = 0
        self.participant_id_list = []
        self.best_order = []
        #random.shuffle(self.anonymous_list)
        
        
        # Temporary solution, wil be deleted when score calcucalation is done
        for i in range(0, len(anonymous_list)):
            participant_id = anonymous_list[i][0]
            self.best_order.append(participant_id)
            self.participant_id_list.append(participant_id) 
        
        
        self.generate_empty_score_table_2d()
        self.add_scores_to_table()
        
    # Generate empty score table with starting base score of 10        
    def generate_empty_score_table_2d(self):
        self.score_table_2d= []
        for i in range(0, len(self.participant_id_list)):
            tmp= []
            for j in range(0, len(self.participant_id_list) ):
                tmp.append(10)
            self.score_table_2d.append(tmp)
            
    def add_scores_to_table(self):
        for i in range(0, len(self.participant_id_list)):
            self.add_score_based_on_gender(i, self.anonymous_list[i][2])
            self.add_score_based_on_wishes(i)
        self.calculate_score()
            
    # checked_index: person who is checked
    # is_man: previusly checked that person's first name is found from list of men names
    def add_score_based_on_gender(self, checked_index, is_man):
        different_gender_score = 2
        for i in range(0, len(self.participant_id_list)):
            if(self.anonymous_list[i][2] != is_man):
                previous_score = self.score_table_2d[checked_index][i] 
                self.score_table_2d[checked_index][i] = previous_score + different_gender_score
    
    # Add score to 2d_score_table generated from seating wishes
    def add_score_based_on_wishes(self, checked_index):
        friend_score = 3
        seating_wishes = self.anonymous_list[checked_index][1]
        for i in range (0, len(seating_wishes)):
            
            seating_wish_id = seating_wishes[i]
            self.score_table_2d[checked_index][seating_wish_id] += friend_score
                        
# Index numbers for helping to visualise seating order # DEPRECATED, #FIXME
#Old way:
#0, 1
#3, 2
#4, 5
#7, 6
#8, 9
#11, 10
# I changed it to go more logically in the actual algorithm, so score calculation needs to be done in the following way:
#New way:
#0, 1
#2, 3
#4, 5
#6, 7
#8, 9
#11, 10
# Note: I think this only affects to gender score calculation though, so it maybe does not needed to be fixed.
    # sets self.final_score to 0 and after that calculates the correct score
    def calculate_score(self):        
        self.final_score = 0

        for i in range(0, len(self.best_order)):
            
            #-------------------------------------------
            # DO PROPER TESTS FOR THIS, SHOULD WORK NOW THOUGH
            #-------------------------------------------
            #print("NEW PERSON, his index is: " , i)
            if(i % 2== 0): #Check the left side of generated table (check github repo's wiki-section for reference)               
                # check two previous index and three next if exists
                starting_value = i-2
                ending_value = i+4
                self.calculate_score_from_index(i, starting_value, ending_value)             
            else:
                starting_value = i-3
                ending_value = i+3
                self.calculate_score_from_index(i, starting_value, ending_value)
            #-------------------------------------------
            # DO PROPER TESTS ENDS
            #-------------------------------------------
    
    def calculate_score_from_index(self, index, starting_value, ending_value):
            participant_id = self.best_order[index]
            for checked_index in range(starting_value, ending_value):        
                    if(self.is_valid_index(checked_index, len(self.best_order)) and index != checked_index):
                        checked_id_of_index = self.best_order[checked_index]
                        #print("index in best order", checked_index)
                        #print("id of best order: ", checked_id_of_index)
                        self.final_score += self.score_table_2d[participant_id][checked_id_of_index]
    
    # Element exists in given array
    def is_valid_index(self, checked_index, length_of_array):
        return (checked_index < length_of_array and checked_index >= 0)
