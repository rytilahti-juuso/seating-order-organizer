© 2021 Juuso Rytilahti.  All rights reserved.

# seating-order-organizer
A way to generate seating order automatically for sitz or some other event.


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
