import json
from threading import Thread
from flask import Flask
from background_tasks import my_background_task__Role_Management
from main import client

app = Flask('')
config = json.load(open('config.json', 'r'))

@app.route('/')
def main():
    return "Your bot is alive!"

app.run(debug=True)
client.loop.create_task(my_background_task__Role_Management(client))
client.run(config['Discord_Token'])
