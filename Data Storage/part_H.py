import time
import psycopg2.extras
import argparse
import re
import csv
import numpy as np
import pandas as pd

DBname = "census"
DBuser = "postgres"
DBpwd = "postgres"
TableName = 'Censuscopy'
Datafile = "acs2017_census_tract_data.csv"  # name of the data file to be loaded
CreateDB = False  # indicates whether the DB table should be (re)-created
Year = 2017
dir = "/home/sukanya2/generated.csv"


def initialize():
    global Year

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--datafile", required=True)
    # parser.add_argument("-c", "--createtable", action="store_true")
    parser.add_argument("-y", "--year", default=Year)
    args = parser.parse_args()

    global Datafile
    Datafile = args.datafile
    # global CreateDB
    # CreateDB = args.createtable
    Year = args.year


# read the input data file into a list of row strings
# skip the header row
def readdata(fname):
    print(f"readdata: reading from File: {fname}")
    csv = open(fname, mode="r")
    csv.readline()
    return csv


# connect to the database
def dbconnect():
    connection = psycopg2.connect(
        host="localhost",
        database=DBname,
        user=DBuser,
        password=DBpwd,
    )
    connection.autocommit = True
    return connection


# create the target table
# assumes that conn is a valid, open connection to a Postgres database
def createTable(conn):
    with conn.cursor() as cursor:
        cursor.execute(f"""
        	DROP TABLE IF EXISTS {TableName};

        	CREATE UNLOGGED TABLE {TableName} (
				Year                INTEGER,
              CensusTract         NUMERIC,
            	State               TEXT,
            	County              TEXT,
            	TotalPop            INTEGER,
            	Men                 INTEGER,
            	Women               INTEGER,
            	Hispanic            DECIMAL,
            	White               DECIMAL,
            	Black               DECIMAL,
            	Native              DECIMAL,
            	Asian               DECIMAL,
            	Pacific             DECIMAL,
            	Citizen             DECIMAL,
            	Income              DECIMAL,
            	IncomeErr           DECIMAL,
            	IncomePerCap        DECIMAL,
            	IncomePerCapErr     DECIMAL,
            	Poverty             DECIMAL,
            	ChildPoverty        DECIMAL,
            	Professional        DECIMAL,
            	Service             DECIMAL,
            	Office              DECIMAL,
            	Construction        DECIMAL,
            	Production          DECIMAL,
            	Drive               DECIMAL,
            	Carpool             DECIMAL,
            	Transit             DECIMAL,
            	Walk                DECIMAL,
            	OtherTransp         DECIMAL,
            	WorkAtHome          DECIMAL,
            	MeanCommute         DECIMAL,
            	Employed            INTEGER,
            	PrivateWork         DECIMAL,
            	PublicWork          DECIMAL,
            	SelfEmployed        DECIMAL,
            	FamilyWork          DECIMAL,
            	Unemployment        DECIMAL
         	);	
         	ALTER TABLE {TableName} ADD PRIMARY KEY (Year, CensusTract); 
    	""")

        print(f"Created {TableName}")


def load(conn, csvfile):
    with conn.cursor() as cursor:
        start = time.perf_counter()
        cursor.copy_from(csvfile, TableName, sep=",")
        elapsed = time.perf_counter() - start
        print(f'Finished Loading. Elapsed Time: {elapsed:0.4} seconds')


def main():
    initialize()
    conn = dbconnect()
    df = pd.read_csv(Datafile)
    csvread = open(dir, 'r')
    if CreateDB:
        createTable(conn)
    load(conn, csvread)


if __name__ == "__main__":
    main()