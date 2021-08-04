import json, inspect, discord
from helper.cEmbed import denied_msg, granted_msg
from helper.cLog import elog
from helper.User import User
from helper.Algorithm import Algorithm
from cDatabase.DB_Algorithm import DB_Algorithm
from helper.GitHub import GitHub

config = json.load(open('config.json', 'r'))

path = __file__.split(config['split_path'])
file = path[len(path) - 1][:-3]

db_algo = DB_Algorithm('db_algorithms')
github_api = GitHub()

# ------------------ [ is_admin_only() ] ------------------ #
    # Limits this command to only admin users (i.e. Ahmad, Khaled, MB, Miguel)
def is_admin_only(): return True

# ------------------ [ usage() ] ------------------ #
    # Returns how the command is called ex. "[prefix][command]"
def usage(): return  file + " [algorithm] [language] [confimartion_key]"

# ------------------ [ description() ] ------------------ #
    # Returns a short explanation of what the function does
def description(): return "Deletes the specified algorithm."

# ------------------ [ check_args() ] ------------------ #
    # Checks if the command called by the user is valid
async def check_args(msg, args):
    author = User(id = str(msg.author.id))
    if not author.is_admin():
        description = msg.author.mention + " You are not allowed to use this function."
        await msg.reply(embed = denied_msg("Admin Command", description))
        return False

    if len(args) != 3:
        await msg.reply(embed = denied_msg("Invalid Command Format", usage()))
        return False

    if args[0] in db_algo.keys(): algo = Algorithm(_id= args[0], lang= args[1])
    else: algo = Algorithm(algo= args[0], lang= args[1])

    if args[2] != config['confirmation_key']:
        await msg.reply(embed = denied_msg("Invalid Confirmation Key", ""))
        return False

    if not algo.is_found():
        await msg.reply(embed = denied_msg("Error", "Algorithm is not available yet."))
        return False

    return algo

async def execute(msg, args, client):
    try:
        algo = await check_args(msg, args)
        if algo == False : return

        github_api.delete_file(str(algo))
        algo.delete()

        await msg.channel.send(embed = granted_msg("Algorithm Deleted Successfully", ""))
    
    except Exception as ex:
        elog(ex, inspect.stack()) 
        await msg.reply(embed = denied_msg())
    
