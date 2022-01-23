# -*- coding: utf-8 -*-
import pandas as pd


class DataGenerator(object):
    def __init__(self):
        self.data_size= 20
        self.max_data_size = 141 # Maximum data size with current parsing setting that can be used without firstname duplicates in men and women
        self.male_first_names = pd.read_excel ('etunimitilasto-2021-02-05-dvv.xlsx', sheet_name='Miehet ens')["Etunimi"]
        self.female_first_names  = pd.read_excel ('etunimitilasto-2021-02-05-dvv.xlsx', sheet_name='Naiset kaikki')["Etunimi"]
        self.surnames = pd.read_excel ('sukunimitilasto-2021-02-05-dvv.xlsx', sheet_name='Nimet')["Sukunimi"]
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
    
    # Write_new_dummy_data_to_target_excel This should be called only when you want to create external excel from pregenerated data. Added for convenience.
    #name and friend list format: [['Juha Korhonen', ['Helena Korhonen', 'Matti Korhonen', 'Johanna Korhonen', 'Mikko Korhonen']], ...]
    #Requires that the target exists #TODO create a new file if target file does not exist
    #NOTE: #FIXME #TODO You may need to import the file with LibreOffice Calc and change it to correct format from .xlsx text import.
    def write_new_dummy_data_to_target_excel(self, name_and_friend_list):
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
        dataframe.to_excel('input-participant-and_wishing-list.xlsx', index = False)