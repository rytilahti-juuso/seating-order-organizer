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
    
    #Generate new target csv. This should be called only when you want to create external excel from pregenerated data. Added for convenience.
    #name and friend list format: [['Juha Korhonen', ['Helena Korhonen', 'Matti Korhonen', 'Johanna Korhonen', 'Mikko Korhonen']], ...]
    #Requires that the target exists #TODO create a new file if target file does not exist
    #NOTE: #FIXME #TODO You may need to import the file with LibreOffice Calc and change it to correct format from .xlsx text import.
    def generate_new_csv(self, name_and_friend_list):
        print("New csv is being generated")
        name = [] #Every participant's name in format: [name1, name2, ...]
        wishes = [] #Wishes of every person in following format: [[wish_list_of_person_1], [wish_list_of_person_2], ...]
        for i in range(0, len(name_and_friend_list)):
            name.append(name_and_friend_list[i][0])
            all_one_person_wishes_as_string = ''
            for j in range(0, len(name_and_friend_list[i][1])): # Loop through all friends
                wished_person_name = name_and_friend_list[i][1][j]
                if(j != (len( name_and_friend_list[i][1])-1) ): # If person is last on the wished list, don't add comma to end    
                    wished_person_name = wished_person_name + ", "
                all_one_person_wishes_as_string += wished_person_name  
            wishes.append(all_one_person_wishes_as_string)
        dictionary = {'Name': name, 'Wishes': wishes}  
        dataframe = pd.DataFrame(dictionary) 
        dataframe.to_csv(r'C:\Users\rytil\Documents\Github\seating-order-organizer\target.xlsx')
        
class ImportDataFromExcel(object):
    def __init__(self):
        print("Importing data from excel")
        self.df = pd.read_excel (r'C:\Users\rytil\Documents\Github\seating-order-organizer\target.xlsx', header=None, names=('Name', 'Wishes'))
        self.data = [] #Format [['Juha Korhonen', ['Helena Korhonen', 'Matti Korhonen', 'Johanna Korhonen', 'Mikko Korhonen']], ...]
        names = self.df['Name'].values.tolist()
        wishes = self.df['Wishes']
        wishes = wishes.tolist()
        for i in range(0, len(wishes)):
            wishes_as_string = str(wishes[i])
            wishes_as_list = self.convert_wishes_to_list(wishes_as_string)
            row = [] #contains: person's_name, [wish_list], example row with all information: 'Juha Korhonen', ['Helena Korhonen', 'Matti Korhonen', 'Johanna Korhonen', 'Mikko Korhonen']
            row.append(names[i])
            row.append(wishes_as_list)
            self.data.append(row)
        self.data.pop(0) # Removes headers from the list ("name" and "[wishes]") 
            
            
            
        print("Data import has been completed!")
    
    def convert_wishes_to_list(self, wishes):
        wishes = wishes.replace(", ", ",")
        wishes =   wishes.split(",") if wishes else [] #return empty list if string is empty
        wishes = filter(None, wishes) # Remove all empty strings ('A', 'B', 'C', '')
        wishes = list(filter(None, wishes))
        if(len(wishes) == 1 and wishes[0] == 'nan'): # If wish list cell in excel is empty when importing, it defaults to 'nan'.
            wishes = []
        return wishes
        

class NecessaryListsFactory(object):
    
    def __init__(self, name_and_wish_list):
        self.name_and_wish_list = name_and_wish_list
        self.pf = ParticipantFactory()
        self.participant_list = [] # Contains only participant objects
        self.dict_of_participants = {} # dictionary of participants, key value is participants name without spaces and caps
        self.anonymous_list = [] #TODO should this be a list or dictionary?
        self.participants_ids_with_special_wishes = []
        self.generate_lists_from_name_and_wish_list()
        self.generate_anonymous_list()
        pc = PoolCreation(self.anonymous_list)
        self.all_pools = pc.all_pools_list
        self.seating_order = self.generate_final_seating_list(self.participant_list, pc.all_pools_list) # Participant full names are in correct seating order
        
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
            individual_participant_and_wishes_list.append(self.create_anonymous_seating_wish_list_and_special_wishes_list(p))
            individual_participant_and_wishes_list.append(p.is_man)
            self.anonymous_list.append(individual_participant_and_wishes_list)
    
    #p = Participant dataclass object
    def create_anonymous_seating_wish_list_and_special_wishes_list(self, p):
        seating_wish_list = []
        has_special_wishes = False
        for wish in p.seating_wish_list_without_spaces_and_caps:
            if(wish in self.dict_of_participants): #If wish is typo or special wish (e.g old students) it should not be added to seating wish list (raises KeyError)     
                seating_wish_list.append(self.dict_of_participants[wish].id)
            else:
                has_special_wishes = True
        if(has_special_wishes):
            self.participants_ids_with_special_wishes.append(p.id)
        return seating_wish_list
    
    def generate_final_seating_list(self, participants, pools):
        anonymous_flat_list = [item for sublist in pools for item in sublist]
        result = [] # format, [name1, name2,...nameN]
        for i in range(0, len(anonymous_flat_list)):
            result.append(participants[anonymous_flat_list[i]].full_name)
        return result
        
        
        
        
        
    
        
        


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
    
    
    #TODO pool creation
class PoolCreation(object):
    
    def __init__(self, anonymous_list):
        self.anonymous_list = anonymous_list
        self.all_pools_list = [] #contains all different pools
        print("pool creation has started")
        for i in range(0, len(anonymous_list)):
            new_pool = []
            ##TODO check that the references do not break
            participant = self.anonymous_list[i][0]
            participant_wishing_list = self.anonymous_list[i][1] 
            if(self.all_pools_list):
                new_pool = self.add_participant_to_new_pool(participant, new_pool, self.all_pools_list)
                for x in range(0, len(participant_wishing_list)):
                    new_pool = self.add_participant_to_new_pool(participant_wishing_list[x], new_pool, self.all_pools_list)
                #print("all_pool_list_is_not_empty")
                if(new_pool):    
                    self.all_pools_list.append(new_pool)
                    
                    
                        
                    
            else: # special case for the first pool
                #print("all_pools_list_is_empty") 
                new_pool.append(participant)
                if(participant_wishing_list):
                    for j in range(0, len(participant_wishing_list)):
                        new_pool.append(participant_wishing_list[j])
                self.all_pools_list.append(new_pool)
    
#participant_id: Id of the checked participant
#pool: pool that is checked if it contains the given id                
    def is_participant_id_in_iterated_pool(self, pool, participant_id):
        for i in range(len(pool)):
            #print(pool[i])
            #print(participant_id)
            #print(pool[i] == participant_id)
            if(pool[i] == participant_id):
                return True
        return False

    def add_participant_to_new_pool(self, participant, new_pool, all_pools):
        is_already_in_some_pool = self.is_participant_id_in_iterated_pool(new_pool, participant)
        if(is_already_in_some_pool is False):    
            for i in range(0, len(all_pools)):
                iterated_pool = all_pools[i]
                if(self.is_participant_id_in_iterated_pool(iterated_pool, participant)):
                    is_already_in_some_pool = True
                    break
                #Else do nothing
            if(is_already_in_some_pool is False): # Time to add a new pool
                new_pool.append(participant)
        return new_pool
                        
            
        
        

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
                    if(self.is_valid_index(checked_index, len(self.best_order)) and index != checked_index):
                        checked_id_of_index = self.best_order[checked_index]
                        #print("index in best order", checked_index)
                        #print("id of best order: ", checked_id_of_index)
                        self.final_score += self.score_table_2d[participant_id][checked_id_of_index]
    
    # Element exists in given array
    def is_valid_index(self, checked_index, length_of_array):
        return (checked_index < length_of_array and checked_index >= 0)
    
if __name__:
    print("Data generator is run in namespace")
    #d = DataGenerator()
    #nlf = NecessaryListsFactory(d.name_and_friend_list) #Necessary lists factory
    #print(d.name_and_friend_list)
    #print(nlf.anonymous_list)
    #print(nlf.participant_list)
    
    ###IMPORT DUMMY DATA FROM EXCEL AND CREATE POOLS FROM THAT DATA ###################################
    #imp = ImportDataFromExcel()
    #nlf = NecessaryListsFactory(imp.data)
    #poolcreation = PoolCreation(nlf.anonymous_list)
    ###IMPORT DUMMY DATA FROM EXCEL AND CREATE POOLS FROM THAT DATA ENDS ###################################
    
    #print(poolcreation.all_pools_list)
    #s = ScoreCalculation(nlf.anonymous_list, d.male_first_names)
    #print(s.score_table_2d)
    #print(d.generated_order[10]][1)
    #pf = ParticipantFactory()
    #p = pf.create_participant_from_given_name(d.name_and_friend_list[1])
    #print(p)
    #print(s.score_table_2d)
    #print(d.female_first_names)
    #print(d.surnames)