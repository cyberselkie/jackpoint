import sqlite3
import logging
from sqlite3.dbapi2 import Error

"""
Description:
Handles all things database.
"""
# IMPORTS
#import [Module/Package]
import sqlite3
import logging
from sqlite3.dbapi2 import Error

#? Configures the logger to log messages of the "INFO" severity level or higher.
logging.basicConfig(level=logging.INFO)

class Shadow_DB():
    """
    Description:
    This class encapsulates the flow of database management into a single database object.
    """
    #? CONSTRUCTOR
    def __init__(self) -> None:
        pass

    def connect_db(self, filename: str=':memory:'):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        global db
        db = None
        try:
            db = sqlite3.connect(filename)
        except Error as e:
            print(e)

        return db

    def insert_data(self,sql_statement, values):
        """
        Create a new project into the projects table
        :param conn:
        :param project:
        :return: project id
        """
        cur = db.cursor()
        cur.execute(sql_statement,values)
        return cur.lastrowid

    def view_data(self,table):
        """
        This method selects everything from the chosen table.
        """
        cursor = db.cursor()    # Creates Cursor
        query = f'SELECT * FROM {table}'
        cursor.execute(query)    
        rows = cursor.fetchall()
        print(f"rows data type: {type(rows)}\n")
        for row in rows:
            print(row)
        cursor.close()

    def exit_db(self):
        """
        This method closes the database.
        """
        db.commit()
        db.close()

def main_db(filename, sql_statement, values):
    data = Shadow_DB()
    data.connect_db(filename)
    data.insert_data(sql_statement, values)
