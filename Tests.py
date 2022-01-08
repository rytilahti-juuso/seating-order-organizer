# -*- coding: utf-8 -*-

# This is simple test case template for writing the tests later when I have time

####################################
#           DataGenerator
####################################

# Everyone who has asked each other as table company share the same last name

# No first name duplicates in generating highest allowed amount of participants


####################################
#           NecessaryListFactory
####################################

# Test that all lists are in sync

# Test that asking for a wish that is not a participant (e.g. old students or bigger typos) does not raise an error

# Participant having no wishes should not create an error 

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

# In 2d Table how participants own score should be handeld (should it be put to be -1)

# Added gender score is calculated correctly not in ideal case when:
    # Both are men
    # Both are women
    # Different relational positions (ex. <man, woman, man, man>, <man, man, man, woman> etc.)