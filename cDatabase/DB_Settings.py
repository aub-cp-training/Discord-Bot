import json
from cDatabase.KV_Database import KV_Database

config = json.load(open('config.json', 'r'))

class DB_Settings(KV_Database):
    def __init__(self, path): 
        super().__init__(path)
        self.db[0] = {
            "prefix": config['default_prefix'],
            "active_tag": config['default_active_tag'],
            "default_channel": None
        }

    def find_guild(self, guild):
        if guild == None: return False
        return guild.id in self.db.keys()

    def add_guild(self, guild):
        if guild == None: return False
        if self.find_guild(guild): return False

        channels = guild.text_channels
        if len(channels) == 0: default_channel = None
        else: default_channel = channels[0].id

        self.db[guild.id] = {
            "prefix": config['default_prefix'],
            "active_tag": config['default_active_tag'],
            "default_channel": default_channel
        }

        self.save()
        return True

    def get_prefix(self, guild):
        if guild == None: return self.db[0]['prefix']
        if not self.find_guild(guild): return None
        return self.db[guild.id]['prefix']

    def get_active_tag(self, guild):
        if guild == None: return self.db[0]['active_tag']
        if not self.find_guild(guild): return None
        return self.db[guild.id]['active_tag']

    def get_default_channel(self, guild):
        if guild == None: return self.db[0]['default_channel']
        if not self.find_guild(guild): return None
        return self.db[guild.id]['default_channel']

    def set_prefix(self, guild, prefix):
        if guild == None: return
        if not self.find_guild(guild): self.add_guild(guild)
        self.db[guild.id]['prefix'] = prefix
        self.save()

    def set_active_tag(self, guild, active_tag):
        if guild == None: return
        if not self.find_guild(guild): self.add_guild(guild)
        self.db[guild.id]['active_tag'] = active_tag
        self.save()

    def set_default_channel(self, guild, default_channel):
        if guild == None: return
        if not self.find_guild(guild): self.add_guild(guild)
        self.db[guild.id]['default_channel'] = default_channel
        self.save()