# code from  https://medium.com/@mahmudahsan/how-to-use-python-sqlite3-using-sqlalchemy-158f9c54eb32

# Program entry point
from App import mydatabase

def main():
    dbms = mydatabase.MyDatabase(mydatabase.SQLITE, dbname='mydb.sqlite')
    # Create Tables
    dbms.create_db_tables()

    # dbms.print_all_data(mydatabase.HOTELS)
    # dbms.print_all_data(mydatabase.REVIEWS)
    # dbms.sample_query()
    # dbms.sample_query()  # simple query
    # dbms.sample_delete()  # delete data
    # dbms.sample_insert()  # insert data
    # dbms.sample_update()  # update data


# run the program
if __name__ == "__main__": main()


# import sqlite3
#
# try:
#     sqliteConnection = sqlite3.connect('test1.db')
#     cursor = sqliteConnection.cursor()
#     print("Successfully Connected to SQLite")
#
#     sqlite_insert_query = """INSERT INTO hotels
#                           (hotelID,	name,	num_reviews,	price,	score)
#                            VALUES
#                           (1,'James',2,90,4.5)"""
#
#     count = cursor.execute(sqlite_insert_query)
#     sqliteConnection.commit()
#     print("Record inserted successfully into hotels table ", cursor.rowcount)
#     cursor.close()
#
# except sqlite3.Error as error:
#     print("Failed to insert data into sqlite table", error)
# finally:
#     if (sqliteConnection):
#         sqliteConnection.close()
#         print("The SQLite connection is closed")
#
# import sqlite3
#
# def readSqliteTable():
#     try:
#         sqliteConnection = sqlite3.connect('test1.db')
#         cursor = sqliteConnection.cursor()
#         print("Connected to SQLite")
#
#         sqlite_select_query = """SELECT * from hotels"""
#         cursor.execute(sqlite_select_query)
#         records = cursor.fetchall()
#         print("Total rows are:  ", len(records))
#         print("Printing each row")
#         for row in records:
#             print("Id: ", row[0])
#             print("Name: ", row[1])
#             print("\n")
#
#         cursor.close()
#
#     except sqlite3.Error as error:
#         print("Failed to read data from sqlite table", error)
#     finally:
#         if (sqliteConnection):
#             sqliteConnection.close()
#             print("The SQLite connection is closed")
#
# readSqliteTable()