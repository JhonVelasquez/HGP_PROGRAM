""" import hashlib

#print(hashlib.algorithms_guaranteed)

bytes

password = "hgp!123"

e_8 = password.encode('utf-8')

h_8 = hashlib.sha3_512()
h_8.update(e_8)
print(h_8.hexdigest())




from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

class MySQLDatabase:
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
    
    def ping(self):
        try:
            with self.engine.connect() as connection:
                # Execute a simple query to ensure the database exists
                result = connection.execute(text("SELECT 1"))
                if result.fetchone():
                    print("Successfully connected to the database")
                    return True
                else:
                    print("Failed to connect to the database")
                    return False
        except SQLAlchemyError as e:
            print(f"Error occurred: {e}")
            return False
        


sqlite_engine = ("sqlite:///.\\db\\hgp_dev.db")
mysql_engine = ("mysql+pymysql://root:R0ck0!@localhost:3306/hgp_dev")

db = MySQLDatabase(mysql_engine)

if db.ping():
    print("Successfully connected to the database")
else:
    print("Failed to connect to the database")







 """


import os
import re
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from urllib.parse import urlparse

def validate_connection_string(connection_string):
    sqlite_pattern = re.compile(r'sqlite:///(.+)')
    mysql_pattern = re.compile(r'mysql\+pymysql://[^:]+:[^@]+@[^:]+:\d+/[^/]+')

    if sqlite_pattern.match(connection_string):
        return 'sqlite'
    elif mysql_pattern.match(connection_string):
        return 'mysql'
    else:
        return None

def get_absolute_path(connection_string):
    parsed_url = urlparse(connection_string)
    db_path = parsed_url.path

    # Handle both forward and backward slashes
    if db_path.startswith('/') or db_path.startswith('\\'):
        db_path = db_path[1:]

    # Normalize and get the absolute path
    db_file = os.path.abspath(os.path.normpath(db_path))
    return db_file

def verify_path_existance(connection_string):
    db_file = get_absolute_path(connection_string)
    return os.path.exists(db_file)

def validate_db_url(connection_string):
    db_type = validate_connection_string(connection_string)
    if db_type == 'sqlite':
        if verify_path_existance (connection_string):
            try:
                return True , (f"Path exists: {db_type}")
            except SQLAlchemyError as e:
                print(f"Error occurred: {e}")
                return False, (f"Error occurred: {e}")
        else:
            print(f"The SQLite database file {connection_string} does not exist.")
            return False, (f"The SQLite database file {connection_string} does not exist.")
    elif db_type == 'mysql':
        # MySQL database
        try:
            return True , (f"Path exists: {db_type}")
        except SQLAlchemyError as e:
            print(f"Error occurred: {e}")
            return False, (f"Error occurred: {e}")
    else:
        print("Invalid or unsupported connection string format")
        return False, ("Invalid or unsupported connection string format")

def ping_database(connection_string):
    engine = create_engine(connection_string)
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            if result.fetchone():
                print("Successfully connected to the database")
                return True, ("Successfully connected to the database")
            else:
                print("Failed to connect to the database")
                return False, ("Failed to connect to the database")
    except SQLAlchemyError as e:
        print(f"Error occurred: {e}")
        return False, (f"Error occurred: {e}")

def validate_ping_db(connection_string):
    validate, mval = validate_db_url(connection_string)
    if(validate):
        return ping_database(connection_string)
    else:
        return False, mval
    
# Example usage:
# SQLite example with standard and additional valid formats
sqlite_connection_string1 = "sqlite:///path_to_existing_database.db"

print("Testing SQLite connection string 1:")
a, mssg = validate_ping_db(sqlite_connection_string1)
if (a == True):
    print("SQLite database ping successful")
else:
    print("SQLite database ping failed")

sqlite_connection_string2 = "sqlite:///./db/hgp_dev.db"
print("\nTesting SQLite connection string 2:")
a, mssg = validate_ping_db(sqlite_connection_string2)
if (a == True):
    print("SQLite database ping successful")
else:
    print("SQLite database ping failed")

# MySQL example
mysql_connection_string = "mysql+pymysql://root:R0ck0!@localhost:3306/hgp_dev"
print("\nTesting MySQL connection string:")
a, mssg = validate_ping_db(mysql_connection_string)
if (a == True):
    print("MySQL database ping successful")
else:
    print("MySQL database ping failed")


sqlite_engine = ("sqlite:///.\\db\\hgp_dev.db")
mysql_engine = ("mysql+pymysql://root:R0ck0!@localhost:3306/hgp_dev")
mysql_connection_string = "mysql+pymysql://username:password@host:port/database"
