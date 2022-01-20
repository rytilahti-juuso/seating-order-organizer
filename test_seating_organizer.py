# -*- coding: utf-8 -*-

import unittest
from data_generator import NecessaryListsFactory, ParticipantFactory, Participant, PoolCreation
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
class TestNecessaryListsFactory(unittest.TestCase):
    def setUp(self):
        # Juha and Helena asked mutual and other Korhonen asked them also.
        # Lehtoset are combined with Heikkilä
        # Johanna Korhonen has special wish
        self.name_and_wish_list =[['Juha Korhonen', ['Helena Korhonen']]
                                  , ['Helena Korhonen', ['Juha Korhonen']]
                                  , ['Matti Korhonen', ['Juha Korhonen', 'Helena Korhonen', 'Johanna Korhonen', 'Mikko Korhonen']]
                                  , ['Johanna Korhonen', ['Juha Korhonen', 'Helena Korhonen', 'Matti Korhonen', 'Mikko Korhonen']]
                                  , ['Mikko Korhonen', ['Juha Korhonen', 'Helena Korhonen', 'Matti Korhonen', 'Johanna Korhonen. I wish not to sit next to person named xx.']]
                                  , ['Marjatta Hämäläinen', ['Antti Hämäläinen', 'Kristiina Hämäläinen', 'Mika Hämäläinen', 'Liisa Hämäläinen']]
                                  , ['Antti Hämäläinen', ['Marjatta Hämäläinen', 'Kristiina Hämäläinen', 'Mika Hämäläinen', 'Liisa Hämäläinen']]
                                  , ['Kristiina Hämäläinen', ['Marjatta Hämäläinen', 'Antti Hämäläinen', 'Mika Hämäläinen', 'Liisa Hämäläinen']]
                                  , ['Mika Hämäläinen', ['Marjatta Hämäläinen', 'Antti Hämäläinen', 'Kristiina Hämäläinen', 'Liisa Hämäläinen']]
                                  , ['Liisa Hämäläinen', ['Marjatta Hämäläinen', 'Antti Hämäläinen', 'Kristiina Hämäläinen', 'Mika Hämäläinen']]
                                  , ['Pekka Lehtonen', ['Sofia Lehtonen', 'Heikki Lehtonen', 'Maarit Lehtonen', 'Seppo Lehtonen']]
                                  , ['Sofia Lehtonen', ['Pekka Lehtonen', 'Heikki Lehtonen', 'Maarit Lehtonen', 'Seppo Lehtonen']]
                                  , ['Heikki Lehtonen', ['Pekka Lehtonen', 'Sofia Lehtonen', 'Maarit Lehtonen', 'Seppo Lehtonen']]
                                  , ['Maarit Lehtonen', ['Pekka Lehtonen', 'Sofia Lehtonen', 'Heikki Lehtonen', 'Seppo Lehtonen']]
                                  , ['Seppo Lehtonen', ['Pekka Lehtonen', 'Sofia Lehtonen', 'Heikki Lehtonen', 'Maarit Lehtonen', 'Annikki Heikkilä']]
                                  , ['Don Diego de la Vega', []]
                                  , ['Annikki Heikkilä', ['Sami Heikkilä', 'Katariina Heikkilä', 'Marko Heikkilä', 'Seppo Lehtonen']]
                                  , ['Sami Heikkilä', ['Annikki Heikkilä', 'Katariina Heikkilä', 'Marko Heikkilä', 'Marja Heikkilä']]
                                  , ['Katariina Heikkilä', ['Annikki Heikkilä', 'Sami Heikkilä', 'Marko Heikkilä', 'Marja Heikkilä']]
                                  , ['Marko Heikkilä', ['Annikki Heikkilä', 'Sami Heikkilä', 'Katariina Heikkilä', 'Marja Heikkilä']]
                                  , ['Marja Heikkilä', ['Annikki Heikkilä', 'Sami Heikkilä', 'Katariina Heikkilä', 'Marko Heikkilä']]
                                  ]
        self.nlf = NecessaryListsFactory(self.name_and_wish_list)
    
    def test_will_detect_duplicates_and_stop_execution(self):
        #Sofia Lehtonen is now Pekka Lehtonen, Sofia Lehtonen is still on peoples wishlist
        name_and_wishlist_with_duplicates = [['Juha Korhonen', ['Helena Korhonen', 'Matti Korhonen', 'Johanna Korhonen', 'Mikko Korhonen']]
                                  , ['Helena Korhonen', ['Juha Korhonen', 'Matti Korhonen', 'Johanna Korhonen', 'Mikko Korhonen']]
                                  , ['Matti Korhonen', ['Juha Korhonen', 'Helena Korhonen', 'Johanna Korhonen', 'Mikko Korhonen']]
                                  , ['Johanna Korhonen', ['Juha Korhonen', 'Helena Korhonen', 'Matti Korhonen', 'Mikko Korhonen']]
                                  , ['Mikko Korhonen', ['Juha Korhonen', 'Helena Korhonen', 'Matti Korhonen', 'Johanna Korhonen']]
                                  , ['Marjatta Hämäläinen', ['Antti Hämäläinen', 'Kristiina Hämäläinen', 'Mika Hämäläinen', 'Liisa Hämäläinen']]
                                  , ['Antti Hämäläinen', ['Marjatta Hämäläinen', 'Kristiina Hämäläinen', 'Mika Hämäläinen', 'Liisa Hämäläinen']]
                                  , ['Kristiina Hämäläinen', ['Marjatta Hämäläinen', 'Antti Hämäläinen', 'Mika Hämäläinen', 'Liisa Hämäläinen']]
                                  , ['Mika Hämäläinen', ['Marjatta Hämäläinen', 'Antti Hämäläinen', 'Kristiina Hämäläinen', 'Liisa Hämäläinen']]
                                  , ['Liisa Hämäläinen', ['Marjatta Hämäläinen', 'Antti Hämäläinen', 'Kristiina Hämäläinen', 'Mika Hämäläinen']]
                                  , ['Pekka Lehtonen', ['Sofia Lehtonen', 'Heikki Lehtonen', 'Maarit Lehtonen', 'Seppo Lehtonen']]
                                  , ['Pekka Lehtonen', ['Pekka Lehtonen', 'Heikki Lehtonen', 'Maarit Lehtonen', 'Seppo Lehtonen']]
                                  , ['Heikki Lehtonen', ['Pekka Lehtonen', 'Sofia Lehtonen', 'Maarit Lehtonen', 'Seppo Lehtonen']]
                                  , ['Maarit Lehtonen', ['Pekka Lehtonen', 'Sofia Lehtonen', 'Heikki Lehtonen', 'Seppo Lehtonen']]
                                  , ['Seppo Lehtonen', ['Pekka Lehtonen', 'Sofia Lehtonen', 'Heikki Lehtonen', 'Maarit Lehtonen']]
                                  , ['Annikki Heikkilä', ['Sami Heikkilä', 'Katariina Heikkilä', 'Marko Heikkilä', 'Marja Heikkilä']]
                                  , ['Sami Heikkilä', ['Annikki Heikkilä', 'Katariina Heikkilä', 'Marko Heikkilä', 'Marja Heikkilä']]
                                  , ['Katariina Heikkilä', ['Annikki Heikkilä', 'Sami Heikkilä', 'Marko Heikkilä', 'Marja Heikkilä']]
                                  , ['Marko Heikkilä', ['Annikki Heikkilä', 'Sami Heikkilä', 'Katariina Heikkilä', 'Marja Heikkilä']]
                                  , ['Marja Heikkilä', ['Annikki Heikkilä', 'Sami Heikkilä', 'Katariina Heikkilä', 'Marko Heikkilä']]
                                  ]
    
    def test_that_wishes_are_splitted_by_comma_semicolon_and_dot(self):
        pass
    
    def test_all_lists_are_in_sync(self):
        print(self.nlf.anonymous_list)
        self.assertEqual(self.nlf.all_pools,
                         [[[0, 1], [2, 3, 4]], [[5, 6, 7, 8, 9]], [[15]], [[10, 11, 12, 13, 14], [16], [17, 18, 19]
                            , [20]]])
        self.assertEqual(self.nlf.anonymous_list, [[0, [1], False], [1, [0], False], [2, [3, 4], False]
                                                   , [3, [0, 1, 2, 4], False], [4, [0, 1, 2], False]
                                                   , [5, [6, 7, 8, 9], False], [6, [5, 7, 8, 9], False]
                                                   , [7, [5, 6, 8, 9], False], [8, [5, 6, 7, 9], False]
                                                   , [9, [5, 6, 7, 8], False], [10, [11, 12, 13, 14], False]
                                                   , [11, [10, 12, 13, 14], False], [12, [10, 11, 13, 14], False]
                                                   , [13, [10, 11, 12, 14], False], [14, [10, 11, 12, 13, 16], False]
                                                   , [15, [], False], [16, [17, 18, 19, 14], False]
                                                   , [17, [16, 18, 19, 20], False], [18, [16, 17, 19, 20], False]
                                                   , [19, [16, 17, 18, 20], False], [20, [16, 17, 18, 19], False]])
        
    
    def test_if_wish_does_not_exist(self):
        pass

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
        self.anonymous_list= [[0, [1,2,3]], [1, [0,2,3]], [2, [0,1,3]], [3, [0,1,2]], [4, [5,6]], [5, [4]], [6, [5, 7]], [7, [6]], [8, []]]
        self.anonymous_deeply_nested = [ [0, [1]], [1, [2]], [2, [3]], [3, [4]], [4, [5]], [5, [4]], [6, []] ]
    
    
    def test_create_pools(self):
        pool_creation = PoolCreation()
        pool_creation.create_pools(self.anonymous_list)
        self.assertEqual(pool_creation.wish_pools, [[0, 1, 2, 3], [4, 5, 6, 7], [8]])
        self.assertEqual(pool_creation.all_mutual_wishes_pools, [[[0, 1, 2, 3]], [[4, 5], [6,7]], [[8]]])
        
    
    def test_create_all_wishes_to_same_group(self):
        pool_creation = PoolCreation()
        pool_creation.create_all_wishes_to_same_group(self.anonymous_list)
        all_wishes_in_same_group_pool = pool_creation.wish_pools
        self.assertEqual(all_wishes_in_same_group_pool, [[0, 1, 2, 3], [4, 5, 6, 7], [8]])
        
        #test also deeply nested wishes
        # If participant have wish and that wish have someone he wished, add them to same pool, and support for even deeper nesting.
        #  e.g. [0, [1, 2]],[1, [0, 2, 5]] and [5, [7]] will be in the same pool (all_pools = [ [0,1,2,5,7], [pool2],... [poolN] ])
        deeply_nested_pool_creation = PoolCreation()
        deeply_nested_pool_creation.create_all_wishes_to_same_group(self.anonymous_deeply_nested)
        deeply_nested_all_wishes = deeply_nested_pool_creation.wish_pools
        self.assertEqual(deeply_nested_all_wishes, [[0, 1, 2, 3, 4, 5], [6]])
        
        
        
    def test_create_mutual_wishes_groups(self):
        pool_creation = PoolCreation()
        all_wishes_in_same_group_pool = [[0, 1, 2, 3], [4, 5, 6, 7], [8]]
        pool_creation.create_mutual_wishes_groups(all_wishes_in_same_group_pool, self.anonymous_list)
        mutual_wishes_pools = pool_creation.all_mutual_wishes_pools
        # Specifies mutual and non mutual wishes to different array (e.g. example below: [[4, 5], [6, 7]]).
        self.assertEqual(mutual_wishes_pools, [[[0, 1, 2, 3]], [[4, 5], [6, 7]], [[8]]])
        
# Check that there are no duplicates in the pools.


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