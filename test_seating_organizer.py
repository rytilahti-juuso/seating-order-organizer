# -*- coding: utf-8 -*-

import unittest
from data_generator import ParticipantFactory, Participant, PoolCreation
from dataclasses import FrozenInstanceError

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

# How duplicate name is handeld?

####################################
#           Participant
####################################

class TestParticipant(unittest.TestCase):

    
    def test_participate_creation_works(self):
        factory = ParticipantFactory()
        participant_created_in_factory = factory.create_participant_from_given_name(['Matti Meikäläinen',
                ['Mikki Hiiri', 'Minni Hiiri' , 'Hessu Hopo']], 10) 
        participant_created_manually = Participant(10, 'Matti Meikäläinen', 'Matti', 'Meikäläinen', 'mattimeikäläinen', False, ['Mikki Hiiri', 'Minni Hiiri' , 'Hessu Hopo'],['mikkihiiri', 'minnihiiri' , 'hessuhopo'])
        #Check that all fields that matter match (is_man is not currently used)
        #Check that name is equal
        self.assertEqual(participant_created_in_factory.first_name, participant_created_manually.first_name)
        self.assertEqual(participant_created_in_factory.surname, participant_created_manually.surname)
        self.assertEqual(participant_created_in_factory.full_name, participant_created_manually.full_name)
        self.assertEqual(participant_created_in_factory.name_without_typos, participant_created_manually.name_without_typos)
        
        # Check that parsing wishing list works
        self.assertEqual(participant_created_in_factory.seating_wish_list, participant_created_manually.seating_wish_list)
        self.assertEqual(participant_created_in_factory.seating_wish_list_without_spaces_and_caps, participant_created_manually.seating_wish_list_without_spaces_and_caps)
        
        # Check that the id is set
        self.assertEqual(participant_created_in_factory.id, participant_created_manually.id)
    
    # Dataclass should always be frozen, lists can be mutated, but you should
    # never mutate the lists in Participant objects once Participant object is
    # created! It might cause huge problems later!
    def test_that_participant_object_cant_be_mutated(self):
        factory = ParticipantFactory()
        participant_created_in_factory = factory.create_participant_from_given_name(['Matti Meikäläinen',
                ['Mikki Hiiri', 'Minni Hiiri' , 'Hessu Hopo']], 0)
        with self.assertRaises(FrozenInstanceError):
            participant_created_in_factory.full_name = 'Name modification'
        with self.assertRaises(FrozenInstanceError):
            participant_created_in_factory.first_name = 'Name modification'
        with self.assertRaises(FrozenInstanceError):
            participant_created_in_factory.surname = 'Name modification'
        with self.assertRaises(FrozenInstanceError):
            participant_created_in_factory.name_without_typos = 'Name modification'
        with self.assertRaises(FrozenInstanceError):
            participant_created_in_factory.id = 2
    
    def test_get_name_without_extra_spaces(self):
        factory = ParticipantFactory()
        self.assertEqual(factory.get_name_without_extra_spaces("    Matti    Meikäläinen   "), "Matti Meikäläinen")
        self.assertEqual(factory.get_name_without_extra_spaces(" Matti Meikäläinen   "), "Matti Meikäläinen")
        self.assertEqual(factory.get_name_without_extra_spaces("    Matti Matias Meikäläinen   "), "Matti Matias Meikäläinen")
        # with tab
        self.assertEqual(factory.get_name_without_extra_spaces("    Matti  Meikäläinen   "), "Matti Meikäläinen")
    
    def test_get_first_names(self):
        factory = ParticipantFactory()
        self.assertEqual(factory.get_first_names("Matti Meikäläinen"), "Matti")
        self.assertEqual(factory.get_first_names("Matti Matias Meikäläinen"), "Matti Matias")
        self.assertEqual(factory.get_first_names("Niño Meikäläinen"), "Niño")
        self.assertNotEqual(factory.get_first_names("Matti Meikäläinen"), "matti")
        self.assertEqual(factory.get_first_names("Matti"), "Matti")
    
    def test_get_surname(self):
        factory = ParticipantFactory()
        self.assertEqual(factory.get_surname('Matti Matias Meikäläinen'), 'Meikäläinen')
        self.assertEqual(factory.get_surname('Matti Meikäläinen'), 'Meikäläinen')
        self.assertEqual(factory.get_surname('Matti Matias Ordoñez'), 'Ordoñez')
        self.assertNotEqual(factory.get_surname('Matti Matias Meikäläinen'), 'meikäläinen')
        self.assertEqual(factory.get_surname('Matti Matias Meikäläinen-Esimerkki'), 'Meikäläinen-Esimerkki')


    def test_get_participant_name_without_spaces_and_capitals(self):
        factory = ParticipantFactory()
        self.assertEqual(factory.get_name_without_spaces_and_caps("Matti Meikäläinen"), "mattimeikäläinen")
        self.assertEqual(factory.get_name_without_spaces_and_caps("Matti     Meikäläinen"), "mattimeikäläinen")
        self.assertEqual(factory.get_name_without_spaces_and_caps("MATTI MEIKÄLÄINEN"), "mattimeikäläinen")
        self.assertEqual(factory.get_name_without_spaces_and_caps("Matti Matias Meikäläinen"), "mattimatiasmeikäläinen")
        self.assertEqual(factory.get_name_without_spaces_and_caps("Matti     Matias        Meikäläinen"), "mattimatiasmeikäläinen")
    
    def test_get_wish_list_without_spaces_and_capitals(self):
        factory = ParticipantFactory()
        self.assertEqual(factory.get_wish_list_without_spaces_and_caps(['Mikki Hiiri', 'Minni Hiiri']), ['mikkihiiri', 'minnihiiri'])
        self.assertEqual(factory.get_wish_list_without_spaces_and_caps(['MikkI Hiiri', 'Minni HIIri']), ['mikkihiiri', 'minnihiiri'])
        self.assertEqual(factory.get_wish_list_without_spaces_and_caps(['Mikki   Hiiri', 'Minni    Hiiri']), ['mikkihiiri', 'minnihiiri'])
        self.assertEqual(factory.get_wish_list_without_spaces_and_caps([]), [])
    
# dataclass object has correct values in default case

# man-name list is List<string> type instead of any other data types (because of use of "in" operator)


#for every name field:
    
    # is_man is working with correct, test with man and woman names

####################################
#           PoolCreation
####################################

class TestPoolCreation(unittest.TestCase):
    
    def setUp(self):
        self.anonymous_list= [[0, [1,2,3]], [1, [0,2,3]], [2, [0,1,3]], [3, [0,1,2]], [4, [5,6]], [5, [4]], [6, [5]], [7, []]]
        self.anonymous_deeply_nested = [ [0, [1]], [1, [2]], [2, [3]], [3, [4]], [4, [5]], [5, [4]], [6, []] ]
    
    
    def test_create_pools(self):
        pool_creation = PoolCreation()
        pool_creation.create_pools(self.anonymous_list)
        self.assertEqual(pool_creation.wish_pools, [[0, 1, 2, 3], [4, 5, 6], [7]])
        self.assertEqual(pool_creation.all_mutual_wishes_pools, [[[0, 1, 2, 3]], [[4, 5], [6]], [[7]]])
        
    
    def test_create_all_wishes_to_same_group(self):
        pool_creation = PoolCreation()
        pool_creation.create_all_wishes_to_same_group(self.anonymous_list)
        all_wishes_in_same_group_pool = pool_creation.wish_pools
        self.assertEqual(all_wishes_in_same_group_pool, [[0, 1, 2, 3], [4, 5, 6], [7]])
        
        deeply_nested_pool_creation = PoolCreation()
        deeply_nested_pool_creation.create_all_wishes_to_same_group(self.anonymous_deeply_nested)
        deeply_nested_all_wishes = deeply_nested_pool_creation.wish_pools
        self.assertEqual(deeply_nested_all_wishes, [[0, 1, 2, 3, 4, 5], [6]])
        
        #test also deeply nested wishes
        
    def test_create_mutual_wishes_groups(self):
        pool_creation = PoolCreation()
        all_wishes_in_same_group_pool = [[0, 1, 2, 3], [4, 5, 6], [7]]
        pool_creation.create_mutual_wishes_groups(all_wishes_in_same_group_pool, self.anonymous_list)
        mutual_wishes_pools = pool_creation.all_mutual_wishes_pools
        self.assertEqual(mutual_wishes_pools, [[[0, 1, 2, 3]], [[4, 5], [6]], [[7]]])
        
        
        
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