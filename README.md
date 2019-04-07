# Real Estate Company Database

This project is an implementation of a database system for a large franchised real estate company in SQLAlchemy. 

1. The company has many offices located all over the country. 

2. Each office is responsible for selling houses in a particular area.

3. An estate agent can be associated with one or more offices.



Run the files from the DataBase folder as root directory:

```
python3 -m venv .venv
source .venv/bin/activate

pip3 install -r requirements.txt

python3 create.py
python3 insert_data.py
python3 query_data.py
```

### Files:
- create.py: imports all packages, establishes database connection and creates tables
- insert_data.py: inserts data into static and dynamic tables
- query_data.py: queries data according to specific questions
- requirements.txt: loads all requirements
- CS162, Assignment 3.ipynb: jupyter notebook

## Data Normalization

The database has seven tables: Agents, Buyers, Sellers, Offices, Houses, Sales, Commissions.

Sales and Commissions are populated from the entries from other tables with the help of the sell_house().

I followed the database normalization rules to make sure that there is no data redundancy and undesirable characteristics like Insertion, Update and Deletion Anamolies.

### First Normal Form

Columns have only one attribute per cell, and each column has a unique name: 'ID,' 'price,' 'email,' etc.

I restricted all values in a single column to have the same type: Text, Integer, or DateTime.

The order of the data entries doesn't matter.

### Second Normal Form

I made sure that all columns are only dependent on the primary key which is unique for every table. This property is called partial dependency where an attribute in a table depends on only a part of the primary key and not on the whole key. In my case, I didn't have any composite keys. Therefore, the second form was not violated. 

### Third Normal Form

I made sure that there is no transitive dependency. For example, I didn't include agent names to the Houses table because they would depend on the agent ID. Instead, I created a separate table called Agents where I store all the information about the agents.

### Fourth Normal Form

For a dependency A → B, if for a single value of A, multiple values of B exists, then the table may have multi-valued dependency. For example, if a table has students who take different courses and also have various hobbies that are independent of each other, such an issue can arise. In my database, I made sure to separate all tables to make sure that this is not the case.

## Indices

An index is an ordered data structure which can be used to find an entry or its primary key in O(log n) time. I didn't explicitly add indices to my tables since SQLite automatically maintains an ordered list of the data within the index's columns as well as their records' primary key values.

The joins that I used in the queries are based on foreign key constraints that are specified in the tables using the ForeignKey keyword.

SQLite is a highly optimized database (https://www.sqlite.org/optoverview.html). Therefore, I don't think that adding any other type of indices would have a significant effect on the performance.

## Transactions

A transaction is a set of tasks put into a single execution unit. It begins with a specific task and ends when all tasks are completed. If any of the tasks fail, the entire transaction fails. Therefore, a transaction has only two results: success or failure.

All transactions should satisfy the ACID properties. Atomicity guarantees that each transaction is treated as a single "unit," which either succeeds or fails. Consistency ensures that a transaction can only bring the database from one valid state to another. Isolation ensures that concurrent execution of transactions leaves the database in the same state that would have been obtained if the transactions were executed sequentially. Durability guarantees that once a transaction has been committed, it will remain committed even in the case of a system failure — source: Wikipedia.

To implement transactions, I used sessionmaker of SQLAlchemy. All the tasks are added with the help of session.add() and executed using session.commit(). I do it to add entries to all the tables to ensure that no information is getting corrupted or lost.


