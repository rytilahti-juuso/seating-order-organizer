#© 2021 Juuso Rytilahti.  All rights reserved.
import re
import random
import copy
from collections import OrderedDict
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
        self.wish_pools = self.create_non_mutual_wish_pools(anonymous_list)
        self.all_mutual_wishes_pools = self.create_mutual_wishes_groups(self.wish_pools, anonymous_list)
        print('Pools have been created!')
    
                    
    def create_non_mutual_wish_pools(self, anonymous_list):
        wish_pools = []
        for p in anonymous_list:
            p_id = p[0]
            p_wishes = p[1]
            # First time setup
            if not wish_pools:
                init_pool = self.create_new_pool_and_append_the_element_to_it(p_id)
                for a in p_wishes:
                    init_pool.append(a)
                wish_pools.append(init_pool)
            # Add to existing pool
            is_not_added_yet = True
            for pool in wish_pools:
                for id in pool:
                    if id in p_wishes and p_id not in pool:
                        pool.append(p_id)
                        is_not_added_yet = False
            if is_not_added_yet:
                wish_pools.append(self.create_new_pool_and_append_the_element_to_it(p_id))
        return wish_pools
    
    def create_new_pool_and_append_the_element_to_it(self, p_id):
        new_pool = []
        new_pool.append(p_id)
        return new_pool
            
            
            
                        
    #TODO remove
    # - anonymous_list: [[0, [89, 75, 50, 23], True], [1, [71, 138, 81, 85], False],...]
    #   where [participant_id, [participant's_wishes], isMan]
    # - Note: the is_man is not used here, only things required are participant_id, [participant's_wishes]
    # -  This adds all those who wished sit to next to each other to same group. The attribute where different groups
    #    are stored is "wish_pools".
    # - wish pools format: [[0,1,2] [group2], [group3]], numbers are participant id's.
    def deprecated_create_all_wishes_to_same_group(self, anonymous_list):
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
        self.remove_duplicates_from_wish_pools(self.wish_pools)
        print("All wishes to same-group-pools-have-been-created!")
    
    #Remove duplicate items from wish pools created in create_all_wishes_to_same_group
    def remove_duplicates_from_wish_pools(self, wish_pools):
        for i, pool in enumerate(wish_pools):
            pool_without_duplicates = list(dict.fromkeys(pool))
            wish_pools[i] = pool_without_duplicates
        
        
    def create_mutual_wishes_groups(self, wish_pools, anonymous_list):
        all_mutual_wishes_pools = []
        for pool in wish_pools:
            sub_pool = []
            # Loop through the pool twice
            for p_id in pool:
                mutual_wish_pool = []
                mutual_wish_pool.append(p_id)
                p = anonymous_list[p_id] #checked participant
                #checked_p_id = checked_p[0]
                p_wish_list = p[1]
                for w_id in pool:
                    w = anonymous_list[w_id]
                    w_wish_list = w[1]
                    if p_id is not w_id:
                       if self.are_wishes_mutual(p_id, w_id, p_wish_list, w_wish_list):
                           if w_id not in mutual_wish_pool:
                               mutual_wish_pool.append(w_id)
                # Go through mutual_wish_pool and remove all wishes that are not fully mutual
                self.remove_not_fully_mutual_wishes(mutual_wish_pool, anonymous_list)
                # Go through sub pool and make sure that this current pool is not yet added
                self.remove_items_already_in_some_sub_pool_from_current_wish_pool(sub_pool, mutual_wish_pool, anonymous_list)
                mutual_wish_pool = self.append_current_mutual_wish_pool_to_existing_sub_pool_if_possible(mutual_wish_pool, sub_pool, anonymous_list)
                if mutual_wish_pool:                    
                    sub_pool.append(mutual_wish_pool)
            if sub_pool:
                all_mutual_wishes_pools.append(sub_pool)
        return all_mutual_wishes_pools
    
    # If mutual wish pool can be appended, this returns empty mutual wish pool
    # and appends all elements of the current wish pool to correct already existing pool in sub_pool array
    def append_current_mutual_wish_pool_to_existing_sub_pool_if_possible(self, mutual_wish_pool, sub_pool, anonymous_list):
        for pool in sub_pool:
            can_be_appended = True
            for p_id in pool:
                p_wishes = anonymous_list[p_id][1]
                for m_id in mutual_wish_pool:
                    m_wishes = anonymous_list[m_id][1]
                    if p_id not in m_wishes or m_id not in p_wishes:
                        can_be_appended = False
            if can_be_appended:
                for a in mutual_wish_pool:
                    pool.append(a)
                mutual_wish_pool = []
        return mutual_wish_pool
            
                     
                    
            
    # mutual_wish_pool: pool that is mutated and that where the not fully mutual wishes are removed.
    # Checks the first element and it's fully mutual wishes                       
    def remove_not_fully_mutual_wishes(self, mutual_wish_pool, anonymous_list):
        to_be_removed = []
        ids_already_checked = []
        for p_id in mutual_wish_pool:
            ids_already_checked.append(p_id)
            for w_id in mutual_wish_pool:
                if p_id is not w_id:
                    p = anonymous_list[p_id]
                    p_wish_list = p[1]
                    w = anonymous_list[w_id]
                    w_wish_list = w[1]
                    if(w_id not in ids_already_checked):
                        for item in ids_already_checked:
                            if not self.are_wishes_mutual(item, w_id, anonymous_list[item][1], w_wish_list) and item not in to_be_removed:
                                to_be_removed.append(item)
                        if not self.are_wishes_mutual(p_id, w_id, p_wish_list, w_wish_list):
                            to_be_removed.append(w_id)
                        ids_already_checked.append(w_id)
        self.remove_items_from_pool(to_be_removed, mutual_wish_pool)
    
    def remove_items_from_pool(self, to_be_removed, mutated_list):
        for item in to_be_removed:
            if item in mutated_list:
                mutated_list.remove(item)
    
    # returns: true if is already added. Currently this does not handle any edge cases 
    # and assumes that mutual wish pool has same items if atleast one of the said items is the same
    def remove_items_already_in_some_sub_pool_from_current_wish_pool(self, sub_pool, mutual_wish_pool, anonymous_list):
        to_be_removed = []
        for pool in sub_pool:
            for p_id in mutual_wish_pool:
                if p_id in pool:
                    to_be_removed.append(p_id)
        for item in to_be_removed:
            if item in mutual_wish_pool:
                mutual_wish_pool.remove(item)
                    
                    
                                    
                    
                    
            
    def are_wishes_mutual(self, p_id, w_id, p_wish_list, w_wish_list):
        return p_id in w_wish_list and w_id in p_wish_list       
        
    def is_id_in_pool(self, p_id, pool):
        return p_id in pool
        
    #TODO remove    
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
    def deprecated_create_mutual_wishes_groups(self, wish_pools, anonymous_list):
        print('Started creating all mutual wishes pools')
        all_mutual_wishes_pools = []
        for pool in wish_pools:
            sub_pool = []
            to_be_removed_from_sub_pool = []
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
                        # Go through all sub lists in sub_pool
                        for item in sub_pool:
                            # If checked p is already added in some pool, add those id's to mutual wish pool
                            if checked_p_id in item:
                                to_be_removed_from_sub_pool.append(item)
                                # If e.g. participants 1 and 7 has mutually wished to sit next to each other,
                                # and 7 does not share any other 1's mutual wishes, 
                                # 7 and 1 should be set to sit next to each other. 
                                # Look from tests a example of this!
                                for c_index, id_in_item in enumerate(item):
                                    if id_in_item == checked_p_id:
                                        changed_index = c_index
                                        break
                                if(changed_index):
                                    # Change participant to be on the edge of
                                    # already created mutual wishes list
                                    #TODO change this to be less expensive copy method
                                    item_copy = copy.deepcopy(item)
                                    tpm = item_copy[changed_index]
                                    item_copy[changed_index] = item_copy[len(item)-1]
                                    item_copy[len(item_copy)-1] = tpm

                                # Extend already created mutual group to contain the new addition
                                mutual_wish_pool.extend(item_copy)
                                
                        mutual_wish_pool.append(checked_w_id)
                        already_added_ids.append(checked_w_id)
                if mutual_wish_pool:
                    mutual_wishes_without_duplicates = list(OrderedDict.fromkeys(mutual_wish_pool))
                    sub_pool.append(mutual_wishes_without_duplicates)
            # Delete duplicate lists that have been added with extension to some other list item
            # This is done in this way because mutating a list that is currently looped is discouraged.
            for dele in to_be_removed_from_sub_pool:
                # If wishes is looped through, there might be a situation where to_be_removed_sub_pool is
                # appended first e.g. [1,2] and after that [1,2,3] before appending that list to sub pool
                if(dele in sub_pool):
                    sub_pool.remove(dele)
            all_mutual_wishes_pools.append(sub_pool)
        self.all_mutual_wishes_pools = all_mutual_wishes_pools
        print('all mutual wishes pools has been created')
