# ------------------ [ Authors: ] ------------------ #
    # Ahmad Zaaroura
    # Khaled Chehabeddine
    # Miguel Merheb

import os, json, inspect, discord, asyncio, importlib, keep_alive, sys
from helper.cLog import elog
from helper.cEmbed import denied_msg, greeting_msg
from helper.User import User
from helper.Algorithm import Algorithm
from cDatabase.DB_Users import DB_Users
from helper.GitHub import GitHub
from helper.CF_API import CF_API
from cDatabase.DB_Algorithm import DB_Algorithm
from cDatabase.DB_Settings import DB_Settings

config = json.load(open('config.json', 'r'))

client = discord.Client(intents= discord.Intents.all())

available_commands = dict()
available_modules = dict() # dict of dicts
db_users = DB_Users('db_users')
db_algo = DB_Algorithm('db_algorithms')
db_settings = DB_Settings('db_settings')
cf_api = CF_API()
github_api = GitHub()


def init_available_commands():
    for (t1, t2, folder) in os.walk(config['cmds_loc']):
        for item in folder:
            if item[-3:] != '.py': continue
            available_commands[item[:-3]] = importlib.import_module(config['cmds_loc'][2:] + '.' + item[:-3])

def init_available_modules():
    for (path, general_folder, folder) in os.walk(config['module_cmds_loc']):
        for inner_folder in general_folder: available_modules[inner_folder] = {}
        current_folder = path.split(config["split_path"])[-1]
        for item in folder:
            if item[-3:] != ".py": continue
            file_path = config['module_cmds_loc'][2:] + "." + current_folder + "." + item[:-3]
            available_modules[current_folder][item[:-3]] = importlib.import_module(file_path)

def init_available_algorithms():
    algo_lst = github_api.get_all_files()
    algo_all = Algorithm().all()
    for algo in algo_all:
        if algo in algo_lst: continue
        Algorithm(str_algo= algo).delete()

    for algo in algo_lst: 
        x = Algorithm(str_algo= algo)
        if x.lang not in ['cpp', 'java', 'py']: continue
        x.add()

# ------------------ [ init() ] ------------------ #
    # Iterates over names in "folder" file of "config["cmds_loc"]"
    # Verifies if name is a command by checking if last 3 letters == ".py"
    # Commands added to "available_commands", otherwise skipped
    # Throws an exception if any error occurs while running, logged using "elog()" function
def init():
    try:
        init_available_commands()
        init_available_modules()
        init_available_algorithms()
        return True
    except Exception as ex: 
        elog(ex, inspect.stack())
        return False

# ------------------ [ on_ready() ] ------------------ #
    # Runs after running main.py
    # Calls [ init() ]
    # Sets bot status to "playing [prefix]help"
@client.event
async def on_ready(): 
    if not init():
        sys.exit('Check Error Log')

    await client.change_presence(activity = discord.Game(config['default_prefix'] + "help"))
    #await client.change_presence(status = discord.Status.offline)
    print("Bot online.")

# ------------------ [ on_message() ] ------------------ #
    # Runs after a user sends a message
    # Checks if command called is not empty ex. "[prefix]"
    # Checks if command called is in "available_commands"
    # Throws an exception if any occurs while running, logged using "elog()" function
        # Error message "denied_msg" sent to appropriate channel
@client.event
async def on_message(msg):
    try:
        prefix = db_settings.get_prefix(msg.guild)

        if msg.content[:len(prefix)] != prefix or msg.author.bot: return
        args = msg.content[len(prefix):].split()

        if (len(args) == 0): return
        command = args[0]

        if command in available_commands.keys(): 
            if command != "register" and not User(id= msg.author.id).is_registered():
                desc = "You are not registered yet.\nUse `" + prefix + "register [YOUR_HANDLE]`"
                await msg.reply(embed = denied_msg("Error", desc))
                return
            await available_commands[command].execute(msg, args[1:], client)
            return

        module = command
        if module in available_modules.keys():
            if len(args) < 2:
                desc = "Try `" + prefix + module + " help` to see available commands for this module"
                await msg.reply(embed = denied_msg("Warning", desc))
                return
            command = args[1]
            if not command in available_modules[module].keys(): return
            if command in ["help", "admin-help"]: await available_modules[module][command].execute(msg, args[2:], client, module)
            elif command in ["commit"]: await available_modules[module][command].execute(msg, msg.content[len(prefix):].split('\n'), client)
            else: await available_modules[module][command].execute(msg, args[2:], client)

    except Exception as ex:
        elog(ex, inspect.stack()) 
        await msg.reply(embed = denied_msg())

# fix on member join
# implement on member leave (remove CodeX from DM)
@client.event
async def on_member_join(member):
    try:
        prefix = db_settings.get_prefix(member.guild)

        channel = discord.DMChannel
        await channel.send(member, embed= greeting_msg(prefix)) 

        await channel.send(member, "First of all, you're gonna need a CodeForces account. If you don't have one, you can register on https://codeforces.com/register !!")
        await channel.send(member, "Please Enter Your CodeForces Handle: ")

        def is_valid(response):
            handle = response.content
            return cf_api.is_valid_handle(handle) and not User(handle= handle).is_taken_handle()

        try:
            msg = await client.wait_for('message', check= is_valid, timeout= 60.0)
            user = User(id= msg.author.id, handle= msg.content, client= client)

            if user.is_taken_id(): user.change_handle(msg.content)
            else: user.register()

            await user.update_roles()
        except asyncio.TimeoutError:
            desc = "Use `" + prefix + "register [YOUR_HANDLE]` to register!"
            await channel.send(member, embed = denied_msg("You Took Too Long To Answer", desc))
            return

        await channel.send(member, User(id= member.id).tag() + ", Welcome to The Team!!")
    except Exception as ex:
        elog(ex, inspect.stack()) 
        await channel.send(member, embed = denied_msg())

@client.event
async def on_member_remove(member):
    try:
        channel = discord.DMChannel

        User(id= member.id).delete()

        await channel.send(member, User(id= member.id).tag() + ", We're Sorry to See You Go!")
    except Exception as ex:
        elog(ex, inspect.stack()) 
        await channel.send(member, embed = denied_msg())

# ------------------ [ my_background_task__Role_Management() ] ------------------ #
    # Runs after the bot becomes online
    # Checks that each user in the user database of the bot has the correct role
    # based on his rank on codeforces
    # Checks 1 user each 5 seconds
    # 1 loop over the users each 3 hours
async def my_background_task__Role_Management():
    await client.wait_until_ready()
    await asyncio.sleep(2)
 
    while not client.is_closed():
        for (user_id, user_handle) in db_users.items():
            await asyncio.sleep(5)
            user = User(id = user_id, handle = user_handle, client = client)
            await user.update_roles()
        await asyncio.sleep(3 * 60 * 60)

# Initialize db_setting on_guild_join

#client.loop.create_task(my_background_task__Role_Management())
#keep_alive.keep_alive()
client.run(config['Discord_Token'])