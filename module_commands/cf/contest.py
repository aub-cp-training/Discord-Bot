from helper.cLog import elog
from helper.cEmbed import granted_msg, denied_msg
from helper.CF_API import CF_API
import inspect, json

config = json.load(open('config.json', 'r'))

cf_api = CF_API()

path = __file__.split(config['split_path'])
file = path[len(path) - 1][:-3]

# ------------------ [ is_admin_only() ] ------------------ #
    # Anybody can use this command
def is_admin_only(): return False

# ------------------ [ usage() ] ------------------ #
    # Returns how the command is called ex. "[prefix][command]"
def usage(): return file + " [contest_id]"

# ------------------ [ description() ] ------------------ #
    # Returns a short explanation of what the function does
def description(): return "Displays the rating changes of the specified contest."

# ------------------ [ check_args() ] ------------------ #
    # Checks if the command called by the user is valid
async def check_args(msg, args):
    if len(args) == 0:
        desc = msg.author.mention + " Please enter a contest id"
        await msg.reply(embed = denied_msg("Command Format Warning", desc))
        return None

    try:
        int(args[0])
        if not (1 <= int(args[0]) <= 2000): raise Exception
    except Exception:
        desc = msg.author.mention + " Invalid Contest ID"
        await msg.reply(embed = denied_msg("Command Warning", desc))
        return None
    
    lst, contest = cf_api.contest_rating_changes(int(args[0]))
    if (lst == None):
        desc = msg.author.mention + " No Ratings Currently Available For The Specified Contest"
        await msg.reply(embed = denied_msg("Command Warning", desc))
        return None

    if len(lst) == 0:
        desc = msg.author.mention + " No Registered Member Officially Participated in This Contest"
        await msg.reply(embed = denied_msg("Result Warning", desc))
        return None

    return [contest] + lst

# ------------------ [ execute() ] ------------------ #
    # Creates a session object and stores it into the database
    # Creates and sends an embed message to "channel" containing session info 
    # Throws an exception if any error occurs, logs it with "elog" and sends "denied_msg"
async def execute(msg, args, client):
    try:

        lst = await check_args(msg, args)
        if (lst == None): return
        contest = lst[0]
        lst = lst[1:]

    

        response = granted_msg("Contest Rating Changes")

        ranks = handles = ratings  = ""
        for (r, h, o, n) in lst:
            ranks += "**" + str(r) + "**" + "\n"
            handles += str(h) + "\n"
            ratings += str(o) + "--" +  str(n) + "\n"

        response.description = contest

        response.add_field(name = "Rank", value = ranks)
        response.add_field(name = "Handle", value = handles)
        response.add_field(name = "Old-New Rating", value = ratings)
  
        await msg.channel.send(embed = response)
    except Exception as ex:
        elog(ex, inspect.stack())
        await msg.reply(embed = denied_msg())