#!/usr/bin/python 
import sqlite3

def createTable(db,tablename):
	db.execute('CREATE TABLE if not exists ' + tablename + '(id integer, title text, authors text, \
                    year text, pub_venue text, ref_id text, ref_num integer, abstract text)')
	print str(tablename) + " created."

def populateTable(db, ):
    f = open('publications.txt')
    INDEX = "";
    TITLE = "";
    AUTHORS = "";
    YEAR = "";
    PUB_VENUE = "";
    REF_ID = "";
    REF_NUM = 0;
    ABSTRACT = "";
    i = 0;
    print "Adding Papers;"
    for rline in f:
        line = rline.decode("utf-8").rstrip();
        if line.startswith('#index'):
            INDEX += line.lstrip('#index');
        if line.startswith('#*'):
            TITLE += line.lstrip('#*');
        if line.startswith('#@'):
            AUTHORS += line.lstrip('#@');
        if line.startswith('#t'):
            YEAR += line.lstrip('#t');
        if line.startswith('#c'):
            PUB_VENUE += line.lstrip('#c');
        if line.startswith('#%'):
            REF_ID += line.lstrip('#%') + ";";
            REF_NUM = REF_NUM+1;
        if line.startswith('#!'):
            ABSTRACT += line.lstrip('#!');
        if line=="":
            REF_ID = REF_ID[:-1] #remove trailing ;
      #      print INDEX + ", " + TITLE;
            db.execute('insert into papers values (?,?,?,?,?,?,?,?)' \
            , (INDEX, TITLE, AUTHORS, YEAR, PUB_VENUE, REF_ID, REF_NUM, ABSTRACT));
            INDEX = "";
            TITLE = "";
            AUTHORS = "";
            YEAR = "";
            PUB_VENUE = "";
            REF_ID = "";
            REF_NUM = 0;
            ABSTRACT = "";
        i += 1
        if i%10000==0:
            print ".",
    f.close()    

def main():
	conn =sqlite3.connect('Paper_db')
	db=conn.cursor()
	raw_input("Creating Tables, Press Enter to Continue")
	createTable(db,'papers')
	print "Tables Created!"
	raw_input("Start Populating, Press Enter to Continue")
	populateTable(db)
	print "Populated!!"
	conn.commit()
	print "Commiteed!!!"
	db.close()

if __name__ == '__main__':
	main()