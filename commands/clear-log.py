import inspect, json
from helper.cLog import elog
from helper.cEmbed import denied_msg, granted_msg
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
def description(): return "Clears the Error Log."

# ------------------ [ execute() ] ------------------ #
    # Checks if the author is an admin, returns "denied_msg" if true, otherwise "granted_msg"
    # Clears the "error_log.log" file
    # Sends a message confirming the log was cleared
    # Throws an exception if any error occurs, logs it with "elog" and sends "denied_msg"
async def execute(msg, args, client):
    try:
        author = User(id = str(msg.author.id))
        if not author.is_admin():
            desc = msg.author.mention + " You are not allowed to use this function."
            await msg.reply(embed = denied_msg("Admin Command", desc))
            return None

        fs = open('./logs/error_log.log', 'w')
        fs.seek(0)
        fs.truncate()
        fs.close()
        await msg.channel.send(embed = granted_msg("Error Log Cleared Successfully", ""))
    except Exception as ex:
        elog(ex, inspect.stack())
        await msg.reply(embed = denied_msg())