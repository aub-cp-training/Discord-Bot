import json, inspect, discord
from helper.cEmbed import denied_msg
from helper.cLog import elog
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
def is_admin_only(): return False

# ------------------ [ usage() ] ------------------ #
    # Returns how the command is called ex. "[prefix][command]"
def usage(): return  file + " [algorithm] (language)"

# ------------------ [ description() ] ------------------ #
    # Returns a short explanation of what the function does
def description(): return "Gets the code of the specified algorithm."

# ------------------ [ check_args() ] ------------------ #
    # Checks if the command called by the user is valid
async def check_args(msg, args):
    if len(args) < 1:
        await msg.reply(embed = denied_msg("Invalid Command Format", usage()))
        return False

    isID = (args[0] in db_algo.keys())

    if len(args) == 1:
        av_langs = db_algo.get_langs(Algorithm(_id= args[0]) if isID else Algorithm(algo= args[0]))
        lang = av_langs[0] if len(av_langs) == 1 else 'cpp'
    else: lang = args[1]

    if isID: algo = Algorithm(_id= args[0], lang= lang)
    else: algo = Algorithm(algo= args[0], lang= lang)
    
    if not algo.is_found():
        await msg.reply(embed = denied_msg("Error", "Algorithm is not available yet."))
        return False

    return algo

async def execute(msg, args, client):
    try:
        algo = await check_args(msg, args)
        if algo == False : return

        await msg.channel.send("Loading `" + str(algo) + "` . . .")
        file_path = algo.get_code_path()
        await msg.channel.send(file= discord.File(file_path, str(algo)))
    
    except Exception as ex:
        elog(ex, inspect.stack()) 
        await msg.reply(embed = denied_msg())
    
