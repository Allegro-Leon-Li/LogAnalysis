# LogAnalysis
This is a Udacity Log Analysis project code. This is a reporting tool that prints out reports (in plain text) based on the data in the database. This reporting tool is a Python program using the psycopg2 module to connect to the database.

## Requirements
  * Python 2.7
  * psycopg2 module for Python
  * PostgreSQL

## How to run
Before running the program, the database must be created by the following steps:
  1. Download the *newsdata.sql* file from Udacity website and put it in the same directory of *report.py*
  2. With PostgreSQL installed, run the psql command: `psql -d news -f newsdata.sql` which created a database called *news*
To run the program, type `python report.py`
