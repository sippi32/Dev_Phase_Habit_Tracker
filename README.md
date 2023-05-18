# Habit_Tracker_1.0 Application by Marc Fischer


Welcome to my very first application. A Habit Tracker. Creating this habit tracker was very, very challenging to me but I think that I have learned a lot during
the process.  

Created with Visual Studio Code, Python 3.11.1, MySQL Workbench (8.0 CE) and as GUI Tkinter.

The aim is to create a habit tracker that allows different users to track their habits at different time intervals. New users can register and existing users can log in with their username and password. The following sample users with passwords can be used for testing purposes:

Each of these existing sample accounts has already created and tracked their own Habits and existing Streaks. Please read the user guide below carefully to best understand the functionalities of the Habit Tracker. In addition to the Habits and categories created individually by the users, the Habit Tracker also comes with a number of predefined Habits and categories that users can choose from. 

The users also have the possibility to analyse their habits in relation to existing streaks, records and the degree of achievement of self-set goals.
In addition, there are various high scores where users can compare themselves with each other and thus motivate each other to continue actively tracking their habits. There is also a point system where users can earn points for existing streaks and thus move up in the high score.

It is important to say that the Habit Tracker requires a MySQL connection. At the first start, the user is asked for this connection (host/username/password) and must also enter a name for the database/schema. This name can be freely chosen. For example habit_tracekr_db. After the connection has been successfully established, the database and its required tables are created. The SQL statements are located in database_tables.txt. Furthermore, the database is filled with predefined habits, categories and already existing example users (inserts.txt). These sample users already have existing track records and can be used for testing purposes. The next time the Habits Tracker is used, the existing database connection and database can then simply be entered and subsequently used.

The following picture contains the **Logins** with usernames and passwords for the example users after the Database was successfully initialised. 

![grafik](https://user-images.githubusercontent.com/131082327/235941616-b0fa93da-2a60-4e96-aebc-20e708c11474.png)

## Installation 

`pip install -r requirements.txt`

contains required packages just like:

datetime, mysql-connector-python, tk, tkcalendar, pandas, matplotlib

## 1. Usage

Change the current working directory to the directory where your habit tracker files are located. For changing the directory use:

`cd path`


Start the application:

`python main.py `

**Simple Start:**

It's also possible to start the application by using the **start.bat** file which first changes the working directory to the folder where the Habit Tracker is located in, the executes the installation of the requirements.txt and then starts the application calling python main.py


The Habit Tracker allows multiple users to use the tracker. The Habit Tracker runs locally and needs a MySQL database to store the progress. At the first login or initialisation, the user is asked for the database connection. Please have information about host, username and password of the MySQL connection ready. Any name can be entered in the database field. If the database does not already exist, a new database will be created automatically and filled with sample data. The tables can be found in the file database_tables.text and the corresponding insert statements with the sample data can be found in inserts.txt. But as already mentioned, the database is created automatically. The next time you log in, simply enter the name of the existing database in the database field. In this case, the existing database will be used for further progress.

 
## 2. Database Connection and User Login/Registration


## 2.1.	Database Connection Screen

-	The first screen when starting the habit tracker is the Database Connection screen (class database_connection_screen, main.py)
-	User has to enter the MySQL Database credentials host/user/password/port and set a name for a new database. If it’s the first login and the database wasn’t created before the database gets created (class MySQLDatabase, def create_database, def_initialize_database, database.py and inserts from inserts.txt)
-	When the database is created, the database information is also stored as an environmental variable for later use during the active session.
-	The initialisation of the database takes approx. 20 seconds, as waiting times between the individual queries have been built in for safety's sake in order not to overload the database.


![image](https://github.com/sippi32/Fin_Phase_Habit_Tracker/assets/131082327/942c3127-2a0f-4440-9eaa-39f358f650ea)
![image](https://github.com/sippi32/Fin_Phase_Habit_Tracker/assets/131082327/07601239-d0c4-47a3-970e-2c1863a9d05b)

  
-	If a user enters incorrect database credentials, an error message is displayed

![grafik](https://user-images.githubusercontent.com/131082327/235931638-975820d9-7296-4028-98b6-5f83a227a894.png)

 
## 2.2.	Created Database tables

-	The following tables are created when initialising the database

user_table:

![grafik](https://user-images.githubusercontent.com/131082327/235931994-c67dbc2d-e648-447c-b270-d93ae6a34c3e.png)

 habits and category tables:

![grafik](https://user-images.githubusercontent.com/131082327/235932033-dc79cc8d-eff1-4a1e-aa0a-85079efdaa4f.png)
![grafik](https://user-images.githubusercontent.com/131082327/235932069-ce7a37fa-f004-4d0c-80b0-9449c9a62547.png)


monitoring_interval table: 

![grafik](https://user-images.githubusercontent.com/131082327/235932112-4ebbff3a-f1e7-4ef0-9524-5eb8e3f6c047.png)

 
active_user_habits tables: 
- (SQL insert statements in insert.txt are dynamical without fixed dates so it is always up to date when a new user initialises the demo database for the first time

![grafik](https://user-images.githubusercontent.com/131082327/235932168-52e573de-ed61-4e29-932d-15a61fe4bf34.png)

 


## 2.3.	Login/Registration Screen

-	After the successful initialisation of the database, the login/registration screen opens.
-	Class login_screen, main.py
-	A new user can register to the habit tracker or its possible to use one existing user (see user_table username, password). 
-	For example user: Silke_29 password: Silke or user: heinzi_09 password: hubinho

![grafik](https://user-images.githubusercontent.com/131082327/235932488-8bd32873-4657-44ab-afa2-bbd022fe05d5.png)
![grafik](https://user-images.githubusercontent.com/131082327/235932508-6af8df05-f7b5-4a7e-b005-e77b8a5d6f54.png)
![grafik](https://user-images.githubusercontent.com/131082327/235932540-3d71e4a3-6c10-4ad2-9870-23ea569f5f90.png)
![grafik](https://user-images.githubusercontent.com/131082327/235932553-1e736470-29ae-49ab-bd54-7cf668cd68bf.png)






 
## 3.	The Habit Tracker main screen
-	The next screen is the main screen of the habit tracker. It gives the logged in user an overview of the current active habits.
-	The user can mark and check off active habits. After the successful check, the streak increases and the remaining time and deadline are extended. Double ticking is prevented and the user is informed with an error pop-up.
-	If a user does not manage to check off an active habit within the time period, the user must reactivate the active habit. However, this causes the active streak to expire. Nevertheless, it remains in the database for a complete history, as a new entry is saved and the status of the old entry is changed.

![grafik](https://user-images.githubusercontent.com/131082327/235932800-700e6ffb-5803-4f01-83b9-88f0037d39a8.png)


## 4.	MyHabits

-	When the MyHabits button is pressed, a pop-up window opens in which the user can see the saved habits. Some of the habitats are predefined system habitats that cannot be deleted by the user. Users can freely add and delete own habits in this screen, which are only visible to them. To do this, the button "Add Habit" must be pressed. Another pop-up opens in which the user can enter the name and description and must select one of the categories. Entries with the same Habit Name multiple times are not allowed.

![grafik](https://user-images.githubusercontent.com/131082327/235932852-f67149fa-8969-4215-9352-8e02466c0b30.png)

 
-	In this example a new habit with the Habit Name “Music” is added

![grafik](https://user-images.githubusercontent.com/131082327/235932883-db36ece2-642a-494e-b843-9e5507614c82.png)

 
-	After saving the the Habit and “Update Table” the new habit is added to the table.

![grafik](https://user-images.githubusercontent.com/131082327/235932916-da797920-1472-4e02-b470-4993c51fdfd0.png)

 
-	Now the user can activate this habit for active habit tracking by selecting the habit and clicking the button “Activate Habit”. The following window opens. User can choose the monitoring interval and additional options like a streak goal/target and a fixed end date. 

![grafik](https://user-images.githubusercontent.com/131082327/235932954-46b35100-c2b4-48b4-8d44-9ee7a7a76273.png)

 
-	After activating the habit the habit it is contained in the Active Habits table in the main screen.

![grafik](https://user-images.githubusercontent.com/131082327/235933005-44c012d5-a0c8-46ff-ba63-07adc40aef39.png)

 
-	Now a user can check off the habit once every monitoring interval

![grafik](https://user-images.githubusercontent.com/131082327/235933031-79d068fb-106d-4f8a-b0e1-2f2c2d558a59.png)
![grafik](https://user-images.githubusercontent.com/131082327/235933053-b863299e-6b8f-4b1d-98c2-c02d7641809f.png)


 

## 5.	MyCategories

-	The MyCategories screen is similar to the MyHabits screen. Users can add new categories and delete existing ones (if not SYS category).

![grafik](https://user-images.githubusercontent.com/131082327/235933095-b58be361-4c21-45bb-aa9c-67071a1ac91a.png)



## 6.	Analyze MyHabits Screen:

-	The Analyze MyHabits Screen contains some predefined private analyses for the personal behaviour. 
-	Users can choose between the following analyses:
	Longest active streaks 
•	Shows all streaks of the user (active and historical) ordered in decreasing order
	Same habit started
•	Gives the user information about how often the same habit was already started. For example, it shows how many times a user has tried to quit smoking. 
	Completion of Streak Targets
•	If a user entered a streak goal/target when activating a habit this two analyses show the user how the progress in % or how many check offs (days/weeks/months) are left


 ![grafik](https://user-images.githubusercontent.com/131082327/235933243-3f94d097-0219-4896-9f05-78a3ebb96c1b.png)
 
 ![grafik](https://user-images.githubusercontent.com/131082327/235933329-cc3b795a-43b1-48d3-b32a-8d8e44d37a9e.png)
 
 ![grafik](https://user-images.githubusercontent.com/131082327/235933353-829b8608-f166-4308-a05d-1f3173fa2865.png)
 
 ![grafik](https://user-images.githubusercontent.com/131082327/235933377-0d46d2e4-7e1e-4050-aa33-f564729b5624.png)


## 7.	Update Profile

-	The Update Profile Button gives a user the opportunity to change personal information just like name, username, password. Single or multiple entries are possible.

![grafik](https://user-images.githubusercontent.com/131082327/235933420-aa5b03ba-f722-41ac-84b4-74799389b890.png)

 
## 8.	Highscores

-	The last screen is the global high score screen where a user can compare the progress to other registered users. 
-	There are two options available:
	Longest global streaks
•	Shows all streaks (active and historical in decreasing order
	Most points earned
•	This function adds kind of gamification to the habit tracker. User can earn points by active streaks. (1 point for each daily streak, 2 points for each weekly streak, 3 points for each monthly streak)

![grafik](https://user-images.githubusercontent.com/131082327/235933463-f3bf6465-3f9b-4d67-97a6-2110db668ee7.png)

![grafik](https://user-images.githubusercontent.com/131082327/235933492-69fd9452-eab2-4f11-afcb-32fa13bc1488.png)


 
-	The following bar chart shows the high score regarding the earned points.

![grafik](https://user-images.githubusercontent.com/131082327/235933608-da407e77-546e-4081-a106-2c0e86fc3f5c.png)

 



## 9. UML Class Diagram

The following picture shows a UML class diagram of the Habit_Tracker_1.0

![grafik](https://user-images.githubusercontent.com/131082327/235934424-56194b96-43ce-4a7c-ae30-7dfcd97f9f5c.png)



 

