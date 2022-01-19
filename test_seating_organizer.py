# -*- coding: utf-8 -*-

import unittest
import DataGenerator

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

class TestParticipant(unittest.TestCase):

    
    def test_participate_creation_works(self):
        factory = DataGenerator.ParticipantFactory()
        participant_created_in_factory = factory.create_participant_from_given_name(['Matti Meikäläinen',
                ['Mikki Hiiri', 'Minni Hiiri' , 'Hessu Hopo']], 0) 
        participant_created_manually = DataGenerator.Participant(0, 'Matti Meikäläinen', 'Matti', 'Meikäläinen', 'mattimeikäläinen', False, ['Mikki Hiiri', 'Minni Hiiri' , 'Hessu Hopo'],['mikkihiiri', 'minnihiiri' , 'hessuhopo'])
        #Check that all fields that matter match (is_man is not currently used)
        #Check that name is equal
        self.assertEqual(participant_created_in_factory.first_name, participant_created_manually.first_name)
        self.assertEqual(participant_created_in_factory.surname, participant_created_manually.surname)
        self.assertEqual(participant_created_in_factory.full_name, participant_created_manually.full_name)
        self.assertEqual(participant_created_in_factory.name_without_typos, participant_created_manually.name_without_typos)
        
        # Check that parsing wishing list works
        self.assertEqual(participant_created_in_factory.seating_wish_list, participant_created_manually.seating_wish_list)
        self.assertEqual(participant_created_in_factory.seating_wish_list_without_spaces_and_caps, participant_created_manually.seating_wish_list_without_spaces_and_caps)

    def test_participant_object_cant_be_mutated(self):
        pass
    
    def test_get_first_namess(self):
        factory = DataGenerator.ParticipantFactory()
        self.assertEqual(factory.get_first_names("Matti Meikäläinen"), "Matti")
        self.assertEqual(factory.get_first_names("Matti Matias Meikäläinen"), "Matti Matias")
        self.assertEqual(factory.get_first_names("Niño Meikäläinen"), "Niño")
        self.assertNotEqual(factory.get_first_names("Matti Meikäläinen"), "matti")
    
    def test_generate_surname(self):
        factory = DataGenerator.ParticipantFactory()
        self.assertEqual(factory.generate_surname('Matti Matias Meikäläinen'), 'Meikäläinen')
        self.assertEqual(factory.generate_surname('Matti Meikäläinen'), 'Meikäläinen')
        self.assertEqual(factory.generate_surname('Matti Matias Ordoñez'), 'Ordoñez')
        self.assertNotEqual(factory.generate_surname('Matti Matias Meikäläinen'), 'meikäläinen')
        self.assertEqual(factory.generate_surname('Matti Matias Meikäläinen-Esimerkki'), 'Meikäläinen-Esimerkki')


    def test_generate_participant_name_without_spaces_and_capitals(self):
        factory = DataGenerator.ParticipantFactory()
        self.assertEqual(factory.generate_name_without_spaces_and_caps("Matti Meikäläinen"), "mattimeikäläinen")
        self.assertEqual(factory.generate_name_without_spaces_and_caps("Matti     Meikäläinen"), "mattimeikäläinen")
        self.assertEqual(factory.generate_name_without_spaces_and_caps("MATTI MEIKÄLÄINEN"), "mattimeikäläinen")
        self.assertEqual(factory.generate_name_without_spaces_and_caps("Matti Matias Meikäläinen"), "mattimatiasmeikäläinen")
    
    def test_generate_wish_list_without_spaces_and_capitals(self):
        pass
    
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
#           PoolCreation
####################################

# Check that there are no duplicates in the pools.

# Add all wishes to same pool.

# If participant have wish and that wish have someone he wished, add them to same pool, and support for even deeper nesting.
#  e.g. [0, [1, 2]],[1, [0, 2, 5]] and [5, [7]] will be in the same pool (all_pools = [ [0,1,2,5,7], [pool2],... [poolN] ])

# TODO: Specify mutual and non mutual wishes to different array.

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
    
if __name__ == '__main__':
    #Will run all tests
    unittest.main()