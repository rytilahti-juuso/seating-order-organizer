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
        self.generate_simple_order()
        
    def generate_simple_order(self):
        for i in range(0, 100):
            if(i % 2 == 0):
                self.generated_names.append(self.male_first_names[i])
            else:
                self.generated_names.append(self.female_first_names[i])

if __name__:
    print("Data generator is run in namespace")
    d = DataGenerator()
    print(d.generated_names)
    #print(d.female_first_names)
    #print(d.surnames)