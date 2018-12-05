import sys
import pandas as pd
import getpass
import string
import sqlite3
import os
os.system("title "+"AmbSQL")
#USE PANDAS DB
try:
    os.system("IF NOT EXIST C:\AmbSQL MKDIR C:\AmbSQL")
except:
    pass
path = 'C:\\AmbSQL\\'
db = sqlite3.connect(path+"dtables.db")
c = db.cursor()
dbu = sqlite3.connect(path+"duser.db")
cu = dbu.cursor()
def main(cnt):
    os.system("cls")
    print("AmbSQL shell version: 1.0.2.0")
    print("")
    print("Type 'docs()' for documentation")
    print("")
    while(True):
        #Use Switch
        try:
            command = input("> ").lower()
            if(command == "connect"):
                usern = input("Enter user-name: ").lower()
                passw = getpass.getpass('Enter password: ')
                if(usern == "system" and passw == "123"):
                    cnt = 1
                    print("Connected.")
                elif(usern == "sys" and passw == "123"):
                    print("connection as SYS is not Authorised for Users!!")
                    print("")
                else:
                    print("Username or Password entered wrong!!")
                del usern
            elif(command == "createtable()"):
                if(cnt != 1):
                    print("ERROR: Not Connected !!")
                else:
                    tname = input("Enter table name: ").upper().strip()
                    c1 = input("Enter 1st Column name: ").upper().strip()
                    c2 = input("2nd Column name: ").upper().strip()
                    c3 = input("3rd Column name: ").upper().strip()
                    try:
                        c.execute("CREATE TABLE "+tname + " (id INTEGER PRIMARY KEY, "+c1+" TEXT, "+c2+" TEXT, "+c3+" TEXT)")
                        db.commit()
                        print("TABLE CREATED!!")
                    except:
                        print("ERROR!! Table Name already exists!!")
                    del tname, c1, c2, c3
            elif(command.startswith("insertvalues(") and command.endswith(")")):
                if(cnt != 1):
                    print("ERROR: Not Connected !!")
                else:
                    try:
                        abc = command[13:-1].upper().strip()
                        if(len(abc) != 0):
                            # table name missing
                            x1 = input("Enter 1st Column Value: ").lower().strip()
                            x2 = input("2nd Column Value: ").lower().strip()
                            x3 = input("3rd Column Value: ").lower().strip()
                            try:
                                c.execute("INSERT INTO "+abc +" VALUES(NULL,?,?,?)", (x1, x2, x3))
                                db.commit()
                                print("SUCCESSFULL!!")
                            except:
                                print("ERROR!! Table Not Found!")
                            del x1, x2, x3
                        else:
                            print("ERROR!! Please Enter the Table name!")
                        del abc
                    except:
                        print("ERROR!! Table Not Found!")
            elif(command.startswith("showtable(") and command.endswith(")")):
                if(cnt != 1):
                    print("ERROR: Not Connected !!")
                else:
                    try:
                        abc = command[10:-1].upper().strip()
                        if(len(abc) != 0):
                            c.execute("SELECT name FROM sqlite_master WHERE type='table';")
                            tables = c.fetchall()
                            for table_name in tables:
                                table_name = table_name[0]
                                table = pd.read_sql_query("SELECT * from %s" % table_name, db)
                                table.to_csv(path+table_name +'.csv', index_label='index')
                            pdr = pd.read_csv(path+abc+'.csv', usecols=[1, 2, 3, 4])
                            print(pdr)
                            del pdr
                        else:
                            print("ERROR!! Please Enter the Table name!")
                        del abc
                    except:
                        print("ERROR!! Table Not Found!")
            elif(command == "clear()"):
                if(cnt != 1):
                    print("ERROR: Not Connected !!")
                else:
                    main(1)
            elif(command == "docs()"):
                print("")
                print("Copyright (c) 2018, Ambuj. All rights reserved.")
                print("")
                print("\tconnect                                            - To login to database")
                print("\tcreateTable()                                      - To create new table")
                print("\tinsertValues(<table_name>)                         - To enter the values in Table")
                print("\tshowTable(<table_name>)                            - To show the Table with values")
                print("\talterTable(<old-table_name> , <new-table_name>)    - To rename Table Name")
                print("\tclear()                                            - To clear the Screen")
                print("")
                print("\tnote=> Username: 'system', password: '123'")
            elif(command.startswith("altertable(") and command.endswith(")")):
                if(cnt != 1):
                    print("ERROR: Not Connected !!")
                else:
                    abc = command[11:-1].upper()
                    try:
                        if(len(abc)!=0):
                            l1 = abc.split(",")
                            if(len(l1)==2):
                                old1 = l1[0].strip()
                                new1 = l1[1].strip()
                                c.execute("ALTER TABLE "+old1+" RENAME TO "+new1)
                                db.commit()
                                os.system("IF EXIST C:\AmbSQL\\"+old1+".csv "+"DEL /F C:\AmbSQL\\"+old1+".csv")
                                print("Table name Updated from "+old1+" to "+new1)
                                del old1, new1
                            else:
                                print("ERROR!! There should be two Parameters!")
                        else:
                            print("ERROR!! Please Enter the Table name!")
                    except:
                        print("ERROR!! Invalid Table Name!")
                    del abc
            elif(command=="logout()"):
                cnt = 0
                print("Successfully Logged Out!!")
            else:
                print("Command not found!!(please ensure you include '()' at the end)")
        except KeyboardInterrupt:
            print("KEYBOARD INTERRUPT")
            os.system("cls")
            sys.exit(0)


main(0)
