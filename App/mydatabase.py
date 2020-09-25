# code from  https://medium.com/@mahmudahsan/how-to-use-python-sqlite3-using-sqlalchemy-158f9c54eb32

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Float, DateTime

# Global Variables
SQLITE = 'sqlite'

# Table Names
ASPECTS_HOTELS = 'aspects_hotels'
COMMENTS = 'comments'
FEATURE_CATEGORY = 'feature_category'
HOTELS = 'hotels'
REVIEWS = 'reviews'
PREFERENCES = 'preferences'
HOTELS_USERS = 'hotels_users'
WORKER_PREFERENCES = 'worker_preferences'
ACTIONS = 'actions'
CHOICES = 'choices'


class MyDatabase:
    # http://docs.sqlalchemy.org/en/latest/core/engines.html
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}'
    }

    # Main DB Connection Ref Obj
    db_engine = None

    def __init__(self, dbtype, username='', password='', dbname=''):
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            self.db_engine = create_engine(engine_url)
            print(self.db_engine)
        else:
            print("DBType is not found in DB_ENGINE")

    def create_db_tables(self):
        metadata = MetaData()
        # hotels = Table(HOTELS, metadata,
        #               Column('hotelID', Integer, primary_key=True),
        #               Column('name', String),
        #               Column('num_reviews', Integer),
        #               Column('price', Integer),
        #               Column('score', Float))
        reviews = Table(REVIEWS, metadata,
                        Column('id', Integer, primary_key=True),
                        Column('hotel_id', None, ForeignKey('hotels.hotelID')),
                        Column('city', String),
                        Column('country', String),
                        Column('author', String),
                        Column('score', Float),
                        Column('review_id', String),
                        Column('review_text', String)
                        )
        # aspects_hotels = Table(ASPECTS_HOTELS, metadata,
        #                        Column('hotelID', Integer),
        #                        Column('aspect', String),
        #                        Column('comments_positive', Integer),
        #                        Column('comments_negative', Integer)
        #                        )
        # comments = Table(COMMENTS, metadata,
        #                  Column('hotelID', Integer),
        #                  Column('reviewID', Integer),
        #                  Column('author', String),
        #                  Column('score', Integer),
        #                  Column('sentence', String),
        #                  Column('feature', String),
        #                  Column('polarity', String),
        #                  Column('category_f', Integer)
        #                  )
        # feature_category = Table(FEATURE_CATEGORY, metadata,
        #                          Column('feature', String),
        #                          Column('category', String)
        #                          )
        # preferences = Table(PREFERENCES, metadata,
        #                     Column('userID', Integer),
        #                     Column('0', String),
        #                     Column('1', String),
        #                     Column('2', String),
        #                     Column('3', String),
        #                     Column('4', String)
        #                     )
        # hotels_users = Table(HOTELS_USERS, metadata,
        #                      Column('rank', Integer),
        #                      Column('160', Integer),
        #                      Column('822', Integer),
        #                      Column('50', Integer),
        #                      Column('373', Integer),
        #                      Column('197', Integer),
        #                      Column('183', Integer),
        #                      Column('240', Integer),
        #                      Column('193', Integer),
        #                      Column('351', Integer),
        #                      Column('840', Integer)
        #                      )
        # worker_preferences = Table(WORKER_PREFERENCES, metadata,
        #                            Column('workerID', String),
        #                            Column('aspect', String),
        #                            Column('order', Integer)
        #                            )
        # actions = Table(ACTIONS, metadata,
        #                 Column('action_type', String),
        #                 Column('page', String),
        #                 Column('feature', String),
        #                 Column('description', String),
        #                 Column('date', DateTime)
        #                 )

        try:
            metadata.create_all(self.db_engine)
            print("Tables created")
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)

    # Insert, Update, Delete
    def execute_query(self, query=''):
        if query == '': return
        print(query)
        with self.db_engine.connect() as connection:
            try:
                connection.execute(query)
            except Exception as e:
                print(e)

    def print_all_data(self, table='', query=''):
        query = query if query != '' else "SELECT * FROM '{}';".format(table)
        print(query)
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                for row in result:
                    print(row)  # print(row[0], row[1], row[2])
                result.close()
        print("\n")

    # Examples
    def sample_query(self):
        # Sample Query
        query = "SELECT first_name, last_name FROM {TBL_USR} WHERE " \
                "last_name LIKE 'M%';".format(TBL_USR=HOTELS)
        self.print_all_data(query=query)
        # Sample Query Joining
        query = "SELECT u.last_name as last_name, " \
                "a.email as email, a.address as address " \
                "FROM {TBL_USR} AS u " \
                "LEFT JOIN {TBL_ADDR} as a " \
                "WHERE u.id=a.user_id AND u.last_name LIKE 'M%';" \
            .format(TBL_USR=HOTELS, TBL_ADDR=REVIEWS)
        self.print_all_data(query=query)

    def sample_delete(self):
        # Delete Data by Id
        query = "DELETE FROM {} WHERE id=3".format(HOTELS)
        self.execute_query(query)
        self.print_all_data(HOTELS)
        # Delete All Data
        '''
        query = "DELETE FROM {}".format(USERS)
        self.execute_query(query)
        self.print_all_data(USERS)
        '''

    def sample_insert(self):
        # Insert Data
        query = "INSERT INTO {}(hotelID, name, num_reviews) " \
                "VALUES (5, 'Nuevo',12);".format(HOTELS)
        self.execute_query(query)
        self.print_all_data(HOTELS)

    def sample_update(self):
        # Update Data
        query = "UPDATE {} set name='XXXX' WHERE hotelID={id}" \
            .format(HOTELS, id=3)
        self.execute_query(query)
        self.print_all_data(HOTELS)

# # import sqlite3
# #
# # # Create BD
# # try:
# #     sqliteConnection = sqlite3.connect('test1.db')
# #     cursor = sqliteConnection.cursor()
# #     print("Database created and Successfully Connected to SQLite")
# #
# #     sqlite_select_Query = "select sqlite_version();"
# #     cursor.execute(sqlite_select_Query)
# #     record = cursor.fetchall()
# #     print("SQLite Database Version is: ", record)
# #     cursor.close()
# #
# # except sqlite3.Error as error:
# #     print("Error while connecting to sqlite", error)
# # finally:
# #     if (sqliteConnection):
# #         sqliteConnection.close()
# #         print("The SQLite connection is closed")
# #
# # # Create tables
# # try:
# #     sqliteConnection = sqlite3.connect('test1.db')
# #     sqlite_create_table_query = '''CREATE TABLE SqliteDb_developers (
# #                                 id INTEGER PRIMARY KEY,
# #                                 name TEXT NOT NULL,
# #                                 email text NOT NULL UNIQUE,
# #                                 joining_date datetime,
# #                                 salary REAL NOT NULL);'''
# #
# #     cursor = sqliteConnection.cursor()
# #     print("Successfully Connected to SQLite")
# #     cursor.execute(sqlite_create_table_query)
# #     sqliteConnection.commit()
# #     print("SQLite table created")
# #
# #     cursor.close()
# #
# # except sqlite3.Error as error:
# #     print("Error while creating a sqlite table", error)
# # finally:
# #     if (sqliteConnection):
# #         sqliteConnection.close()
# #         print("sqlite connection is closed")
# #
# # # insert values
# # try:
# #     sqliteConnection = sqlite3.connect('test1.db')
# #     cursor = sqliteConnection.cursor()
# #     print("Successfully Connected to SQLite")
# #
# #     sqlite_insert_query = """INSERT INTO SqliteDb_developers
# #                           (id, name, email, joining_date, salary)
# #                            VALUES
# #                           (1,'James','james@pynative.com','2019-03-17',8000)"""
# #
# #     count = cursor.execute(sqlite_insert_query)
# #     sqliteConnection.commit()
# #     print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
# #     cursor.close()
# #
# # except sqlite3.Error as error:
# #     print("Failed to insert data into sqlite table", error)
# # finally:
# #     if (sqliteConnection):
# #         sqliteConnection.close()
# #         print("The SQLite connection is closed")
# #
# # # back up DB
# # import sqlite3
# # def progress(status, remaining, total):
# #     print(f'Copied {total-remaining} of {total} pages...')
# #
# # try:
# #     #existing DB
# #     sqliteCon = sqlite3.connect('test1.db')
# #     #copy into this DB
# #     backupCon = sqlite3.connect('test1.db')
# #     with backupCon:
# #         sqliteCon.backup(backupCon, pages=3, progress=progress)
# #     print("backup successful")
# # except sqlite3.Error as error:
# #     print("Error while taking backup: ", error)
# # finally:
# #     if(backupCon):
# #         backupCon.close()
# #         sqliteCon.close()
#
#
# from sqlalchemy import create_engine, ForeignKey
# from sqlalchemy import Column, Date, Integer, String, Float
# from sqlalchemy.ext.declarative import declarative_base
# import pandas as pd
# engine = create_engine('sqlite:///hotels.db', echo=True)
# #engine = create_engine('sqlite:///C:\\sqlitedbs\\IntExplanations.db', echo=True)
# Base = declarative_base()
# # data_path='C:\Python\IntExplanations\data'
# # hotels=pd.read_csv(data_path+'/hotels.csv',sep='\t')
# class Hotels(Base):
#     __tablename__ = "hotels"
#     hotelID = Column(Integer, primary_key=True)
#     name = Column(String)
#     num_reviews = Column(Integer)
#     price = Column(Integer)
#     score = Column(Float)
#
#     def __init__(self, name):
#         self.name = name
#
# # class Reviews(Base):
# #     __tablename__ = "reviews"
# #     idRev = Column(Integer, primary_key=True)
# #     nameRev = Column(String)
# #
# #     def __init__(self, name):
# #         self.name = name
#
# Base.metadata.create_all(engine)
# #
# # # # access the mapped Table
# # # Hotels.__table__
# # # ins = Hotels.insert()
# #
# # from sqlalchemy import create_engine
# # engine = create_engine('sqlite:///test1.db', echo=True)
# #
# # # from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Float
# # # metadata = MetaData()
# # # hotels = Table('hotels', metadata,
# # #     Column('hotelID', Integer, primary_key=True),
# # #     Column('name', String),
# # #     Column('num_reviews', Integer),
# # #     Column('price', Integer),
# # #     Column('score', Float)
# # #  )
# # # Base.metadata.create_all(engine)
