# REAST-API-with-Flask

Descripition: in this project we build a REST API webserver using flask, with SQLALCHEMY and Marshmellow libraries we are
creating a sqlite database for storing and acessing the data.

## Main file - ws.py:
In this file we are coding our web server and building the database, our available requests for the webserver are:
POST, PUT, GET, PATCH and DELETE, each request have a description in the code file.

## Scondery file - cpu_memory_data:
With this file the user get extract the CPU memory data from his computer, after doing so we can put the data 
inside our database with the webserver.

## Execution and creating the database:
We can execute our webserver using the "Postman" app after running the server on command propmt (windows).
* Important: for running first time we must include the line "db.create_all()" between the lines 49 - 51 to create the database.
