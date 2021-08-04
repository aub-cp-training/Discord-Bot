import json, discord
from helper.cTime import MyDate

config = json.load(open('config.json', 'r'))
icon_url = config['icon_url']
bot_name = "CodeX"

# ------------------ [ granted_msg() ] ------------------ #
    # Creates a default embed for any valid commands
def granted_msg(_title, desc = ""):
    response = discord.Embed(
        title = _title,
        description = desc,
        color = discord.Color.green(),
    )
    response.set_footer(
        text = bot_name + " • " + MyDate().footer(),
        icon_url = icon_url
    )
    return response

# ------------------ [ denied_msg() ] ------------------ #
    # Creates and sends a message if an invalid command is called
def denied_msg(
        _title = "Error Message", 
        desc = ("There was an error while executing the command.\n"
                + "The error has been logged and will be fixed shortly.")):
    response = discord.Embed(
        title = _title,
        color = discord.Color.red(),
    )
    response.description = desc
    response.set_footer(
        text = bot_name + " • " + MyDate().footer(),
        icon_url = icon_url
    )
    return response

def greeting_msg(prefix):
    desc = f"""
My name is **{bot_name}**.

I was developed by the CP Training Team to help you in your journey.

New features will be added on the go, and members are more than welcome to help keeping me up to date.

To see the currently available commands, type `{prefix}help`!

***Good Luck in your journey!***
    """
    response = discord.Embed(
        title = "Welcome to the AUB CP Training Team",
        description = desc,
        color = discord.Color.blue(),
    )
    response.set_footer(
        text = bot_name + " • " + MyDate().footer(),
        icon_url = icon_url
    )
    return response