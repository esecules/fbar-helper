#! /usr/bin/python
import csv
import sqlite3
import sys
import time
from tabulate import tabulate
import yaml

con = sqlite3.connect("transactions.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS Transactions (timestamp INTEGER, amount REAL, account TEXT, PRIMARY KEY(timestamp, account));")
cur.execute("CREATE VIEW IF NOT EXISTS dailyBalance(timestamp, transAmt, balance, account) AS SELECT timestamp, amount ,(SELECT SUM(amount) FROM Transactions t2 WHERE t1.account == t2.account AND t2.timestamp <= t1.timestamp) AS balance, account FROM Transactions t1;")

if len(sys.argv) == 3:
    with open( 'config.yaml', 'r' ) as f:
        config = yaml.load(f)
    for bankName in config:
        bank=config[bankName]
        print bankName
        with open(sys.argv[1],'rb') as fin: # `with` statement available in 2.5+
            # csv.DictReader uses first line in file for column headings by default
            dr = csv.reader(fin) # comma is default delimiter
            to_db= [];
            rows = [ r for r in dr ]
            startRow = 1 if bank["ignoreFirstRow"] else 0
            endRow = -1 if bank["ignoreLastRow"] else len(rows)
            if not bank["datesAscending"]:
                rows = [r for r in reversed( rows )]
            try:
                for row in rows[startRow:endRow]:
                    epoch = int(time.mktime(time.strptime(row[bank['dateColumn']], bank['dateFormat'])))
                    while epoch in [e[0] for e in to_db]:
                        epoch+=1
                    to_db.append((epoch, row[bank['moneyColumn']], sys.argv[2]))
            except:
                continue
            cur.executemany("INSERT INTO Transactions (timestamp, amount, account) VALUES (?, ?, ?);", to_db)
            con.commit()
            print "inserted %d transactions" % len(to_db)
        break
    
cur=con.cursor()

maxes = []
for row in cur.execute("SELECT DATE( timestamp, 'unixepoch', 'localtime' ), account , MAX( balance ) FROM dailyBalance GROUP BY account"):
    maxes.append( row );

print tabulate(maxes, headers=["date", "account", "balance" ], floatfmt=".2f")
con.close()
