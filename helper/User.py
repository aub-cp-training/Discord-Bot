import json, discord
from cDatabase.DB_Users import DB_Users
from cDatabase.KV_Database import KV_Database
from helper.CF_API import CF_API

config = json.load(open('config.json', 'r'))
database_users = DB_Users("db_users")
cf_ranking = KV_Database('CodeForces_Ranking')
cf_api = CF_API()

# ------------------------------------ { User } ------------------------------------ # 
class User:
    id = None
    handle = None
    client = None

    # ------------------ [ __init__() ] ------------------ # 
        # Initializes id and handle based on given parameters
    def __init__(self, id = '', handle = '', client = None):
        if (id != '' and handle != ''):
            self.id, self.handle = str(id), handle
        elif (id != ''):
            self.id = str(id)
            self.handle = database_users.find_handle(self.id)
        elif (handle != ''): 
            self.id = str(database_users.find_id(self.handle))
            self.handle = handle
        self.client = client

    # ------------------ [ is_admin() ] ------------------ # 
        # Returns true if user is Ahmad, Khaled, Miguel, or MB, otherwise false
    def is_admin(self):
        if self.id in [
            '763289145288032268',
            '763319277540605972',
            '763345404674048020',
            '765903184241623041'
        ]: return True
        return False

    # ------------------ [ tag() ] ------------------ # 
        # Tags the user that called the command
    def tag(self):
        return '<@!' + str(self.id) + '>'

    # ------------------ [ is_taken_id() ] ------------------ # 
        # Checks if the ID is already registered
    def is_taken_id(self):
        if (self.id == None): return True
        return database_users.is_taken_id(self)

    # ------------------ [ is_taken_handle() ] ------------------ # 
        # Checks if an ID is already registered to another handle
    def is_taken_handle(self):
        if (self.handle == None): return True
        return database_users.is_taken_handle(self)

    # ------------------ [ is_registered() ] ------------------ # 
        # Checks if user is in the database
    def is_registered(self):
        if (self.id == None or self.handle == None): return False
        return database_users.is_registered(self)

    
    # ------------------ [ register() ] ------------------ # 
        # Registers the user to the bot's database
    def register(self):
        if (self.id == None or self.handle == None): return False
        return database_users.register(self)

    
    # ------------------ [ change_handle() ] ------------------ # 
        # Changes the user's handle in the database
    def change_handle(self, new_handle):
        if (self.handle == new_handle): return False
        if (not self.is_registered()): return False
        self.handle = new_handle
        return database_users.change_handle(self, new_handle)

    
    # ------------------ [ delete() ] ------------------ # 
        # Deletes the user from the database
    def delete(self):
        # Remove from contests
        if (self.id == None or self.handle == None): return False
        return database_users.remove_user(self)

    # ------------------ [ __str__() ] ------------------ # 
        # Returns a string representation of the user with their id and handle
    def __str__(self):
        return "User: " + str(self.id) + ' ' + str(self.handle)

    # ------------------ [ add_role() ] ------------------ # 
        # Adds a role to the to the user in the Discord server
    async def add_role(self, _role):
        guild = self.client.get_guild(config['guild_id'])
        member = await guild.fetch_member(int(self.id))
        role = discord.utils.get(member.guild.roles, name = _role)
        await member.add_roles(role)

    # ------------------ [ get_roles() ] ------------------ # 
        # return a list of all Discord roles of the user
    async def get_roles(self):
        guild = self.client.get_guild(config['guild_id'])
        member = await guild.fetch_member(int(self.id))
        return member.roles

    
    # ------------------ [ has_role() ] ------------------ # 
        # Returns true if the user is a member of the specified role
    async def has_role(self, _role):
        guild = self.client.get_guild(config['guild_id'])
        member = await guild.fetch_member(int(self.id))
        role = discord.utils.get(member.guild.roles, name = _role)
        return role in member.roles

    # ------------------ [ remove_role() ] ------------------ # 
        # Removes the role from the specified member
    async def remove_role(self, _role):
        guild = self.client.get_guild(config['guild_id'])
        member = await guild.fetch_member(int(self.id))
        role = discord.utils.get(member.guild.roles, name = _role)
        await member.remove_roles(role)

    # ------------------ [ get_different_roles() ] ------------------ # 
        # returns a list of all the CodeForces related roles that are not
        # up-to-date with the user's current rank on CodeForces
    async def get_different_roles(self, role):
        roles = await self.get_roles()
        x = cf_ranking.get(role)
        lst = []
       
        for r in roles:
          if r.name in cf_ranking.keys() and cf_ranking.get(r.name) != x:
            lst.append(r.name)

        return lst

    async def update_roles(self):
        rank = cf_api.user_rank(self)
        lst = await self.get_different_roles(rank)
        for r in lst: await self.remove_role(r)
        await self.add_role(rank)
