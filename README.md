© 2021 Juuso Rytilahti.  All rights reserved.

# seating-order-organizer
A way to generate seating order automatically for sitz or some other event. The main idea of the current version is to ease the work of the one doing the seating planning for sitz and other such events


How to set this working:
1. Currently there is no `requirements.txt`. It will be added at a later date. Currently code runs fine on Spyder version 4.2.5, which was installed with Anaconda version 2.0.3.
2.  Open the file DataGenerator.py
3. In the file replace all the used absolute pathing ctrl + f e.g. `C:\Users\`. These are probably changed to dynamic add some point when I have time.
4. All excel files should pre-exist before running the code.
5. You should see multiple prints. 
```
Code is run trough namespace
Importing data from excel
Data import has been completed!
pool creation has started
Pools have been created!
Started creating all mutual wishes pools
all mutual wishes pools has been created
Data export succesfully completed!
```
If you see only some of the prints, some important code line has been commented out either at the bottom of the file under `if __name__:` clause or in the `NecessaryListsFactory` -class.
6. If you see all of the above prints and no errors raise, you are probably fine and can start coding. 

# Workflow:
1. See that the code is running properly using above steps
2. Copy participants and their wishes to the columns in the file named `input-participant-and_wishing-list.xlsx`.
3. Run all the code in the namespace
4. Check the created `output-seating-order.xlsx` file. Look for are cells where the font is **red**. This means that the participant has special wishes (e.g. "I would like to sit next to the other old students") or they have typos in their wishes. Look in the `input-participant-and_wishing-list.xlsx` and correct the wishes so that they match the names of the participants. If there is someone who has a special wish "I don't want to sit next to person xx" you can leave that wish unaltered. It will not affect functionality of the code.
5. Run code again with the altered input file.
6. Now open the output and open a **new** empty excel file next to it.
7. Now you can copy names to that new excel file which you just created either one name at a time or in groups using `ctrl + c` and `ctrl +v`.

# General Notes:
- The names that end up in `output-seating-order.xlsx` file are the ones under the `name`-column in the input excel file.
- Most of the code handles anonymous list, which is indexes of the participants. There are at least two reason for that
  - Performance. It is a lot lighter to handle array of numbers instead of array of strings or data-objects.
  - It negates some user input errors. in the code before the indexes are created from the lists, the comparing between names and wishes is done after preprocessing user input.    This preprosessing is all removing spaces and Capital letters.
  - The code returns always the name that the participant has inputted in the `names` column. So if someone has a wish were reads e.g. `matti meikäläinen` and Partipant has inputted his name on the event signup correctly `Matti Meikäläinen` you will see that in the excel the used name is `Matti Meikäläinen`.

# Color and style formatting meaning:
- If font is red it  means that the participant has special wishes (e.g. "I would like to sit next to the other old students") or they have typos in their wishes.
- You may notice that between some groups there are an empty column while others do not. This is intentional. The reason is that if you have names with different background color withing two empty columns, it means that there are people who have non-mutual ( basically chained) wishes.
- The background color rotates between five different colors. This is so that there can't be a mixup of two persons belonging the same group. Consider example below:
0 1
2 3
4 5
The numbers represent final seating order, where zero is left side and 1 is on the right side of the table. Do you notice how next to partipant indexed as number `2` can only be a maximum of five different participants?

# How to implement this to server-side.


