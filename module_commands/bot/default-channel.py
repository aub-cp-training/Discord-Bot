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
def usage(): return file + ' [channel_mention]'

# ------------------ [ description() ] ------------------ #
    # Returns a short explanation of what the function does
def description(): return "Set the default_channel for the bot"

# ------------------ [ execute() ] ------------------ #
    # Checks if there are commands in "available_commands"
    # Adds only non-admin commands into the embed
    # Throws an exception if any error occurs, logs it with "elog" and sends "denied_msg"
async def execute(msg, args, client):
    try:
        lst = msg.channel_mentions
        if len(lst) != 1:
            await msg.reply(embed = denied_msg("Please Mention a Channel", ""))
            return

        channel = lst[0]
        if str(channel.category) != "Text Channels":
            await msg.reply(embed = denied_msg("Please Mention a Text Channel", ""))
            return

        db_settings.set_default_channel(msg.guild, channel.id)

        await msg.channel.send(embed = granted_msg("Default Channel Changed Successfully"))
    except Exception as ex:
        elog(ex, inspect.stack())
        await msg.reply(embed = denied_msg())