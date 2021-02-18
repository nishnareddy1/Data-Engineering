import time
import psycopg2.extras
import argparse
import re
import csv

DBname = "postgres"
DBuser = "postgres"
DBpwd = "postgres"
TableName = 'CensusDataUnlogged'
Datafile = "Oregon2015.csv"  # name of the data file to be loaded
CreateDB = False  # indicates whether the DB table should be (re)-created
Year = 2015


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
    with open(fname, mode="r") as fil:
        dr = csv.DictReader(fil)
        headerRow = next(dr)
        # print(f"Header: {headerRow}")

        rowlist = []
        for row in dr:
            rowlist.append(row)

    return rowlist


# convert list of data rows into list of SQL 'INSERT INTO ...' commands
def getSQLcmnds(rowlist):
    valstrlist = []
    for row in rowlist:
        # handle the null vals
        for key in row:
            if not row[key]:
                row[key] = 0
            row['County'] = row['County'].replace('\'', '')
        valstrlist.append((Year, row['CensusTract'], str(row['State']), str(row['County']), row['TotalPop'],
                           row['Men'], row['Women'], row['Hispanic'], row['White'], row['Black'], row['Native'],
                           row['Asian'], row['Pacific'], row['Citizen'], row['Income'], row['IncomeErr'],
                           row['IncomePerCap'],
                           row['IncomePerCapErr'], row['Poverty'], row['ChildPoverty'], row['Professional'],
                           row['Service'], row['Office'],
                           row['Construction'], row['Production'], row['Drive'], row['Carpool'], row['Transit'],
                           row['Walk'], row['OtherTransp'],
                           row['WorkAtHome'], row['MeanCommute'], row['Employed'], row['PrivateWork'],
                           row['PublicWork'],
                           row['SelfEmployed'], row['FamilyWork'], row['Unemployment']))
    return valstrlist


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


def load(conn, ivallist):
    with conn.cursor() as cursor:
        print(f"Loading {len(ivallist)} rows")
        start = time.perf_counter()
        cmd = f"INSERT INTO {TableName} VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        psycopg2.extras.execute_batch(cursor, cmd, ivallist)
        elapsed = time.perf_counter() - start
        print(f'Finished Loading. Elapsed Time: {elapsed:0.4} seconds')


def main():
    initialize()
    conn = dbconnect()
    rlis = readdata(Datafile)
    cmdlist = getSQLcmnds(rlis)

    if CreateDB:
        createTable(conn)

    load(conn, cmdlist)


if __name__ == "__main__":
    main()