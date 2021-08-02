from cDatabase.KV_Database import KV_Database

# ------------------------------------ { DB_Users } ------------------------------------ # 
    # Inherits from KV_Database
class DB_Users(KV_Database):
    # ------------------ [ __init__() ] ------------------ # 
        # Initializes a new database with the specified path
    def __init__(self, path):
        super().__init__(path)

    # ------------------ [ find_id() ] ------------------ # 
        # Returns the ID registered to this handle in the database
        # Returns None if the handle wan't found
    def find_id(self, handle):
        for (k, v) in self.db.items():
            if (v == handle): return k
        return None

    # ------------------ [ find_handle() ] ------------------ # 
        # Returns the handle registered to this ID in the database
        # Returns None if the handle wasn't found
    def find_handle(self, _id):
        if (_id in self.db.keys()): return self.db[_id]
        return None

    # ------------------ [ is_taken_id() ] ------------------ # 
        # Returns True if the ID is already in the database
        # And False otherwise
    def is_taken_id(self, user):
        return (user.id in self.db.keys())

    # ------------------ [ is_taken_handle() ] ------------------ # 
        # Returns True if the handle is already registered to any ID in the database
        # And False otherwise
    def is_taken_handle(self, user):
        for (k, v) in self.db.items():
            if (v == user.handle): return True
        return False

    # ------------------ [ is_registered() ] ------------------ # 
        # Returns True if the pair (ID, Handle) is in the database
        # False otherwise
    def is_registered(self, user):
        for (k, v) in self.db.items():
            if (k == user.id and v == user.handle): return True
        return False

    # ------------------ [ register() ] ------------------ # 
        # Registers a new user to the database
        # Returns True if registration was successful, and False otherwise
    def register(self, user):
        if (self.is_taken_handle(user)): return False
        if (self.is_taken_id(user)): return False
        self.db[user.id] = user.handle
        self.save()
        return True

    # ------------------ [ change_handle() ] ------------------ # 
        # Changes the handle of the user, to "new_handle"
    def change_handle(self, user, new_handle):
        self.db[user.id] = new_handle
        self.save()
        return True

    # ------------------ [ remove_user() ] ------------------ # 
        # Removes a user from the database
    def remove_user(self, user):
        if (not self.is_registered(user)): return True
        del(self.db[user.id])
        self.save()
        return True