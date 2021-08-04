import inspect, json
from helper.cEmbed import denied_msg
from helper.cLog import elog
from helper.LeaderBoard import LeaderBoard
from cDatabase.DB_Users import DB_Users
from helper.CF_API import CF_API

config = json.load(open('config.json', 'r'))

path = __file__.split(config['split_path'])
file = path[len(path) - 1][:-3]

db_users = DB_Users("db_users")
cf_api = CF_API()

# ------------------ [ is_admin_only() ] ------------------ #
    # Anybody can use this command
def is_admin_only(): return False

# ------------------ [ usage() ] ------------------ #
    # Returns how the command is called ex. "[prefix][command]"
def usage(): return file

# ------------------ [ description() ] ------------------ #
    # Returns a short explanation of what the function does
def description(): return "Displays the current codeforces standings based on ratings."

async def execute(msg, args, client):
    try:
        lst = cf_api.multiple_user_ratings(db_users.values())
        await msg.channel.send(embed = LeaderBoard().Standings(lst))
    except Exception as ex:
        elog(ex, inspect.stack())
        await msg.reply(embed = denied_msg())