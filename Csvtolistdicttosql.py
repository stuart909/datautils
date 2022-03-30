import sqlite3
import csv
'''
Written by: Stuart Anderson
Copyright: Tobu Pengin, LLC, 2021
'''

class Database():
    def __init__(self, db=':memory:'):
        #create global database connection and db cursor
        self.db = db
        self.conn = sqlite3.connect(self.db)
        self.c = self.conn.cursor()
        #if self.db != ':memory:':
            #self.load()
    def close(self):
        #close db connection
        self.conn.close()

    def save(self):
        #save db information
        self.conn.commit()
        self.dump()

    def find(self, x):
        #manual sql search, takes a sql statement string
        search = self.c.execute(x)
        return search.fetchall()

    def manual(self, q):
        try:
            self.c.execute(q)
        except e:
            print(e.args[0])

    def dump(self):
        if self.db != ':memory:':
            file_db = sqlite3.connect(self.db)
            query = "".join(line for line in self.conn.iterdump())
            file_db.executescript(query)
            file_db.close()
    '''
    TODO either fix or nix load
        def load(self):
            if self.db != ':memory:':
                mem_db = sqlite3.connect(':memory:')
                query = "".join(line for line in self.conn.iterdump())
                mem_db.executescript(query)
                self.close()
                self.conn = mem_db
    '''        

    def search(self, SELECT, FROM, WHERE=None, VAL=None, OP='='):
        #a standard search filtering the contents with a where statement
        if WHERE != None and VAL != None:
            #If we supply WHERE and VAL to filter table selections
            if type(VAL) is tuple:
                #if I supplied the proper tuple for VAL, just search for it
                search = self.c.execute("SELECT " + SELECT + " FROM " + FROM + " WHERE " + WHERE + OP + "?", VAL)
                return search.fetchall()
            else:
                #if I supplied a string for VAL, then make it a tuple
                    if VAL[0] == '(' and VAL[len(VAL)-1] == ')':
                        #if VAL is a string that looks like a tuple, format it to tuple
                        search = self.c.execute("SELECT " + SELECT + " FROM " + FROM + " WHERE " + WHERE + "=?", (VAL.strip("('),"),))
                        return search.fetchall()
                    else:
                        #else it is just a string so plop VAL into a tuple
                        search = self.c.execute("SELECT " + SELECT + " FROM " + FROM + " WHERE " + WHERE + "=?", (VAL,))
                        return search.fetchall()
        else:
            #If we only want to select from a table
            search = self.c.execute("SELECT " + SELECT + " FROM " + FROM)
            return search.fetchall()

    def insert(self, table, vals):
        #inserts a row into a table.  Rows are usually a tuple, the entire row to be inserted, or a list of tuples, a list of row data to be inserted.
        #db.insert('poop_table', [(1,'Bob','Chicago'),(2,'Amber','Nashville'),(3,'Bill','New York')])
        #the above example inserts 3 rows containing an ID number, name, and city name.  This would require the table to already be setup with the appropriate columns
        if type(vals) is list:
            #vals is list containing tuples
            self.c.executemany("INSERT INTO " + table + " VALUES " + "(" + ("?," * (len(vals[0]) - 1 ) ) + "?)", vals)
        elif type(vals) is str:
            #vals is a string
            if vals[0] != '(' and vals[len(vals)-1] != ')':
                #if a regular string is supplied without tuple markings correct it and insert new string
                newstr = "(" + vals + ",)"
                self.c.execute("INSERT INTO " + table + " VALUES " + newstr)
            else:
                #else the string looks like a tuple and simply insert it
                self.c.execute("INSERT INTO " + table + " VALUES " + vals)
        else:
            #vals is tuple, convert to string and insert
            self.c.execute("INSERT INTO " + table + " VALUES " + str(vals))
        self.save()

    def make(self, table, columns, data_type):
        #make creates the table in the database.  it takes a list of column names (string), and a list of SQLite datatypes that represent the column datatypes.
        #db.make('poop_table',['ID','Name','City'],['INTEGER','TEXT','TEXT'])
        #the above example will create the poop_table with ID, Name, and City columns, with datatype, int, string, and string, respectively
        table_check = self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='%s'" % table)
        table_check = table_check.fetchone()
        if type(columns) is list:
            for i in columns:
                try:
                    if table in table_check:
                          self.c.execute("ALTER TABLE '%s' ADD COLUMN %s %s" % (table, i, data_type[columns.index(i)]))
                except:
                    self.c.execute("CREATE TABLE '%s' ('%s' '%s')" % (table, i, data_type[columns.index(i)]))
                    table_check = [table,]
        else:
            try:
                if table in table_check:
                    self.c.execute("ALTER TABLE '%s' ADD COLUMN %s %s" % (table, columns, data_type))
            except:
                    self.c.execute("CREATE TABLE '%s' ('%s' '%s')" % (table, columns, data_type))
                    table_check = [table,]

        self.save()

    def update(self, table, _set, where):
        #requires table name, and either a list or tuple of the set info (column value pair), and the where filter list or tuple, column filter pair
        #db.update('poop_table', ['StudentName','Tommy'], ['StudentID','33'])
        #the above example will update the poop_table row containing studentID 33 and update the StudentName to tommy.
        self.c.execute('UPDATE %s SET %s = %s WHERE %s = %s;' % (table, _set[0], _set[1], where[0], where[1]))


data = []
keys = []

with open('/home/stuart/Documents/peeps.csv', newline='') as csvfile:
    d = csv.reader(csvfile, delimiter=',')
    for n,row in enumerate(d):
        if n == 0:
            keys = [k for k in row]
        else:
            tmp = {}
            for v in row:
                tmp.update({keys[row.index(v)]:v})
            data.append(tmp)
#adding the ID key to my csv key header data, manually
keys.insert(0,'ID')
#create database in memory
db = Database(':memory:')
#make table based on csv example, but adding ID manually
db.make('test',keys,['INTEGER','TEXT','TEXT','INTEGER','TEXT'])
#iterate through my csv data
#using enumerate to give an ID number n, the dict data will be d
for n,d in enumerate(data):
    #creating a temporary ID number in a list named put
    put = [10001+n]
    for k,v in d.items():
        #looping through my d dict.items, and unpacking into key,value (k,v)
        put.append(v)
        #adding the current value, in order, into put, so it no has ID and items in order
    #inserting individual rows into table test, that we just created
    db.insert('test',tuple(put))
    
db.save()



