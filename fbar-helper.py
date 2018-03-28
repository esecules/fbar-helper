#! /usr/bin/python
import csv
import sqlite3
import sys
import time
from tabulate import tabulate

con = sqlite3.connect("transactions.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS Transactions (timestamp INTEGER, amount REAL, account TEXT);")
cur.execute("create view if not exists dailyTransactions( timestamp, amount ,account ) as select timestamp, sum( amount ), account  from transactions  group by date(timestamp, 'unixepoch','localtime'), account;")
cur.execute("create view if not exists dailyBalance(timestamp, transAmt, balance, account) as select timestamp, amount ,(select sum(amount) from dailyTransactions t2 where t2.timestamp <= t1.timestamp and t1.account == t2.account) as balance, account from dailyTransactions t1;")

if len(sys.argv) == 3:
    with open(sys.argv[1],'rb') as fin: # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.reader(fin) # comma is default delimiter
        to_db= [];
        for row in dr:
            pattern = '%m/%d/%y'
            epoch = int(time.mktime(time.strptime(row[0], pattern)))
            to_db.append((epoch, row[1], sys.argv[2]))
    
        cur.executemany("INSERT INTO Transactions (timestamp, amount, account) VALUES (?, ?, ?);", to_db)
        con.commit()
        print "inserted %d transactions" % len(to_db)
        
cur=con.cursor()

maxes = []
for row in cur.execute("SELECT date( timestamp, 'unixepoch', 'localtime' ), account , max( balance ) FROM dailyBalance group by account"):
    maxes.append( row );

print tabulate(maxes, headers=["date", "account", "balance" ], floatfmt=".2f")
con.close()
