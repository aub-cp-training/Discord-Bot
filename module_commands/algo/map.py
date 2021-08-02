import json, inspect
from helper.User import User
from helper.cEmbed import granted_msg, denied_msg
from helper.cLog import elog
from helper.Algorithm import Algorithm
from cDatabase.DB_Algorithm import DB_Algorithm

config = json.load(open('config.json', 'r'))

path = __file__.split(config['split_path'])
file = path[len(path) - 1][:-3]

db_algo = DB_Algorithm('db_algorithms')

# ------------------ [ is_admin_only() ] ------------------ #
    # Limits this command to only admin users (i.e. Ahmad, Khaled, MB, Miguel)
def is_admin_only(): return True

# ------------------ [ usage() ] ------------------ #
    # Returns how the command is called ex. "[prefix][command]"
def usage(): return  file + " [map_value] [algorithm]"

# ------------------ [ description() ] ------------------ #
    # Returns a short explanation of what the function does
def description(): return "Add a new map_value to the specified algorithm"

# ------------------ [ check_args() ] ------------------ #
    # Checks if the command called by the user is valid
async def check_args(msg, args):
    author = User(id = str(msg.author.id))
    if not author.is_admin():
        description = msg.author.mention + " You are not allowed to use this function."
        await msg.reply(embed = denied_msg("Admin Command", description))
        return False

    if len(args) != 2:
        await msg.reply(embed = denied_msg("Invalid Command Format", usage()))
        return False

    if args[1] in db_algo.keys(): algo = Algorithm(_id= args[1])
    else:
        if args[1] not in db_algo.inv.keys():
            await msg.reply(embed = denied_msg("Error", "Algorithm is not available."))
            return False
        else: algo = Algorithm(algo= args[1])
  
    return [algo, args[0]]

async def execute(msg, args, client):
    try:
        args = await check_args(msg, args)
        if args == False: return

        if args[0].map_to(args[1]):
            await msg.channel.send(embed = granted_msg("Mapping Added Successfully"))
        else:
            elog("Adding Mapping " + args[0] + " to algo " + args[1], inspect.stack()) 
            await msg.reply(embed = denied_msg())
    
    except Exception as ex:
        elog(ex, inspect.stack()) 
        await msg.reply(embed = denied_msg())
    
