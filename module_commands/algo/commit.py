import json, inspect
from helper.User import User
from helper.cEmbed import granted_msg, denied_msg
from helper.GitHub import GitHub
from helper.cLog import elog
from helper.Algorithm import Algorithm
from cDatabase.DB_Algorithm import DB_Algorithm

config = json.load(open('config.json', 'r'))

path = __file__.split(config['split_path'])
file = path[len(path) - 1][:-3]

github_api = GitHub()
db_algo = DB_Algorithm('db_algorithms')

# ------------------ [ is_admin_only() ] ------------------ #
    # Limits this command to only admin users (i.e. Ahmad, Khaled, MB, Miguel)
def is_admin_only(): return True

# ------------------ [ usage() ] ------------------ #
    # Returns how the command is called ex. "[prefix][command]"
def usage(): return  file + " [algorithm] ([code] OR [file_attachment])"

# ------------------ [ description() ] ------------------ #
    # Returns a short explanation of what the function does
def description(): 
    return (
        "Creates a new file in the repository.\n" +
        "```" + file + " [algorithm] [code]\n" +
        file + " [algorithm] [file_attachment]```\n" +
        "Notes: \n```\n" +
        "`[code]` format: '''[lang]\\n [code] \\n'''\n" + 
        "`[file_attachment]` name format:\n" + 
        "   .zip: [algo]__[lang].zip            \n" +
        "   .cpp, .java, .py: [algo].[lang]     \n```"
    )

# ------------------ [ check_args() ] ------------------ #
    # Checks if the command called by the user is valid
async def check_args(msg, args):
    author = User(id = str(msg.author.id))
    if not author.is_admin():
        description = msg.author.mention + " You are not allowed to use this function."
        await msg.reply(embed = denied_msg("Admin Command", description))
        return False

    flag = (len(msg.attachments) == 0 and len(args) >= 4 and len(args[0].split()) == 3)
    flag = flag or (len(msg.attachments) == 1 and len(args) == 1 and len(args[0].split()) == 3)

    if not flag:
        await msg.reply(embed = denied_msg("Invalid Command Format", usage()))
        return False

    if len(msg.attachments) == 1: 
        algo = args[0].split()[-1]
        filename = msg.attachments[0].filename.split('.')
        extension = filename[-1]

        if extension == 'zip':
            if len(filename) != 2 or len(filename[0].split("__")) != 2:
                await msg.reply(embed= denied_msg("Invalid File Name", ""))
                return False
            file_path = config['module_cmds_loc'] + "/algo/code.zip"
            await msg.attachments[0].save(file_path)
            filename = filename[0].split("__")
            algo = Algorithm(algo= filename[0], lang= filename[1], is_zip= True)
        else:
            if len(filename) != 2:
                await msg.reply(embed= denied_msg("Invalid File Name", ""))
                return False

            file_path = config['module_cmds_loc'] + "/algo/code.txt"
            await msg.attachments[0].save(file_path)

            with open(file_path, 'r') as f: code = f.read()

            algo = Algorithm(algo= filename[0], lang= extension, code= code, is_zip= False)
    else: 
        algo = args[0].split()[-1]
        lang = args[1].strip('`')
        code = '\n'.join(args[2 : -1])
        file_path = config['module_cmds_loc'] + "/algo/code.txt"
        with open(file_path, 'w') as f: f.write(code)
        algo = Algorithm(algo= algo, lang= lang, code= code, is_zip= False)

    if algo.lang not in ['cpp', 'java', 'py']:
        await msg.reply(embed = denied_msg("Invalid Language", "Try one of `cpp`, `java`, `py`"))
        return False

    if algo.is_found():
        await msg.reply(embed = denied_msg("Error", "Algorithm already exists in this language"))
        return False

    return algo

async def execute(msg, args, client):
    try:
        algo = await check_args(msg, args)
        if algo == False: return

        result = algo.commit()

        if result == True:
            algo.add()
            await msg.channel.send(embed = granted_msg("Algorithm Added Succesfully", str(algo)))
        else:
            elog(result, inspect.stack()) 
            desc = "We faced an error while uploading the file.\n"
            desc += "Consider trying again in a couple of minutes."
            await msg.reply(embed = denied_msg("Error", desc))
    
    except Exception as ex:
        elog(ex, inspect.stack()) 
        await msg.reply(embed = denied_msg())
    
