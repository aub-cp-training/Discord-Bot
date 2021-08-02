import inspect, json
from helper.cLog import elog
from helper.cEmbed import denied_msg
from helper.User import User

config = json.load(open('config.json', 'r'))

path = __file__.split(config['split_path'])
file = path[len(path) - 1][:-3]

# ------------------ [ is_admin_only() ] ------------------ #
    # Limits this command to only admin users (i.e. Ahmad, Khaled, MB, Miguel)
def is_admin_only(): return True

# ------------------ [ usage() ] ------------------ #
    # Returns how the command is called ex. "[prefix][command]"
def usage(): return file

# ------------------ [ description() ] ------------------ #
    # Returns a short explanation of what the function does
def description(): return "Displays the Error Log."

# ------------------ [ execute() ] ------------------ #
    # Checks if the author is an admin, returns "denied_msg" if true, otherwise "granted_msg"
    # Creates a string "errorlogs" containing all error logs of "error_log.log"
    # Checks if string is valid, if not, sends "denied_msg", otherwise sends "errorlogs"
    # Throws an exception if any error occurs, logs it with "elog" and sends "denied_msg"
async def execute(msg, args, client):
    try:
        author = User(id = str(msg.author.id))
        if not author.is_admin():
            desc = msg.author.mention + " You are not allowed to use this function."
            await msg.reply(embed = denied_msg("Admin Command", desc))
            return None

        fs = open('./logs/error_log.log', 'r')
        errorlogs = ""
        for line in fs.readlines(): errorlogs += line + '\n'
    
        if (len(errorlogs) == 0):
            await msg.reply(embed = denied_msg("Error Log is Empty", ""))
            return

        await msg.channel.send("```" + errorlogs + "```")
        fs.close()
    except Exception as ex:
        elog(ex, inspect.stack())
        await msg.reply(embed = denied_msg())