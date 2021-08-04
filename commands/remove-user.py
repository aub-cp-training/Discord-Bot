import json, inspect
from helper.cLog import elog
from helper.cEmbed import granted_msg, denied_msg
from helper.User import User

config = json.load(open('config.json', 'r'))

path = __file__.split(config['split_path'])
file = path[len(path) - 1][:-3]

def is_admin_only(): return True

def usage(): return file + " [tag] [confirmation_key]"

def description():
    return "Remove a User from the system."

async def check_args(msg, args):
    author = User(id = str(msg.author.id))
    if not author.is_admin():
        desc = msg.author.mention + " You are not allowed to use this function."
        await msg.reply(embed = denied_msg("Admin Command", desc))
        return None

    if len(args) < 2:
      desc = msg.author.mention + " Please tag someone and enter the Confirmation Key."
      await msg.reply(embed = denied_msg("Command Format Error", desc))
      return None

    if (args[1] != config['confirmation_key']):
      desc = msg.author.mention + " Invalid Confirmation Key."
      await msg.reply(embed = denied_msg("Warning", desc))
      return None

    if msg.mentions[0].bot:
      desc = msg.author.mention + " You Can't Remove a Bot."
      await msg.reply(embed = denied_msg("Warning", desc))
      return None

    user = User(id = str(msg.mentions[0].id))

    if not user.is_registered():
      desc = user.tag() + " is not registered"
      await msg.reply(embed = denied_msg("Warning", desc))
      return None

    return user    
        
async def execute(msg, args, client):
  try:
    user = await check_args(msg, args)
    if (user == None): return

    if user.delete():
        response = granted_msg("Remove User")
        response.description = user.tag() + " is deleted successfully"
        await msg.channel.send(embed = response)
    else:
        await msg.reply(embed = denied_msg("We faced an error while connecting to the database", ""))
        return

  except Exception as ex:
    elog(ex, inspect.stack())
    await msg.reply(embed = denied_msg())
    return