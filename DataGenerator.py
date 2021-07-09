# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 16:00:54 2021

@author: rytil
"""
import pandas as pd

class DataGenerator(object):
    def __init__(self):
        self.male_first_names = pd.read_excel (r'C:\Users\rytil\Documents\Github\seating-order-organizer\etunimitilasto-2021-02-05-dvv.xlsx', sheet_name='Miehet kaikki')["Etunimi"]
        self.female_first_names  = pd.read_excel (r'C:\Users\rytil\Documents\Github\seating-order-organizer\etunimitilasto-2021-02-05-dvv.xlsx', sheet_name='Naiset kaikki')["Etunimi"]
        self.surnames = pd.read_excel (r'C:\Users\rytil\Documents\Github\seating-order-organizer\sukunimitilasto-2021-02-05-dvv.xlsx', sheet_name='Nimet')["Sukunimi"]
        self.generated_names = []
        self.name_and_friend_list = []
        self.generate_unique_names()
        self.generate_name_and_friend_list()
    
    # Generate unique names for participants
    def generate_unique_names(self):
        surname_index = 0 # Same surnames for every group that has asked each other as seating company. This is simply for convenience and easier checkming later the results of seating organizer algorithm by hand
        for i in range(0, 100):   
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

class ScoreCalculation(object):
    def __init__(self, name_and_friend_list, male_first_names):
        self.name_and_friend_list = name_and_friend_list
        self.male_first_names = male_first_names
        self.baseline_score = 0 # Generated ny shuffling the perfect order list
        self.best_score = 0
        
        self.best_order = []
        
        # Temporary solution, wil be deleted when score calcucalation is done
        for i in range(0, len(name_and_friend_list)):
            name = name_and_friend_list[i][0]
            self.best_order.append(name)
            
        self.generate_empty_score_table_2d()
            
    def generate_empty_score_table_2d(self):
        self.score_table_2d= []
        for i in range(0, len(self.best_order)):
            tmp= []
            for j in range(0, len(self.best_order) ):
                tmp.append(0)
            self.score_table_2d.append(tmp)
    
    def calculate_score(self):
        print("asd")
        for i in range(0, len(self.best_order)):
            if(i % 2== 0):
                print("is man")
                # check two previous index and three next if exists
                for j in range(i-3, i+2):
                    checked_index = i+j
                    if(checked_index < len(self.best_order) and checked_index > 0):
                        print("Now is time to check")
            else:
                print("Is woman")
                     # check three previous index and two next if exists

            
if __name__:
    print("Data generator is run in namespace")
    d = DataGenerator()
    print(d.generated_order[10][0])
    print(d.generated_order[10][1])
    #print(d.female_first_names)
    #print(d.surnames)