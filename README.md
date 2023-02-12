© 2021 Juuso Rytilahti.  All rights reserved. This code can be altered, forked and used freely by non-profit organizations e.g. different student unions with the permission from the copyright holder as long as authors of the code are credited and a link to the original repository is provided (if original repository is publicly available). 

# seating-order-organizer
A way to generate seating order automatically for sitz or some other event. The main idea of the current version is to ease the work of the one doing the seating planning for sitz and other such events.

Executable version with simpler instructions and less steps to take to use can be found in the file `dist.zip`.


# First Time Setup:
1. If virtualenv is not yet installed, run pip install `pip install virtualenv` .
2. Open command line. Navigate to this repository's folder with command line (e.g. `C:\Users\rytil\Documents\Github\seating-order-organizer`).
3. Run `python -m virtualenv venv`
4. Activate the virtual enviroment, if you're on windows the command is `.\venv\Scripts\activate.bat`, if youre using some other OS (e.g. Mac or Linux) google how to activate the virtualenv enviroment.  
5. Install requirements using `pip install -r requirements.txt`
6. You can run the actual code now using `python excel_import_and_export.py`
7. You should see multiple prints. 
```
Code is run trough namespace
Importing data from excel
Data import has been completed!
pool creation has started
Started creating all-wishes-to-same-group-pools
All wishes to same-group-pools-have-been-created!
Started creating all mutual wishes pools
all mutual wishes pools has been created
Pools have been created!
Data export succesfully completed!
```
If you see only some of the prints, some important code line has been commented out at the bottom of the `excel_import_and_export.py` -file under the `if __name__:` if clause.
Inside there should be the following lines uncommented:
``` python
if __name__:
    print('Code is run trough namespace')
    imp = ImportDataFromExcel()
    nlf = NecessaryListsFactory(imp.data)
    e = ExportData()   
    e.export_data_to_excel(nlf)
```
8. If you see all of the above prints and no errors raise, you are probably fine and you can proceed to start using the script. The most optimal workflow how this script can be utilized is currently described below in the #Workflow section 

Notes about first time setup:
- All excel files should pre-exist before running the code.
- Tests can be run with following command `python test_seating_organizer.py`. Currently the unit tests do not cover the excel import and export classes, score calculation or data generation. They cover the classes found in the `sorting_algorithm.py` -file 
- You can deactivate the virtualenv-enviroment by typing `deactivate` and pressing enter in the command line.

# Workflow:
1. See that the code is running properly using above steps.
2. Open command line. Navigate to this repository's folder with command line (e.g. `C:\Users\rytil\Documents\Github\seating-order-organizer`).
3. Activate the created virtual enviroment by typing `python -m virtualenv venv` into the command line.
4. Copy participants and their wishes to the columns in the file named `input-participant-and_wishing-list.xlsx`.
5. In the command line, run `python excel_import_and_export.py`
6. Check the created `output-seating-order.xlsx` file. Look for are cells where the font is **red**. This means that the participant has special wishes (e.g. "I would like to sit next to the other old students") or they have typos in their wishes. Look in the `input-participant-and_wishing-list.xlsx` and correct the wishes so that they match the names of the participants. If there is someone who has a special wish "I don't want to sit next to person xx" you can leave that wish unaltered. It will not affect functionality of the code, only the font color of the said participants name will be red in the output excel.
7. Run code again with the altered input file using the same command (`python excel_import_and_export.py`).
8. Now open the output and open a **new** empty excel file next to it.
9. Now you can copy names to that new excel file which you just created either one name at a time or in groups using cut and paste (`ctrl + x` and `ctrl +v`). Cut is better than copy because then you avoid accidently placing someone twice to the actual seating chart.
10. Finally do correct style formatting to the excel that you just created (Actual final seating chart): Set all cells to have the following style: background color white, font color black and set border color to be gray. Save the created excel as `my-event-name-year.xslx`.
11. Close the terminal or deactive the enviroment using `deactivate` command. 
12. You're done! Congratz!

# General Notes:
- The names that end up in `output-seating-order.xlsx` file are the ones under the `name`-column in the input excel file.
- If participant has multiple first names (Matti Matias Meikäläinen), his first names are processed together ('Matti Matias'). He then may cause multiple person_has_special wishes flags (currently font color red in excel) to appear. This is because the compared names for the wishes are taken as what participant has signed as their name when signing up for the event in the form for that event. This is intended behaviour and should not be changed. If changed, this may backfire when this code is used on a backend together with seating planner UI. 
- Most of the code handles anonymous list, which is indexes of the participants. There are multiple reasons for that
  - Performance. It is a lot lighter to handle array of numbers instead of array of strings or data-objects.
  - It negates some user input errors. in the code before the indexes are created from the lists, the comparing between names and wishes is done after preprocessing user input.    This preprosessing is removing all spaces and Capital letters.
    - **NOTE:** After the anonymous list of participants is created, it should **NEVER** be shuffled. It should **never** be **mutated** or **shuffled** after it has been      created. This will break the code! Anonymous list means the list that has been based upon participant data-object list ( anonymous_list: `[[0, [89, 75, 50, 23], True], [1, [71, 138, 81, 85], False],...]` where one element of the list is: `[participant_id, [participant's_wishes], isMan]` ). Please take this to consideration when writing unit tests also, it is super annoying if the tests for PoolCreation fail because manually created anonymous_list is out of sync.
  - The code returns always the name that the participant has inputted in the `names` column. So if someone has a wish were reads e.g. `matti meikäläinen` and Partipant has inputted his name on the event signup correctly `Matti Meikäläinen` you will see that in the excel the used name is `Matti Meikäläinen`.

# Color and style formatting meaning:
- If font is red it  means that the participant has special wishes (e.g. "I would like to sit next to the other old students") or they have typos in their wishes. Red font color overrides all other font colors!
- If font color is not black or red, it means that that person have mutual wish with someone outside their own "mutual wish pool". That mutual wish is still inside the non-mutual seating order (inside the group separated by empty cells). If you do not see any other cell with same font color in that same group and there is a red font color cell, the pair is that red font color cell name because special wishes override mutual wish font color! 
- Default font color is black.
- The background color rotates between five different colors. This is so that there can't be a mixup of two persons belonging the same group. Consider example below:
```
0 1
2 3
4 5
```
The numbers represent final seating order, where zero is left side and 1 is on the right side of the table. Do you notice how next to partipant indexed as number `2` can only be a maximum of five different participants?

## How participants are grouped and how this affects to excel style formatting
- You may notice that between some groups there are an empty column while others do not. This is intentional. The reason is that if you have names with different background color withing two empty columns, it means that there are people who have non-mutual ( basically chained) wishes or they have mutual wish outside their own mutual wish group.
- Participants who have mutual chaining in their wishes will have the same background color. This is limitation of currently used excel output style formatting and is likely at some later point changed to be a little bit different.
#### Current behavior:
This input to `PoolCreation` class `create_mutual_wishes_groups()`-method
 ``` python
anom_list2 = [[0, [1,2,3]], [1, [0,2,3, 7]], [2, [0,1,3]], [3, [0,1,2]], [4, [5,6]], [5, [4]]
                              , [6, [5]], [7, [1]], [8, []]]
 ```
 Provides following mutual wish pools:
``` python
 [[[4, 5], [6]], [[0, 3, 2, 1, 7]], [[8]]])
 ```
 
  #### Explanation:
  If 1 and 7 has mutually wished to sit next to each other, and 7 does not share any other 1's mutual wishes , 7 and 1 should be set to sit next to each other. 
  - In the `test_seating_organizer.py` file there are more edge cases described and how they are currently handled. Most notably method `test_create_mutual_wishes_groups(self)` of the class `TestPoolCreation`.


