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
def usage(): return file + " [tag_1] [tag_2]"

# ------------------ [ description() ] ------------------ #
    # Returns a short explanation of what the function does
def description():
    return ("Compare the 2 members.")

async def valid_handle(msg, handle1, handle2):
    try:
        await msg.channel.send("Gathering info for `" + handle1 + "`")
        mp1 = cf_api.get_statistics(handle1)
        await msg.channel.send("Gathering info for `" + handle2 + "`")
        mp2 = cf_api.get_statistics(handle2)

        keys, col1, col2 = "", "", ""
        for (k, v) in mp1.items(): 
            keys += k + "\n"
            col1 += (v if v != None else "--") + "\n"
            col2 += (mp2[k] if mp2[k] != None else "--") + "\n"

        response = granted_msg("`" + handle1 + "` vs `" + handle2 + "`")
        base = "https://cfviz.netlify.app/compare.html"
        req = "?handle1=" + handle1 + "&handle2=" + handle2
        response.url = base + req
        
        response.add_field(name= '\u200b', value= keys, inline= True)
        response.add_field(name= handle1, value= col1, inline= True)
        response.add_field(name= handle2, value= col2, inline= True)
  
        await msg.channel.send(embed = response)
    except Exception as ex:
        elog(ex, inspect.stack())
        await msg.reply(embed = denied_msg())

async def check_args(msg, args):
    if len(args) != 2 or len(msg.mentions) != 2:
        await msg.reply(embed = denied_msg("Invalid Command Format", ""))
        return False

    user1 = User(id= msg.mentions[0].id)
    user2 = User(id= msg.mentions[1].id)

    if not (user1.is_registered() and user2.is_registered()):
        await msg.reply(embed = denied_msg("Tagged Member is not registered", ""))
        return False

    return [user1.handle, user2.handle]

# ------------------ [ execute() ] ------------------ #
    # Checks if there are commands in "available_commands"
    # Adds only non-admin commands into the embed
    # Throws an exception if any error occurs, logs it with "elog" and sends "denied_msg"
async def execute(msg, args, client):
    try:
        args = await check_args(msg, args)
        if args == False: return

        await valid_handle(msg, args[0], args[1])

    except Exception as ex:
        elog(ex, inspect.stack())
        await msg.channel.send(embed = denied_msg())