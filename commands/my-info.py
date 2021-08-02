import inspect, json
from helper.cLog import elog
from helper.cEmbed import granted_msg, denied_msg

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
def description(): return "Shows User's Dircord Identification Card."

# ------------------ [ execute() ] ------------------ #
    # Creates embed of user's discord information
    # Tries if user has a nickname and role, throws exception and passes if an error occurs
    # Throws exception "ex" if any error occurs, logs it with "elog" and sends "denied_msg"
async def execute(msg, args, client):
    try:
        user = msg.author
        response = granted_msg(
            "Discord Identification Card", 
            "This is a description of user: " + str(user)
        )
        response.set_thumbnail(url = user.avatar_url)
        response.add_field(
            name = "Name: ", 
            value = user.name, 
        )
        response.add_field(
            name = "ID: ", 
            value = user.id,
        )
        response.add_field(
            name = '\u200b',
            value = '\u200b'
        )
        try:
            response.add_field(
                name = "Nickname: ", 
                value = user.nick, 
            )
            response.add_field(
                name = "Top Role: ", 
                value = user.top_role.name, 
            )
        except Exception: pass
        await msg.channel.send(embed = response)
    except Exception as ex:
        elog(ex, inspect.stack())
        await msg.reply(embed = denied_msg())