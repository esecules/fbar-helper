# fbar-helper
Python tool to help with finding the maximum account balance given a CSV file containing transactions.

# Usage
* **First** you will need to add a row for each account with the year's starting balance. Something like:
```
1/1/17,12345.67,-,"","Opening Balance"
```
* To add new transactions
```
$ ./fbar-helper /path/to/transactions.csv "Account Name"
```
* To view results only
```
$ ./fbar-helper
```
* To reset everything 
```
$ rm transactions.db
```

* You will need to ensure that there are no transactions from other years in the CSV.
* Only one account's data per CSV file.
* An account's transactions can be split across multiple CSV files.

# Disclaimer
I'm not trained in accounting in any way. Use at your own risk. 
