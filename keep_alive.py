from threading import Thread
from flask import Flask

app = Flask('')

@app.route('/')
def main():
    return "Your bot is alive!"

if __name__ == '__main__':
    app.run(debug=True)
    client.loop.create_task(my_background_task__Role_Management(client))
    client.run(config['Discord_Token'])
