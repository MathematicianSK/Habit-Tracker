## Habit tracker
This is a simple habit tracker application built with Python. With it you can check-off currently saved habits, create new habits, remove existing habits and further analyze your progress in the form of different lists with statistics. 
The data is saved in a JSON file, you can enter the program via a command line interface. 


## Requirements
In order to run this program you need Python 3.7 or higher. 
To be able to also run the test program you also have to install pytest. 


## Installation and setup
To use this tracker, take the following steps: 
- Download all the necessary files, namely `class_habit_py`, `class_habitsstorage.py`, `streak.py`, `statistics.py` and `main_program_habit_tracker.py` and put them into one folder. 
- You also have to download the test file `test_habit_tracker.py` too if you want to run it. It does not have to be in the same folder as the other files. 
- Open a terminal and navigate to the folder where you put in the files of this program. 


## Running the program and test
To start and run the habit tracker put the following command in your terminal: 

`python main_program_habit_tracker` 

After that, the command line interface of the main menu appears and you can use the application. 

In order to run the test file, you first have to install a virtual environment by typing in the command 

`python -m venv v_env` 

in your terminal. Afterwards, you can activate the test environment (in Windows) by using 

`v_env\Scripts\activate.bat`

Now you have to install pytest with the command 

`pip install pytest==7.4.4` 

You now can test the habit tracker by typing in 

`pytest` 


## How to use the habit tracker
With this program you can check-off currently saved habits, create new habits, remove existing habits and further analyze your progress. 

To check-off a habit, you you choose number 1 in the main menu. You then receive a list of all your habits which you have not checked-off in the current time interval so far with their corresponding habit-IDs. 
By typing in a habit-ID, you check-off the respective habit. 

To create a new habit, you type in 2 from the main menu. You will then first be asked what the periodicity of your habit is. 
You can pick either a daily period by typing in 1 or a weekly period by typing in 2. After that, you have the opportunity to give your new habit its name. 

To remove a habit from your app, you take the integer 3 of the main menu. You then get a list of all your habits saved in the application with their habit-IDs. 
When you then type in one of those habit-IDs, the corresponding habit is deleted from the list. 

If you want to see your improvements with your habits, you type in the number 4 of the main menu for the statistics section. You are then presented seven different lists you can choose from to further analyze your progress. 