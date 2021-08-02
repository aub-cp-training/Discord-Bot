import json, discord
from helper.cTime import MyDate

config = json.load(open('config.json', 'r'))
icon_url = config['icon_url']

# ------------------ [ granted_msg() ] ------------------ #
    # Creates a default embed for any valid commands
def granted_msg(_title, desc = ""):
    response = discord.Embed(
        title = _title,
        description = desc,
        color = discord.Color.green(),
    )
    response.set_footer(
        text = "CodeX • " + MyDate().footer(),
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
        text = "CodeX • " + MyDate().footer(),
        icon_url = icon_url
    )
    return response