import json, inspect, discord, asyncio
from helper.cEmbed import granted_msg, denied_msg
from helper.cLog import elog
from helper.Algorithm import Algorithm
from cDatabase.DB_Algorithm import DB_Algorithm

config = json.load(open('config.json', 'r'))

path = __file__.split(config['split_path'])
file = path[len(path) - 1][:-3]

db_algo = DB_Algorithm('db_algorithms')

# ------------------ [ is_admin_only() ] ------------------ #
    # Limits this command to only admin users (i.e. Ahmad, Khaled, MB, Miguel)
def is_admin_only(): return False

# ------------------ [ usage() ] ------------------ #
    # Returns how the command is called ex. "[prefix][command]"
def usage(): return file + " [algorithm] + (language)"

# ------------------ [ description() ] ------------------ #
    # Returns a short explanation of what the function does
def description(): return "searches Available Algorithms"

def get_new_msg(curr_page, title, lst_algorithms, lst_languages, lst_ids):
    response = granted_msg(title, f"Page {curr_page + 1}/{len(lst_algorithms)}")
    response.add_field(name = "ID", value = lst_ids[curr_page], inline = True)
    response.add_field(name = "Algorithm", value = lst_algorithms[curr_page], inline = True)
    response.add_field(name = "Languages", value = lst_languages[curr_page], inline = True)
    return response

async def pages(msg, title, lst_algorithms, lst_languages, lst_ids, client):
    pages = len(lst_algorithms)
    curr_page = 0

    bot_msg = await msg.channel.send(embed = get_new_msg(curr_page, title, lst_algorithms, lst_languages, lst_ids))

    await bot_msg.add_reaction("◀️")
    await bot_msg.add_reaction("▶️")
    

    def check(reaction, user):
        return user == msg.author and str(reaction.emoji) in ["◀️", "▶️"]

    while True:
        try:
            reaction, user = await client.wait_for("reaction_add", timeout= 60, check= check)

            if str(reaction.emoji) == "▶️" and curr_page + 1 != pages:
                curr_page += 1
                await bot_msg.edit(embed = get_new_msg(curr_page, title, lst_algorithms, lst_languages, lst_ids))
                await bot_msg.remove_reaction(reaction, user)
            
            elif str(reaction.emoji) == "◀️" and curr_page > 0:
                curr_page -= 1
                await bot_msg.edit(embed = get_new_msg(curr_page, title, lst_algorithms, lst_languages, lst_ids))
                await bot_msg.remove_reaction(reaction, user)
            
            else: await bot_msg.remove_reaction(reaction, user)

        except asyncio.TimeoutError:
            await bot_msg.clear_reactions()
            break

async def execute(msg, args, client):
    try:
        if len(args) == 0 or len(args[0]) == 0:
            await msg.reply(embed = denied_msg("Invalid Search Query", ""))
            return
        
        keyword = args[0]
        language = (args[1] if len(args) > 1 else None)
        
        str_algorithms, str_languages, str_ids = str(), str(), str()
        lst_algorithms, lst_languages, lst_ids = list(), list(), list()

        arr = sorted(db_algo.inv.items(), key= lambda x : x[0])
        i = 0
        for (name, _id) in arr:
            if i != 0 and i % 15 == 0:
                lst_algorithms.append(str_algorithms)
                lst_languages.append(str_languages)
                lst_ids.append(str_ids)
                str_algorithms = str_languages = str_ids = ""
            
            algo = Algorithm(_id= _id)

            if language != None and language not in algo.get_langs(): continue
            if not algo.is_valid_mapping(keyword): continue

            str_algorithms += algo.algo + "\n"
            str_languages += str(algo.get_langs()) + "\n"
            str_ids += "**" + algo._id + "**\n"
            i += 1

        if len(str_algorithms) != 0:
            lst_algorithms.append(str_algorithms)
            lst_languages.append(str_languages)
            lst_ids.append(str_ids)
            str_algorithms = str_languages = str_ids = ""

        if len(lst_algorithms) == 0:
            await msg.reply(embed = denied_msg("Empty Search Results", ""))
            return

        title = "Search Results for `algo= '" + keyword + "'`"
        if language != None: title += ", `lang= '" + language + "'`"

        await pages(msg, title, lst_algorithms, lst_languages, lst_ids, client)
    
    except Exception as ex:
        elog(ex, inspect.stack()) 
        await msg.reply(embed = denied_msg())