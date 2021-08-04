import json, inspect
from helper.User import User
from helper.cTime import MyDate
from helper.cLog import elog, alog
from helper.Session import Session
from helper.cEmbed import granted_msg, denied_msg
from cDatabase.DB_Settings import DB_Settings

config = json.load(open('config.json', 'r'))

path = __file__.split(config['split_path'])
file = path[len(path) - 1][:-3]

db_settings = DB_Settings('db_settings')

# ------------------ [ is_admin_only() ] ------------------ #
    # Limits this command to only admin users (i.e. Ahmad, Khaled, MB, Miguel)
def is_admin_only(): return True

# ------------------ [ usage() ] ------------------ #
    # Returns how the command is called ex. "[prefix][command]"
def usage(): return  file + " [mm/dd/yyyy] [hh:mm] [duration] [topic] (description)"

# ------------------ [ description() ] ------------------ #
    # Returns a short explanation of what the function does
def description(): return "```fix\nCreates a session and announces it to the server```"

# ------------------ [ check_args() ] ------------------ #
    # Checks if the command called by the user is valid
async def check_args(msg, args):
    author = User(id = str(msg.author.id))
    if not author.is_admin():
        description = msg.author.mention + " You are not allowed to use this function."
        await msg.reply(embed = denied_msg("Admin Command", description))
        return None
    if len(args) < 4:
        description = msg.author.mention + " `" + usage() + "`"
        await msg.reply(embed = denied_msg("Command Format Error", description))
        return None

    start_date = MyDate(args[0] + ' ' + args[1])
    if not start_date.is_valid():
        description = msg.author.mention + " Please enter a valid starting date and time."
        await msg.reply(embed = denied_msg("Contest Start Time Error", description))
        return None

    try:
        session_duration = eval(args[2])
        assert (session_duration > 0 and session_duration <= 744)
    except:
        await msg.reply(embed = denied_msg("Invalid Session Duration", ""))
        return None  

    if len(args) == 4: session = Session(start_date, session_duration, args[3], msg.author.name)
    else: session = Session(start_date, session_duration, args[3], msg.author.name, " ".join(args[4:]))

    if session.is_found():
        description = msg.author.mention + " This session already exists"
        await msg.reply(embed = denied_msg("Session Error", description))
        return None
    return session

# ------------------ [ execute() ] ------------------ #
    # Creates a session object and stores it into the database
    # Creates and sends an embed message to "channel" containing session info 
    # Throws an exception if any error occurs, logs it with "elog" and sends "denied_msg"
async def execute(msg, args, client):
    try:
        session = await check_args(msg, args)
        if (session == None): return

        session_id = session.create()
        alog(str(msg.author.id) + " created a session")

        response = granted_msg("ACM Session #" + str(session._id), "")
        response.add_field(
            name = "Date", 
            value = "```fix\n" + str(session._date) + "```", 
            inline = True
        )
        response.add_field(
            name = "Host",
            value = "```fix\n" + session.host + "```",
            inline = True
        )
        response.add_field(
            name = "Topic", 
            value = "```ini\n" + session.topic + "```", 
            inline = False
        )
        if (session.desc != "-"):
            response.add_field(
                name = "Description", 
                value = "```bash\n" + session.desc + "```", 
                inline = False
            )
        channel = client.get_channel(db_settings.get_default_channel(msg.guild))
        await channel.send(db_settings.get_active_tag(msg.guild))
        await channel.send(embed = response)
        if msg.channel.id != db_settings.get_default_channel(msg.guild):
            await msg.reply(embed = granted_msg("Session created successfully", ""))
    except Exception as ex:
        elog(ex, inspect.stack())
        await msg.reply(embed = denied_msg())