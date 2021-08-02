import inspect, json
from helper.cEmbed import granted_msg, denied_msg
from helper.cLog import elog
from helper.CF_API import CF_API

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
def description(): return "Displays Current or Upcoming CodeForces Contests."

async def execute(msg, args, client):
    try:
        response = granted_msg("Current or Upcoming CodeForces Contests")

        d = CF_API().codeforces_contests()

        names = dates = durations = str()
        for v in d.values():
            names += v['name'] + '\n'
            dates += v['date'] + '\n'
            durations += v['duration'] + '\n'
            for i in range(len(v['name']) // 48):
                dates += '\n'
                durations += '\n'

        if len(names) == 0:
            desc = "No Current or Upcoming Contests"
            await msg.channel.send(embed = denied_msg("Warning", desc))
            return

        response.add_field(name = 'Name', value = names, inline = True)
        response.add_field(name = 'Date', value = dates, inline = True)
        response.add_field(name = 'Duration', value = durations, inline = True)

        await msg.channel.send(embed = response)

    except Exception as ex:
        elog(ex, inspect.stack())
        await msg.reply(embed = denied_msg())