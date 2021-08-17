# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 16:00:54 2021

@author: rytil
"""
import pandas as pd
import random
from dataclasses import dataclass, field, astuple, asdict
from typing import List
import re

class DataGenerator(object):
    def __init__(self):
        self.data_size= 100
        self.max_data_size = 141 # Maximum data size with current parsing setting that can be used without firstname duplicates in men and women
        self.male_first_names = pd.read_excel (r'C:\Users\rytil\Documents\Github\seating-order-organizer\etunimitilasto-2021-02-05-dvv.xlsx', sheet_name='Miehet ens')["Etunimi"]
        self.female_first_names  = pd.read_excel (r'C:\Users\rytil\Documents\Github\seating-order-organizer\etunimitilasto-2021-02-05-dvv.xlsx', sheet_name='Naiset kaikki')["Etunimi"]
        self.surnames = pd.read_excel (r'C:\Users\rytil\Documents\Github\seating-order-organizer\sukunimitilasto-2021-02-05-dvv.xlsx', sheet_name='Nimet')["Sukunimi"]
        self.generated_names = []
        self.name_and_friend_list = []
        self.generate_unique_names()
        self.generate_name_and_friend_list()
    
    # Generate unique names for participants
    def generate_unique_names(self):
        surname_index = 0 # Same surnames for every group that has asked each other as seating company. This is simply for convenience and easier checkming later the results of seating organizer algorithm by hand
        for i in range(0, self.data_size):   
            if(i % 5 == 0 and i != 0):
                surname_index = i
            if(i % 2 == 0):
                self.generated_names.append(self.male_first_names[i] + " " + self.surnames[surname_index])
            else:
                self.generated_names.append(self.female_first_names[i] + " " + self.surnames[surname_index])
    
    def generate_name_and_friend_list(self):
        for i in range(0, len(self.generated_names)):
            participant_surname = self.generated_names[i].split(sep= " ", maxsplit=2)[1]
            participant_name = self.generated_names[i]
            friends = [] # seating request, who I wan't to sit next to me
            for j in range(-5, 6): #Loop trough all people on both sides of the person
                current_loop_index = i + j
                if(current_loop_index >= 0 and current_loop_index < len(self.generated_names)):
                    request_name = self.generated_names[current_loop_index]
                    request_surname = request_name.split(sep= " ", maxsplit=2)[1]
                    if(participant_surname == request_surname and participant_name != request_name):    
                        friends.append(self.generated_names[current_loop_index])
            temp = [] #Temp for storing list containing two elements: <name>, <seating_request>
            temp.append(self.generated_names[i])
            temp.append(friends)
            self.name_and_friend_list.append(temp)


class NecessaryListsFactory(object):
    
    def __init__(self, name_and_wish_list):
        self.name_and_wish_list = name_and_wish_list
        self.pf = ParticipantFactory()
        self.participant_list = [] # Contains only participant objects
        self.dict_of_participants = {} # dictionary of participants, key value is participants name without spaces and caps
        self.anonymous_list = [] #TODO should this be a list or dictionary?
        self.generate_lists_from_name_and_wish_list()
        self.generate_anonymous_list()
        
    def generate_lists_from_name_and_wish_list(self):
        for i in range(0, len(self.name_and_wish_list)):
            p = self.pf.create_participant_from_given_name(self.name_and_wish_list[i], i)
            self.dict_of_participants[p.name_without_typos] = p
            self.participant_list.append(p)
    
    # creates elements to self.anonymous list in the following format [<participant id>, <seating order wishes id> <is man>]
    def generate_anonymous_list(self):
        for p in self.participant_list:
            individual_participant_and_wishes_list = [] # is anonymous using only id's
            individual_participant_and_wishes_list.append(p.id)
            individual_participant_and_wishes_list.append(self.create_anonymous_seating_wish_list(p))
            individual_participant_and_wishes_list.append(p.is_man)
            self.anonymous_list.append(individual_participant_and_wishes_list)
    
    def create_anonymous_seating_wish_list(self, p):
        seating_wish_list = []
        for wish in p.seating_wish_list_without_spaces_and_caps:
            seating_wish_list.append(self.dict_of_participants[wish].id)
        return seating_wish_list
        
        


class ParticipantFactory(object):
    def __init__(self):
        male_first_names = pd.read_excel (r'C:\Users\rytil\Documents\Github\seating-order-organizer\etunimitilasto-2021-02-05-dvv.xlsx', sheet_name='Miehet ens')["Etunimi"] 
        self.male_first_names = male_first_names.tolist()
       
        
    # Returns new Participant object with necessary information
    # Participant is list containing name and and friend list, where elements are [<participant fullname>, <seating order wishes>]
    def create_participant_from_given_name(self, participant_and_wishes_list, id):
        ######################
        # Participant's name
        ######################
        full_name = participant_and_wishes_list[0]
        first_name = self.generate_first_name(full_name)
        last_name = self.generate_last_name(full_name)
        name_without_typos = self.generate_name_without_spaces_and_caps(full_name)
        is_man = first_name in self.male_first_names
         
        
        ######################
        # wish list
        ######################
        wish_list = participant_and_wishes_list[1]
        wish_list_without_spaces_and_caps = self.generate_wish_list_without_spaces_and_caps(wish_list)
        
        p = Participant(id, full_name, first_name, last_name, name_without_typos, is_man, wish_list, wish_list_without_spaces_and_caps)
        return p
        
    # return first name if name contains space, otherwise returns full name
    def generate_first_name(self, name):
        splitted_name = name.split(" ", 1)
        return splitted_name[0]
  
    # return last name if name contains space, otherwise returns full name
    def generate_last_name(self, name):
        splitted_name = name.split(" ", 1)
        if(len(splitted_name) >= 2):
            return splitted_name[1]
        else: #TODO this is maybe unnecessary
            #Maybe other should be just an empty space?
            return splitted_name[0]

    
    def generate_name_without_spaces_and_caps(self, name):
        tmp = name.lower()
        tmp = re.sub("\s+", "", tmp.strip())
        return tmp
    
    def generate_wish_list_without_spaces_and_caps(self, wish_list):
        wish_list_without_spaces_and_caps = []
        for name in wish_list:
            wish_list_without_spaces_and_caps.append(self.generate_name_without_spaces_and_caps(name))
        return wish_list_without_spaces_and_caps

@dataclass(frozen = True) #TODO change this class to be frozen
class Participant:
    id: int
    full_name: str 
    first_name: str 
    last_name: str
    name_without_typos: str #Name where the caps and spaces are removed. This is to avoid atleast some user typos when they were typing seating wishes list
    is_man: bool
    seating_wish_list: List[str] #TODO this can be mutated afterwards, convert to frozen dataclass object
    seating_wish_list_without_spaces_and_caps: List[str] #TODO this can be mutated afterwards, convert to frozen dataclass object
    
    


class ScoreCalculation(object):
    def __init__(self, anonymous_list, male_first_names):
        self.anonymous_list = anonymous_list
        self.male_first_names = male_first_names.tolist()
        self.baseline_score = 0 # Generated ny shuffling the perfect order list
        self.final_score = 0
        self.participant_id_list = []
        self.best_order = []
        
        
        # Temporary solution, wil be deleted when score calcucalation is done
        for i in range(0, len(anonymous_list)):
            participant_id = anonymous_list[i][0]
            self.best_order.append(participant_id)
            self.participant_id_list.append(participant_id) 
        #random.shuffle(self.participant_id_list) # TODO remove
        
        
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
            print("a")
            seating_wish_id = seating_wishes[i]
            self.score_table_2d[checked_index][seating_wish_id] += friend_score
                        
# Index numbers for helping to visualise seating order
#0, 1
#3, 2
#4, 5
#7, 6
#8, 9
#11, 10
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
                    if((checked_index < len(self.best_order) and checked_index >= 0) and index != checked_index):
                        checked_id_of_index = self.best_order[checked_index]
                        #print("index in best order", checked_index)
                        #print("id of best order: ", checked_id_of_index)
                        self.final_score += self.score_table_2d[participant_id][checked_id_of_index]
if __name__:
    print("Data generator is run in namespace")
    d = DataGenerator()
    s = ScoreCalculation(d.name_and_friend_list, d.male_first_names)
    print(d.generated_order[10][1])
    #print(d.female_first_names)
    #print(d.surnames)