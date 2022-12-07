# Rental management system

#### Video Demo: https://youtu.be/73FMt5GjYc4
### Description:

Rental Managment system is a web application where a small car rental business can manage their fleet of vehicles, make contracts with its customers, entering all the necessary information such us the vehicle's rental and return day, the charge per day, total charge etc as well the necessary customer personal information such as name phone number address car licence number etc. The application provides a viszualization off all  the necessary information for the busines using a callendar type table which shows anytime the current situation of the fleep which vehicle is rented and for how much time, who has rent the vehicle and information about the charge.

## How to use it

#### REGISTER AND LOG IN

For now application can be used by anyone by simply registering with a username and a password. 

#### ADD VEHICLE

After registretion the user (busines) can enter its fleet  of vehicles by presing the add vehicle option located in the menu on the left of the screen. In this location the user can enter through a form the details of each vehicle, such as the brand, model, licence plate, displacement and the category of the vehicle (motorcycle, car etc).

#### NEW CONTRACT

After importing the vehicles the user can start making contracts with his customers by going to the menu option new contract. There he can enter all the necessary personal details of the customer (name, address. etc), choose though the form the day and time of the rental and return of the vehicle and base on this selection the avaliable vehicles will appear on the form i.e. the vehicles that are not rented for the rental period he has entered. Please note that the form will not be submitted if any required contract information is not received and upon submision it will show which information is missing. 

#### CALENDAR

 Calendar is the base page of the app, is the page that the user sees after logging in. There  is a board in calendar format where in the  first columm are all the vehicles  entered by the user and in the first row a callendar starting for the current date an for a period of one week. A little over there are two buttons through which the user can navigate the calendar in front and back one day each time he pressses a button. The callendar board is updated whenever the user makes a new contract or adds a new vehicle. Through the calendar the user has a global image for the situation of every vehicle, if is rented or not, to whom it is rented and when it returns as well as information about the charge to each customer.

#### SHOW/DELETE CONTRACT

By choosing this option from the menu user can sees all the contracts has made in a table beginnig from the last contract that has submited. User can also delete a contract from this location. Note that if a contact is deleted and the customer information is also deleted.

#### SHOW CUSTOMERS 

In this location user can sees all the information about his customers begining from the last customer who has rented a vehicle.


## How it works

Rental manager is an apllication created with **Python flask framework, Javascript HTML and CSS**. My project folder has the following structure:
- static
  - styles.css
  - index.js
  - new_contract.js
- templates
  - base.html
  - index.html
  - login.html
  - new_contract.html
  - new_vehicle.html
  - register.html
  - show_and_delete_contract.html
  - show_customers.html
- app.py
- mcalendar.py
- database.py
- project_db.sqlite

Let's explain what some of these files do starting from the end.

### project_db.sqlite and database.py
project_db.sqlite is the database of the application which is a sqlite3 database containing 4 tables.

- Table users with three columms (id, username, password): In this table stored the users's information. Note that the password columm does not store the actual password but a hash using werkzeug.security library and check_password_hash, generate_password_hash.

- Table vehicles with seven columms (id, ak, type , brand, model, displacement userid): In this table 
stored the vehicles of each user using a foreign key "userid" to know  which user each vehicle belong to.

- Table customers with  ten columms (id, firstname, lastname, address1, address2, phonenum1, phonenum2, licence, id_passport, userid). Nothing spacial here just the necessary customers information and also a foreign key to users table (userid)

- Table contracts with ten columms (id, customer, vehicle, rentday, returnday, chargepd, payinad, totalcharge, reminder, userid). In this table customer is a foreign key to customers table, vehicle is a foreign key to vehicles table and user id is also a foreign key to users table)

database.py is only used to create the database.

### mcalendar.py

The mcalendar contains an auxiliary function that accepts five arguments. Two dates the starting date and the end date and three python dicts that are essentially the data of the corresponding tables of the database. The funcion is called from the index function within the flask application either by the "POST" method or with the "GET" method and returns a table which will then get its final form though javascript from the calendar function in index.js.


### app.py

app.py is the flask application that if you are familiar with the flask framework it is not difficult to understand how it works.

### templates

In the taplates folder is the base.html file  and the rest html files that extend base.html. According to the way a flask application is structured

### static

In static folter there is a css file that i used to style the application and two js files. index.js and newcontract.j which i will explain below.

### index.js

In index.js is the code i used so that the user can navigate the calendar by sendind every time a button is pressed requests to server with different dates refreshing only the calendar without having to refresh the whole page. There is also the calendar function which formats the data received from the server into a user-friendly format.

### newcontract.js

Here is the code to update the list of available vehicles every a rental period is selected using asynchronous javascript. There are still some functions for calculating rental charge.

