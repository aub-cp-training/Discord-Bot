import json, inspect
from helper.cEmbed import granted_msg, denied_msg
from helper.cLog import elog

config = json.load(open('config.json', 'r'))

path = __file__.split(config['split_path'])
file = path[len(path) - 1][:-3]

# ------------------ [ is_admin_only() ] ------------------ #
    # Anybody can use this command
def is_admin_only(): return False

# ------------------ [ usage() ] ------------------ #
    # Returns how the command is called ex. "[prefix][command]"
def usage(): return file

# ------------------ [ description() ] ------------------ #
    # Returns a short explanation of what the function does
def description(): return "Displays information about me!"
  
# ------------------ [ execute() ] ------------------ #
    # Creates and sends an embed that gives the user info about KFC Bot
    # Throws an exception if an error occurs, logs it in "elog" and sends "denied_msg"
async def execute(msg, args, client):
    try:
        response = granted_msg("InFo AbOuT mE! ^_^")
        response.color = 0x302dd7
        response.add_field(
            name = "Framework",
            value = "Discord.py"
        )
        response.add_field(
            name = "Born on",
            value = "..."
        )
        response.add_field(
            name = "Version",
            value = config['version']
        )
        response.add_field(
            name = "Version Release Date", 
            value = "..."
        )
        response.add_field(
            name = "Developers", 
            value = "Khaled Chehabeddine, Ahmad Zaaroura, and Miguel Merheb",
            inline = False
        )
        response.add_field(
            name = "\u200b", 
            value = "***More Features Coming Soon!\nStay tuned***",
            inline = False
        )
        await msg.channel.send(embed = response)
    except Exception as ex:
        elog(ex, inspect.stack())
        await msg.reply(embed = denied_msg())