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

def usage(): return file + " [tag] [new_handle]"

def description():
    return "Change The Handle of the Tagged User."
          
async def check_args(msg, args):
    author = User(id = str(msg.author.id))
    if not author.is_admin():
        desc = msg.author.mention + " You are not allowed to use this function."
        await msg.reply(embed = denied_msg("Admin Command", desc))
        return None

    if len(args) < 2:
      desc = msg.author.mention + " Please tag someone and provide a handle."
      await msg.reply(embed = denied_msg("Command Format Error", desc))
      return None

    if msg.mentions[0].bot:
      desc = msg.author.mention + " No Bots Allowed."
      await msg.reply(embed = denied_msg("Warning", desc))
      return None

    user = User(id = str(msg.mentions[0].id))

    if not user.is_registered():
      desc = user.tag() + " is not registered"
      await msg.reply(embed = denied_msg("Warning", desc))
      return None

    if User(handle = args[1]).is_taken_handle():
        desc = "`" + user.handle + "` is already assigned to another user."
        await msg.reply(embed = denied_msg("Warning", desc))
        return None
  
    try:
      cf_api.user_info(User(handle = args[1]))
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

    if user.change_handle(args[1]):
        await user.update_roles()
        response = granted_msg("Change Handle")
        response.description = user.tag() + "'s handle has been successfully changed"
        await msg.channel.send(embed = response)
    else:
        await msg.reply(embed = denied_msg("We faced an error while connecting to the database", ""))
        return

  except Exception as ex:
    elog(ex, inspect.stack())
    await msg.reply(embed = denied_msg())
    return