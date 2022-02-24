# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 16:00:54 2021

@author: rytil
© 2021 Juuso Rytilahti.  All rights reserved.
"""
import pandas as pd
import json
from sorting_algorithm import NecessaryListsFactory
from dummy_data_generation import DataGenerator
        
class ImportDataFromExcel(object):
    def __init__(self):
        print("Importing data from excel")
        self.df = pd.read_excel ('input-participant-and_wishing-list.xlsx', header=None, names=('Name', 'Wishes'))
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

    ##################################
    #    Handle duplicates STARTS    #
    ##################################
        


class ExcelStyleFormatting(object):
    
    
    ################################################
    #    Create participants style format STARTS   #
    ################################################
    
    def __init__(self):
        # Add empty cells in the export excel after these ids. key: participant_id, value: how many empty spaces are needed
         self.add_empty_cells_after_these_ids = {} 
    
    #Generate color rules for each participant. When this is called all lists must be in sync already.
    # Each subgroup will have rotating background color. People with special wishes will have their cell's font color changed to red.
    def generate_color_rules(self, participants, participant_ids_with_special_wishes, all_pools, names_of_mutuals_outside_own_mutual_pool):
        dict_of_participants_colors = {} # key: participants full name, value: style formatting settings
        dict_of_participants_colors = self.set_different_font_color_if_has_mutual_wish_outside_own_group(participants, dict_of_participants_colors, names_of_mutuals_outside_own_mutual_pool)
        dict_of_participants_colors = self.set_special_font_color_if_participant_has_special_wishes(participants, participant_ids_with_special_wishes, dict_of_participants_colors)    
        self.set_background_color_and_append_empty_cells_after_necessary_ids(participants, all_pools, dict_of_participants_colors)
        return dict_of_participants_colors
    
    def set_different_font_color_if_has_mutual_wish_outside_own_group(self, participants, dict_of_participants_colors, names_of_mutuals_outside_own_mutual_pool):
        for sub_pool in names_of_mutuals_outside_own_mutual_pool:
            for i, pool in enumerate(sub_pool):
                color = ''
                if(i % 5 == 0):
                    color = 'color: blue;'
                elif(i % 5 == 1):
                    color = 'color: yellow;'
                elif(i % 5 == 2):
                    color = 'color: orange;'
                elif(i % 5 == 3):
                    color = 'color: purple;'
                elif(i % 5 == 4):
                    color = 'color: green;'
                for name in pool:
                    if name in dict_of_participants_colors:
                        dict_of_participants_colors += color
                    else:    
                        dict_of_participants_colors[name] = color
        return dict_of_participants_colors
    
    # When this is called all lists must be in sync already. Font is changed to red, the default font color is black.
    def set_special_font_color_if_participant_has_special_wishes(self,participants, participant_ids_with_special_wishes, dict_of_participants_colors):
        for i in range(0, len(participant_ids_with_special_wishes)):
            name = participants[participant_ids_with_special_wishes[i]].full_name
            dict_of_participants_colors[name] = 'color: red;' #TODO change that this changes border instead of font color
        return dict_of_participants_colors

    # Set background color by subgroup. When this is called all lists must be in sync already
    def set_background_color_and_append_empty_cells_after_necessary_ids(self, participants, mutual_pools, dict_of_participants_colors):
        rotating_background_color_index = -1
        # Count of currently used cells. 
        # Is used to append a correct amount of empty cells after a non-mutual wish group is looped through.
        count_of_cells = 0
        for i, sub_pool in enumerate(mutual_pools):
            rotating_background_color_index += 1
            for j, mutual_pool in enumerate(sub_pool):
                if len(sub_pool) != 1 and j != 0:
                    rotating_background_color_index += 1
                for k, p_id in enumerate(mutual_pool):
                    count_of_cells += 1
                    background_color = ''
                    background_color = self.get_background_color_by_index(rotating_background_color_index)
                    self.add_background_to_participant(participants, dict_of_participants_colors, p_id, background_color)
                    # is final mutual_pool in sub_pool and id is the final item in the final mutual pool
                    if j == len(sub_pool)-1 and k == len(mutual_pool) - 1:
                        final_p_id = mutual_pool[len(mutual_pool)-1]
                        if count_of_cells % 2 == 0:
                            self.add_empty_cells_after_these_ids[final_p_id] = 2
                            count_of_cells += 2
                        else:
                            self.add_empty_cells_after_these_ids[final_p_id] = 3
                            count_of_cells += 3
    
    # participants = list of participant obkects in order
    # p_id = the id of the participants which has the background change set
    # dict_of_participants_colors: Dictionary of color settings of participants, key:full_name_of_participant, value: style formatting settings
    # background_color: background color added to the styles, is a string in format: 'background-color: #ECDDD0;'
    def add_background_to_participant(self, participants, dict_of_participants_colors, p_id, background_color):
        name = participants[p_id].full_name
        if(name in dict_of_participants_colors):
            dict_of_participants_colors[name] += background_color
        else:    
            dict_of_participants_colors[name] = background_color
    
    def get_background_color_by_index(self, i):
        background_color= ''
        if(i % 5 == 0):
            background_color = 'background-color: #ECDDD0;'
        elif(i % 5 == 1):
            background_color = 'background-color: #92b1b6;'
        elif(i % 5 == 2):
            background_color = 'background-color: #CED2C2;'
        elif(i % 5 == 3):
            background_color = 'background-color: #BFD1DF;'
        elif(i % 5 == 4):
            background_color = 'background-color: #C1BFB5;'
        return background_color
    ################################################
    #    Create participants style format ENDS   #
    ################################################



#Contains data export classes.                         
class ExportData(object):  
    
    # Return: final seating list with empty cells for excel
    # pools: pools that also contain mutual wishes in separate list e.g. [[1,2], [3]]
    def generate_final_seating_excel_format(self, participants, participants_ids_with_special_wishes, mutual_pools, pools, names_of_mutuals_outside_own_mutual_pool):
        excel_style_formatting = ExcelStyleFormatting()
        # names_that_have_special_wishes: participants names that have special wishes. key: name, value: style formatting settings
        self.names_with_color_rules = excel_style_formatting.generate_color_rules(participants, participants_ids_with_special_wishes, mutual_pools, names_of_mutuals_outside_own_mutual_pool)
        self.add_empty_cells_after_these_ids = excel_style_formatting.add_empty_cells_after_these_ids
        anonymous_flat_list = self.flat_mutual_wishes_list(mutual_pools)
                
        result = [] # format, [name1, name2,...nameN]
        #print(anonymous_flat_list)
        for i in range(0, len(anonymous_flat_list)):
            result.append(participants[anonymous_flat_list[i]].full_name)
            # If id is at the end of the subgroup of mutual and non_mutual wishes, append two empty spaces 
            # (so you get a empty column in the excel) between the groups.
            # #TODO This is for the excel export and when this is running on a server backend, please remove this feature or
            # make it optional
            if(anonymous_flat_list[i] in  self.add_empty_cells_after_these_ids):
                number_of_empty_spaces = self.add_empty_cells_after_these_ids[anonymous_flat_list[i]]
                for i in range(number_of_empty_spaces):    
                    result.append("")
        return result
    
    # Returns: flat mutual wish pool list
    def flat_mutual_wishes_list(self, mutual_pools):
        anonymous_flat_list = []
        for big_pool in mutual_pools:
            for pool in big_pool:
                for p_id in pool:
                    anonymous_flat_list.append(p_id)
        return anonymous_flat_list
        
    #data = dictionary which, contains all data, different data groups named e.g.
    #d = {}
    #d["final_seating_order"] = ["Matti Meikäläinen", "Sanni Meikäläinen", "Mikki Hiiri"], the only 1d group
    #d['groups_by_wished'] = [["Matti Meikäläinen", "Sanni Meikäläinen"], ['Mikki Hiiri']], 2d dictionary, value names in that group, key group index.
    # So d['groups_groups_by_wished'][1] = ['Mikki Hiiri']
    # There also can be others groups e.g d['group_by_diet'] or d['group_by_student_union'] which has not yet been implemented.
    # So e.g if d[group_by_student_union]['Asteriski ry'] returns all participants which are members of Asteriski ry 
    # Note: Items on the different data lists should be the participant.full_name.
    #Returns: data as json object
    def get_data_as_json(self, data):
        json_string = json.dumps(data)
        return json_string
    
    # participants_in_correct_order: ["name1","name2",... "nameN"]
    
    def export_data_to_excel(self, nlf):
        final_seating_order_with_correct_excel_formatting = e.generate_final_seating_excel_format(nlf.participant_list, nlf.participants_ids_with_special_wishes, nlf.all_pools, nlf.pc.wish_pools, nlf.names_of_mutuals_outside_own_mutual_pool)
        participants_in_correct_order = final_seating_order_with_correct_excel_formatting
        #TODO At later date this could be made more efficient
        left_side = []
        right_side = []
        for i in range(0, len(participants_in_correct_order)):
            if(i % 2== 0):
                #add to left side
                left_side.append(participants_in_correct_order[i])
            else:
                right_side.append(participants_in_correct_order[i])
        if(len(right_side) < len(left_side)): # ValueError: arrays must all be same length, and since they are added one by one to each side this is the only possible breaking point to produce error
            right_side.append("")
        dictionary = {'left_side': left_side, 'right_side': right_side}  
        df = pd.DataFrame(dictionary)

        self.df = df
        df.style.apply(self.highlight_special_wishes, axis=None).to_excel('output-seating-order.xlsx', sheet_name='seating_order',index=False, engine='openpyxl')
        print('Data export succesfully completed!')
    
    def highlight_special_wishes(self, x):
        #https://stackoverflow.com/questions/54019597/export-styled-pandas-data-frame-to-excel
        #if not match return empty string
        df1 = pd.DataFrame('', index=x.index, columns=x.columns)
        #rewrite values by boolean masks
        #df1['left_side'] = np.where(m1, 'background-color: {}'.format(r), df1['left_side'])
        #df1['right_side'] = np.where(self.lol, 'background-color: red', df1['left_side'])
        color = 'background-color: lightgreen; color: red'
        for i in range(0, len(df1)):
            if(x.at[i, 'left_side'] in self.names_with_color_rules):
                df1.at[i,'left_side'] = self.names_with_color_rules[x.at[i, 'left_side']]
            if(x.at[i, 'right_side'] in self.names_with_color_rules):
                df1.at[i,'right_side'] = self.names_with_color_rules[x.at[i, 'right_side']]
        return df1

    
if __name__:
    print('Code is run trough namespace')
    #d = DataGenerator()
    #nlf = NecessaryListsFactory(d.name_and_friend_list) #Necessary lists factory
    #print(d.name_and_friend_list)
    #print(nlf.anonymous_list)
    #print(nlf.participant_list)
    
    ###IMPORT DUMMY DATA FROM EXCEL AND CREATE POOLS FROM THAT DATA ###################################
    imp = ImportDataFromExcel()
    nlf = NecessaryListsFactory(imp.data)
    e = ExportData()   
    e.export_data_to_excel(nlf)
    ###IMPORT DUMMY DATA FROM EXCEL AND CREATE POOLS FROM THAT DATA ENDS ###################################
    
    #print(poolcreation.wish_pools)
    #s = ScoreCalculation(nlf.anonymous_list, d.male_first_names)
    #print(s.score_table_2d)
    #print(d.generated_order[10]][1)
    #pf = ParticipantFactory()
    #p = pf.create_participant_from_given_name(d.name_and_friend_list[1])
    #print(p)
    #print(s.score_table_2d)
    #print(d.female_first_names)
    #print(d.surnames)