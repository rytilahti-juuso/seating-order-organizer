# -*- coding: utf-8 -*-

# This is simple test case template for writing the tests later when I have time

####################################
#           DataGenerator
####################################

# Everyone who has asked each other as table company share the same last name

# No first name duplicates in generating highest allowed amount of participants


####################################
#           Participant
####################################

# dataclass object has correct values in default case

# man-name list is List<string> type instead of any other data types (because of use of "in" operator)

#fullname_has_multiple_spaces

# How duplicate name is handeld?

#for every name field:
    
    # Name has finnish special letters

    # Name has spanish special letters 

    # name_without_typos is correct with all cases
    
    # is_man is working with correct, test with man and woman names


####################################
#           ScoreCalculation
####################################

# Special case: first participants are calculated correctly

# Added gender score is calculated correctly in ideal case (all partipants are in order, man, woman, man woman)

# Added gender score is calculated correctly not in ideal case when:
    # Both are men
    # Both are women
    # Different relational positions (ex. <man, woman, man, man>, <man, man, man, woman> etc.)