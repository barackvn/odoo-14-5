# Odoo Data Migration (Odoo V14)

Using this module, you can migrate your data from your old system to Odoo database without RESTAPI using database 
direct connection.

This module will performs the migration process in a professional way using model objects, 
in addition to that you can also use both systems (your current system and Odoo) together by 
syncing Odoo with your old system,
this is can done by defining schedule migration jobs to copy customers\vendors\products\inoices\.. data 
to odoo based on Odoo schedule Actions.
        
## Prerequisites

### Install package "pyodbc"

You have to install this package to allow your server to conect to your system database.

please follow the following link to install the required package based on your odoo hosting environment (Windows \ Linux)

https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-1-configure-development-environment-for-pyodbc-python-development?view=sql-server-ver15

    
## Connection String

**First**: You need to install the proper driver depend on database type.

**Second**: You need to use the proper connection string.

**For more details**: access the following link.

https://github.com/mkleehammer/pyodbc/wiki


### Connection to MSSQL

You have to install MSSQL ODBC driver that suitable for your Odoo server.

Connection string = "'DRIVER={ODBC Driver 17 for SQL Server};SERVER=test;DATABASE=test;UID=user;PWD=password'"


### Connection to Postgres

You have to install psqlodbc first as Postgres ODBC driver.

Connection string = "Driver={PostgreSQL};Server=IP address;Port=5432;Database=myDataBase;Uid=myUsername;Pwd=myPassword;"


### Other connections types 

You may visit the following URL 

https://www.connectionstrings.com/
