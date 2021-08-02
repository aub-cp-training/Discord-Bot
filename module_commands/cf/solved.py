import os, importlib, json, inspect
from helper.cEmbed import granted_msg, denied_msg
from helper.cLog import elog
from helper.User import User
from helper.CF_API import CF_API

config = json.load(open('config.json', 'r'))

path = __file__.split(config['split_path'])
file = path[len(path) - 1][:-3]

cf_api = CF_API()

# ------------------ [ is_admin_only() ] ------------------ #
    # Anybody can use this command
def is_admin_only(): return False

# ------------------ [ usage() ] ------------------ #
    # Returns how the command is called ex. "[prefix][command]"
def usage(): return file

# ------------------ [ description() ] ------------------ #
    # Returns a short explanation of what the function does
def description():
    return ("Displays Solved CodeForces Problems of the Specified User.\n**Usage:**```"
            + file + "          --> Yourself\n" 
            + file + " [tag]    --> Tagged Member\n"
            + file + " [handle] --> Provided Handle```")

async def valid_handle(msg, info, lst):
    try:
        response = granted_msg("Solved Problems")
        response.set_author(
            name = info.handle,
            url = "https://codeforces.com/profile/" + info.handle,
            icon_url = info.title_photo,
        )
        response.set_thumbnail(url = info.avatar)
    
        for (k, v) in lst['problems']:
            response.add_field(name = k, value = v)
    
        response.add_field(name = "\u200b", value = '\u200b', inline = False)

        response.add_field(name = "Problemset", value = lst['problemset'])
        response.add_field(name = "Gym", value = lst['gym'])
        response.add_field(name = "Total Solved", value = lst['total'], inline = False)
  
        await msg.channel.send(embed = response)
    except Exception as ex:
        elog(ex, inspect.stack())
        await msg.reply(embed = denied_msg())

# ------------------ [ execute() ] ------------------ #
    # Checks if there are commands in "available_commands"
    # Adds only non-admin commands into the embed
    # Throws an exception if any error occurs, logs it with "elog" and sends "denied_msg"
async def execute(msg, args, client):
    try:
        user = None
    
        if (len(args) == 0): user = User(id = str(msg.author.id))
        elif len(msg.mentions) != 0:
            if msg.mentions[0].bot: 
                await msg.reply(embed = denied_msg("No Bots", ""))
                return
            user = User(id = str(msg.mentions[0].id))
        else:
            user = User(handle = args[0])

        if (user.id != None and user.handle == None):
            await msg.reply(embed = denied_msg("User is Not Registered Yet", ""))
            return

        try:
            info = cf_api.user_info(user)
            lst = cf_api.solved_problems(user)
        except Exception:
            await msg.reply(embed = denied_msg("Invalid Handle", ""))
            return

        await valid_handle(msg, info, lst)

    except Exception as ex:
        elog(ex, inspect.stack())
        await msg.channel.send(embed = denied_msg())