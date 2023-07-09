# shop-manage-cli-python
Simple CLI shop management application using Python and PostgreSQL
you can add,remove and edit products in your database,create reciepts and delete them,display current stock in your shop and print reciepts using their ID.
## Installation
you need to install the dependencies (python modules) mentioned in the requirments.txt file.
then you need to create a database using postgres using the following command:
create database your-database-name;
then you need to create a schema for your database using the following command:
create schema schema-name;
then you need to execute the sql commands provided in the script.sql file to create the relation for the applications and the functions and triggers needed for the application to function properly.
lastly, you need to modify the config.ini file to make it possible for the application to connect to the database, you need to edit the database name and the schema name  in the postgresql section to the ones you created in the last step, then you need to set the password as your postgres super user password, because I didn't implement the application using roles because I'm lazy, and set the password of the system in the main section to the password you like.
