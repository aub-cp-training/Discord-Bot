import os, importlib

# ------------------------------------ { KV_Database } ------------------------------------ #
class KV_Database:
    db, path = dict(), str()

    # ------------------ [ exist() ] ------------------ #
        # Returns True if the path already exists
        # and False otherwise
    def exist(self): return os.path.isfile(self.path)

    # ------------------ [ create_file() ] ------------------ # 
        # Creates a new .py file with the specified path
        # And adds the Database module to it
    def create_file(self):
        try:
            file = open(self.path, "w+")
            file.write("DataBase = {}")
            file.close()
            self.db = {}
        except FileNotFoundError as ex:
            print("Error Creating: " + str(ex))
    
    # ------------------ [ load() ] ------------------ # 
        # Loads a database from the specified path
    def load(self):
        try:
            dir = '.'.join(self.path.split('/'))
            db = importlib.import_module(dir[:-3])
            self.db = db.DataBase
        except ImportError as ex:
            print("Error Loading: " + str(ex))

    # ------------------ [ __init__() ] ------------------ # 
        # Initializes a new database with the specified path
    def __init__(self, path):
        self.path = "databases/" + path + ".py"
        if self.exist(): self.load()
        else: self.create_file()

    # ------------------ [ get() ] ------------------ # 
        # Returns the value associated with the given key
    def get(self, key): return self.db[key]

    # ------------------ [ delete_key() ] ------------------ # 
        # Deletes the given key from the database
    def delete_key(self, key): del(self.db[key])

    # ------------------ [ keys() ] ------------------ # 
        # Returns a list of all the keys in the database
    def keys(self): return list(self.db.keys())

    # ------------------ [ items() ] ------------------ # 
        # Returns a list of all the items in the database
    def items(self): return list(self.db.items())

    # ------------------ [ values() ] ------------------ # 
        # Returns a list of (key, value) pairs
    def values(self): return list(self.db.values())

    # ------------------ [ find() ] ------------------ # 
        # Returns True if the key is in the database
        # and False otherwise
    def find(self, key): return (key in self.db.keys())

    # ------------------ [ save() ] ------------------ # 
        # Saves the database to the .py file
    def save(self):
        file = open(self.path, "w+")
        file.write("DataBase = ")
        file.write(str(self.db))
        file.close()

    def clear(self):
        self.db = {}
        self.save()