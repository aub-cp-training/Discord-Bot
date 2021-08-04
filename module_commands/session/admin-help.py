import os, importlib, json, inspect
from helper.cEmbed import granted_msg, denied_msg
from helper.cLog import elog
from cDatabase.DB_Settings import DB_Settings

config = json.load(open('config.json', 'r'))

path = __file__.split(config['split_path'])
file = path[len(path) - 1][:-3]
available_commands = dict()

db_settings = DB_Settings('db_settings')

# ------------------ [ is_admin_only() ] ------------------ #
    # Admins only
def is_admin_only(): return True

# ------------------ [ usage() ] ------------------ #
    # Returns how the command is called ex. "[prefix][command]"
def usage(parent_file): return parent_file + " " + file

# ------------------ [ description() ] ------------------ #
    # Returns a short explanation of what the function does
def description(parent_file): return "```fix\nDisplays available " + parent_file + " commands of the bot.```"

# ------------------ [ init() ] ------------------ #
    # Iterates over names in "folder" file of "config["cmds_loc"]"
    # Verifies if name is a command by checking if last 3 letters == ".py"
    # Commands added to "available_commands", otherwise skipped
def init(parent_file):
    for (path, general_folder, folder) in os.walk(config['module_cmds_loc']):
        current_folder = path.split(config["split_path"])[-1]
        if current_folder != parent_file: continue
        for item in folder:
            if item[-3:] != ".py": continue
            file_path = config['module_cmds_loc'][2:] + "." + current_folder + "." + item[:-3]
            available_commands[item[:-3]] = importlib.import_module(file_path)

# ------------------ [ execute() ] ------------------ #
    # Checks if there are commands in "available_commands"
    # Adds only non-admin commands into the embed
    # Throws an exception if any error occurs, logs it with "elog" and sends "denied_msg"
async def execute(msg, args, client, parent_file):
    try:
        if len(available_commands) == 0: init(parent_file)     
        prefix = db_settings.get_prefix(msg.guild)
        response = granted_msg("Bot Commands")
        for cmd in available_commands:
            if not available_commands[cmd].is_admin_only(): continue
            if cmd == "admin-help":
                response.add_field(
                    name = prefix + available_commands[cmd].usage(parent_file), 
                    value = available_commands[cmd].description(parent_file), 
                    inline = False
                )
            else:
                response.add_field(
                    name = prefix + parent_file + " " + available_commands[cmd].usage(), 
                    value = available_commands[cmd].description(), 
                    inline = False
                )
        await msg.channel.send(embed = response)
    except Exception as ex:
        elog(ex, inspect.stack())
        await msg.reply(embed = denied_msg())