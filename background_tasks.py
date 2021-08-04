import asyncio
from cDatabase.DB_Users import DB_Users
from helper.User import User

db_users = DB_Users('db_users')

# ------------------ [ my_background_task__Role_Management() ] ------------------ #
    # Runs after the bot becomes online
    # Checks that each user in the user database of the bot has the correct role
    # based on his rank on codeforces
    # Checks 1 user each 5 seconds
    # 1 loop over the users each 3 hours
async def my_background_task__Role_Management(client):
    await client.wait_until_ready()
    await asyncio.sleep(2)
 
    while not client.is_closed():
        for (user_id, user_handle) in db_users.items():
            await asyncio.sleep(5)
            user = User(id = user_id, handle = user_handle, client = client)
            await user.update_roles()
        await asyncio.sleep(3 * 60 * 60)