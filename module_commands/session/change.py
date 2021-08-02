import json, inspect
from helper.User import User
from helper.cTime import MyDate
from helper.cLog import elog, alog
from helper.Session import Session
from cDatabase.DB_Session import DB_Session
from cDatabase.DB_Settings import DB_Settings
from helper.cEmbed import granted_msg, denied_msg

config = json.load(open('config.json', 'r'))

path = __file__.split(config['split_path'])
file = path[len(path) - 1][:-3]

db_settings = DB_Settings('db_settings')
database_session = DB_Session("db_session")

# ------------------ [ is_admin_only() ] ------------------ #
    # Limits this command to only admin users (i.e. Ahmad, Khaled, MB, Miguel)
def is_admin_only(): return True

# ------------------ [ usage() ] ------------------ #
    # Returns how the command is called ex. "[prefix][command]"
def usage(): return (file + " [Session id] date= [mm/dd/yyyy] [hh:mm] dur= [duration]" + 
                            " topic= [topic] desc= (description)")

# ------------------ [ description() ] ------------------ #
    # Returns a short explanation of what the function does
def description(): return "```fix\nModifies a previously created session```"

# ------------------ [ check_args() ] ------------------ #
    # Checks if the command called by the user is valid
async def check_args(msg, args):
    author = User(id = str(msg.author.id))
    if not author.is_admin():
        description = msg.author.mention + " you are not allowed to use this function."
        await msg.reply(embed = denied_msg("Admin Command", description))
        return None
    
    if len(args) < 3:
        description = msg.author.mention + " `" + usage() + "`"
        await msg.reply(embed = denied_msg("Command Format Error", description))
        return None

    if not database_session.find(int(args[0])): 
        description = msg.author.mention + " invalid session ID."
        await msg.reply(embed = denied_msg("Session ID", description))
        return None

    curr_session = Session(_id = int(args[0]))

    start_date, session_duration = curr_session._date, curr_session.duration
    topic, desc_ = curr_session.topic, curr_session.desc

    if "date=" in args: 
        start_date = MyDate(args[args.index("date=") + 1] + ' ' + args[args.index("date=") + 2])
        if not start_date.is_valid():
            description = msg.author.mention + " Please enter a valid starting date and time."
            await msg.reply(embed = denied_msg("Contest Start Time Error", description))
            return None
    
    if "dur=" in args: 
        try:
            session_duration = eval(args[args.index("dur=") + 1])
            assert (session_duration > 0 and session_duration <= 744)
        except:
            await msg.reply(embed = denied_msg("Invalid Session Duration", ""))
            return None
        
    if "topic=" in args: topic = args[args.index("topic=") + 1]
    if "desc=" in args: desc_ = " ".join(args[args.index("desc=") + 1:])

    session = Session(start_date, session_duration, topic, msg.author.name, desc_)
    return [curr_session, session]

# ------------------ [ execute() ] ------------------ #
    # Creates a session object and stores it into the database
    # Creates and sends an embed message to "channel" containing session info 
    # Throws an exception if any error occurs, logs it with "elog" and sends "denied_msg"
async def execute(msg, args, client):
    try:
        args = await check_args(msg, args)
        if (args == None): return
        args[0].change(args[1])

        session = args[1]

        alog(str(msg.author.id) + " modified a session")

        response = granted_msg("ACM Session #" + str(args[0]._id), "")
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
            await msg.reply(embed = granted_msg("Session changed successfully", ""))
    except Exception as ex:
        elog(ex, inspect.stack())
        await msg.reply(embed = denied_msg())