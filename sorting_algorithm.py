import re
import random
import pandas as pd
from typing import List
from dataclasses import dataclass
# -*- coding: utf-8 -*-


class NecessaryListsFactory(object):
    
    def __init__(self, name_and_wish_list):
        #print(name_and_wish_list)        
        # If participant list has duplicates, return and print error message which contains list of duplicate participants
        handle_duplicates = HandleDuplicates()
        if(handle_duplicates.has_participant_list_duplicates(name_and_wish_list)):
            duplicate_names_without_typos = handle_duplicates.get_duplicates_without_typos(name_and_wish_list)
            message = handle_duplicates.get_duplicate_error_message(duplicate_names_without_typos)
            raise DuplicatesInParticipantsError(message)
        # Dp not add random shuffle back until seating generation is done fully automatically. Now user does bulk of the work and
        #shuffling between running the script multiple times just messes with the user flow
        #random.shuffle(name_and_wish_list) # This shuffle is done because without it the first and last who signed up for the event would always sit in at the end of the table! 
        
        self.name_and_wish_list = name_and_wish_list
        self.pf = ParticipantFactory()
        self.participant_list = [] # Contains only participant objects
        self.dict_of_participants = {} # dictionary of participants, key value is participants name without spaces and caps
        self.anonymous_list = [] #TODO should this be a list or dictionary?
        self.participants_ids_with_special_wishes = []
        self.generate_lists_from_name_and_wish_list()
        self.generate_anonymous_list()
        self.pc = PoolCreation()
        self.pc.create_pools(self.anonymous_list)
        self.all_pools = self.pc.all_mutual_wishes_pools
        #self.seating_order_with_ids = [item for sublist in self.all_pools for item in sublist]
        self.seating_order = self.generate_final_seating_list(self.participant_list, self.pc.wish_pools) # Participant full names are in correct seating order
        #print(self.add_empty_cells_after_these_ids)
        #e = ExportData()
        #e.export_data_to_excel(self.seating_order, self.names_with_color_rules)
    
            
    
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
    
    # Return: final seating list, without the empty cell places for excel
    def generate_final_seating_list(self, participants, pools):
        anonymous_flat_list = [item for sublist in pools for item in sublist]
        result = [] # format, [name1, name2,...nameN]
        for i in range(0, len(anonymous_flat_list)):
            result.append(participants[anonymous_flat_list[i]].full_name)
        return result

class DuplicatesInParticipantsError(Exception):
    """Exception raised when there are duplicates in the given participant list.

    Attributes:
        message -- explanation of the error, contains the list of the duplicate names.
    """

    def __init__(self, message="There is at least one duplicate pair."):
        self.message = message
        super().__init__(self.message)
        
class HandleDuplicates(object):

    #Note: This takes only account if participant names has duplicates, not if the wishes have duplicates
    #Returns: True if there are duplicates in participant list, else returns False
    def has_participant_list_duplicates(self, name_and_wish_list):
        participant_names = [i[0] for i in name_and_wish_list]  
        return len(participant_names) != len(set(participant_names))
    
    #returns: dictionary, key:name_without_typos, value:full_name_with_typos
    def get_duplicates_without_typos(self, name_and_wish_list): 
        duplicate_names = {} 
        for i, p_name_and_wishes in enumerate(name_and_wish_list): 
            for j, p_name_and_wishes_comparable in enumerate(name_and_wish_list): 
                name1 = p_name_and_wishes[0].lower() 
                tmp = re.sub("\s+", "", name1.strip()) 
                name2 =  p_name_and_wishes_comparable[0].lower() 
                tmp2 = re.sub("\s+", "", name2.strip()) 
                if(tmp == tmp2 and j > i): #Strings are the same       
                    name = p_name_and_wishes[0] 
                    duplicate_names[tmp] = name
        return duplicate_names
    
    #duplicate_names_without_typos: dictionary, key:name_without_typos, value:full_name_with_typos
    #Return: Error message with duplicate names listed
    def get_duplicate_error_message(self, duplicate_names_without_typos):
        error_message = 'There are some duplicates, deal with them first! The duplicate participants are: '
        i = 0
        for item in duplicate_names_without_typos:
            if(i == 0): 
                error_message += duplicate_names_without_typos[item]
            else:    
                error_message += ', ' + duplicate_names_without_typos[item]
            i += 1
        return(error_message)
    
    ##################################
    #    Handle duplicates ENDS    #
    ##################################
    
class ParticipantFactory(object):
       
    def load_men_names(self):
        men_first_names = pd.read_excel ('etunimitilasto-2021-02-05-dvv.xlsx', sheet_name='Miehet ens')["Etunimi"] 
        self.men_first_names = men_first_names.tolist()
       
    # Returns new Participant object with necessary information
    # Participant is list containing name and and friend list, where elements are [<participant fullname>, <seating order wishes>]
    def create_participant_from_given_name(self, participant_and_wishes_list, id):
        ######################
        # Participant's name
        ######################
        full_name = self.get_name_without_extra_spaces(participant_and_wishes_list[0])
        first_name = self.get_first_names(full_name)
        surname = self.get_surname(full_name)
        name_without_typos = self.get_name_without_spaces_and_caps(full_name)
        try:
            self.men_first_names
            is_man = first_name in self.men_first_names
        except AttributeError:
            is_man = False
         
        
        ######################
        # wish list
        ######################
        wish_list = participant_and_wishes_list[1]
        wish_list_without_spaces_and_caps = self.get_wish_list_without_spaces_and_caps(wish_list)
        
        p = Participant(id, full_name, first_name, surname, name_without_typos, is_man, wish_list, wish_list_without_spaces_and_caps)
        return p
    
    def get_name_without_extra_spaces(self, full_name):
        name = full_name
        name = re.sub("\s\s+" , " ", name)
        if name[0] == ' ':
            name = name.split(" ", 1)[1]
        if name[len(name)-1] == ' ':
            name = name.rsplit(" ", 1)[0]
        return name
        
    
    # return first names if name contains space, otherwise returns full name
    # 'Matti Matias Meikäläinen' returns 'Matti Matias'
    def get_first_names(self, name):
        splitted_name = name.rsplit(" ", 1)[0]
        return splitted_name
  
    # return last name if name contains space, otherwise returns full name
    def get_surname(self, name):
        splitted_name = name.split(" ")
        if(len(splitted_name) >= 2):
            return splitted_name[len(splitted_name)-1]
        else: #TODO this is maybe unnecessary
            #Maybe other should be just an empty space?
            return splitted_name[0]

    
    def get_name_without_spaces_and_caps(self, name):
        tmp = name.lower()
        tmp = re.sub("\s+", "", tmp.strip())
        return tmp
    
    def get_wish_list_without_spaces_and_caps(self, wish_list):
        wish_list_without_spaces_and_caps = []
        for name in wish_list:
            wish_list_without_spaces_and_caps.append(self.get_name_without_spaces_and_caps(name))
        return wish_list_without_spaces_and_caps

@dataclass(frozen = True) #TODO change this class to be frozen
class Participant:
    id: int
    full_name: str 
    first_name: str 
    surname: str
    name_without_typos: str #Name where the caps and spaces are removed. This is to avoid atleast some user typos when they were typing seating wishes list
    is_man: bool
    seating_wish_list: List[str] #TODO this can be mutated afterwards, convert to frozen dataclass object
    seating_wish_list_without_spaces_and_caps: List[str] #TODO this can be mutated afterwards, convert to frozen dataclass object
    
    
    #TODO pool creation
class PoolCreation(object):        
    
    # Creates both pools in correct order.
    def create_pools(self, anonymous_list):
        print("pool creation has started")
        self.create_all_wishes_to_same_group(anonymous_list)
        self.create_mutual_wishes_groups(self.wish_pools, anonymous_list)
        print('Pools have been created!')
    
    # - anonymous_list: [[0, [89, 75, 50, 23], True], [1, [71, 138, 81, 85], False],...]
    #   where [participant_id, [participant's_wishes], isMan]
    # - Note: the is_man is not used here, only things required are participant_id, [participant's_wishes]
    # -  This adds all those who wished sit to next to each other to same group. The attribute where different groups
    #    are stored is "wish_pools".
    # - wish pools format: [[0,1,2] [group2], [group3]], numbers are participant id's.
    def create_all_wishes_to_same_group(self, anonymous_list):
        print("Started creating all-wishes-to-same-group-pools")
        self.anonymous_list = anonymous_list
        self.wish_pools = [] #contains all different pools
        
        for participant_and_wishes in anonymous_list:
            new_pool = []
            ##TODO check that the references do not break
            participant = participant_and_wishes[0]
            participant_wishing_list = participant_and_wishes[1]
            if self.wish_pools : 
                #Check all existing pools
                duplicate_pools_to_be_removed = []
                for pool in self.wish_pools:
                    if participant in pool:
                        # they should not be the same object
                        duplicate_pools_to_be_removed.append(pool)
                        new_pool = new_pool + pool
                    wishes_to_be_deleted = []    
                    for wish in participant_wishing_list:
                        #Combine the pools if necessary
                        if(wish in pool and participant not in pool):
                            if(pool not in duplicate_pools_to_be_removed):
                                duplicate_pools_to_be_removed.append(pool)    
                            new_pool =  pool + new_pool
                            wishes_to_be_deleted.append(wish)
                    # Remove already added wishes
                    for dele in wishes_to_be_deleted:
                        participant_wishing_list.remove(dele)
                # Remove duplicate pools
                for dup in duplicate_pools_to_be_removed:
                    if(dup in self.wish_pools):
                        self.wish_pools.remove(dup)
                
                # Add participant to new_pool if he is not in the new_pool
                if participant not in new_pool:
                    new_pool.append(participant)
                #Add rest of the wishing list to new_pool
                if(participant_wishing_list):
                    for part in participant_wishing_list:
                        if(part not in new_pool):
                            new_pool.append(part)
                #Finally, add new pool to all_pools
                if(new_pool):
                    self.wish_pools.append(new_pool)
            else: # special case for the first pool
                new_pool.append(participant)
                if(participant_wishing_list):
                    for p_and_wishes in participant_wishing_list:
                        new_pool.append(p_and_wishes)
                self.wish_pools.append(new_pool)
        print("All wishes to same-group-pools-have-been-created!")
        
    # - Create mutual wishes subgroups. These will be added "all_mutual_wishes_pools"-list. 
    # - anonymous_list: [[0, [89, 75, 50, 23], True], [1, [71, 138, 81, 85], False],...] 
    #    where [participant_id[participant's_wishes], isMan]
    # - #Note: the is_man is not used here, only things required are participant_id, [participant's_wishes]
    # - wish_pools: Contains pools of participants where at least one participant has wished other as a seat wish. This
    #   parameter is a list and the list is created with create_all_wishes_to_same_group(anonymous_list).
    # - pools_of_mutual_wishes format:
    #    [ [[0,1,2] [3,4,58, 25], [9]], [[mutual_wish_list1],[mutual_wish_list2]... [mutual_wish_listN]],
    #    ... [wish_poolN]],numbers are participant id's.
    # - How this works: This breaks down wish_pools pools to even smaller pools (lists).
    #   So e.g. let's say that the anonymous_list is: [[0 [1,2]], [1, [0, 2]], [2, []], [[3], []] ].
    #   - NOTE: empty list means that that participant did not have any seat wishes.
    #   It will be converted in create_all_wishes_to_same_group(anonymous_list)-method to be the following: [[0,1,2], [3]]
    # - So after this method all_mutual_wishes_pools is: [[[0,1], [2]], [3]]
    def create_mutual_wishes_groups(self, wish_pools, anonymous_list):
        print('Started creating all mutual wishes pools')
        all_mutual_wishes_pools = []
        for pool in wish_pools:
            sub_pool = []
            # If Id is already added to some small_pool, don't add it again
            already_added_ids = []
            #Iterate through the pool
            for p_id in pool:
                checked_p = anonymous_list[p_id] #checked participant
                checked_p_id = checked_p[0]
                checked_p_wish_list = checked_p[1]
                # Create a mutual wish group for this participant
                mutual_wish_pool = [] 
                
                if(checked_p_id not in already_added_ids):
                    mutual_wish_pool.append(checked_p_id) 
                
                already_added_ids.append(checked_p_id)
                for wish in checked_p_wish_list:
                    checked_w = anonymous_list[wish] #checked wish
                    checked_w_id = checked_w[0]
                    checked_w_wish_list = checked_w[1]
                    if(checked_p_id in checked_w_wish_list and  checked_w_id not in already_added_ids):
                        mutual_wish_pool.append(checked_w_id)
                        already_added_ids.append(checked_w_id)
                if mutual_wish_pool:    
                    sub_pool.append(mutual_wish_pool)
            all_mutual_wishes_pools.append(sub_pool)
        self.all_mutual_wishes_pools = all_mutual_wishes_pools
        print('all mutual wishes pools has been created')
