import json, inspect
from helper.cLog import elog
from helper.cEmbed import granted_msg, denied_msg
from helper.User import User
from helper.CF_API import CF_API

config = json.load(open('config.json', 'r'))

path = __file__.split(config['split_path'])
file = path[len(path) - 1][:-3]

cf_api = CF_API()

def is_admin_only(): return True

def usage(): return file + " [tag] [handle]"

def description():
  return "Register a new User in the System."

async def check_args(msg, args):
    author = User(id = str(msg.author.id))
    if not author.is_admin():
        desc = msg.author.mention + " You are not allowed to use this function."
        await msg.reply(embed = denied_msg("Admin Command", desc))
        return None

    if len(args) < 2 or len(msg.mentions) == 0:
      desc = msg.author.mention + " Please tag someone and provide a handle."
      await msg.reply(embed = denied_msg("Command Format Error", desc))
      return None

    if msg.mentions[0].bot:
      desc = msg.author.mention + " You Can't Register a Bot."
      await msg.reply(embed = denied_msg("Warning", desc))
      return None

    user = User(id = str(msg.mentions[0].id), handle = args[1])

    if user.is_taken_id():
      desc = user.tag() + " is already registerd as " + user.handle
      await msg.reply(embed = denied_msg("Warning", desc))
      return None

    if user.is_taken_handle():
        desc = "`" + user.handle + "` is already assigned to another user."
        await msg.reply(embed = denied_msg("Warning", desc))
        return None
  
    try:
      cf_api.user_info(user)
    except Exception as ex:
      desc = user.tag() + " Invalid Handle"
      await msg.reply(embed = denied_msg("Assignment Error", desc))
      return None

    return user    
        
async def execute(msg, args, client):
  try:
    user = await check_args(msg, args)
    if (user == None): return
    user.client = client

    if user.register():
        await user.update_roles()
        response = granted_msg("Registration")
        response.description = user.tag() + " is registered successfully"
        await msg.channel.send(embed = response)
    else:
        await msg.reply(embed = denied_msg("We faced an error while registering", ""))
        return

  except Exception as ex:
    elog(ex, inspect.stack())
    await msg.reply(embed = denied_msg())
    return