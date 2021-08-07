from threading import Thread
from flask import Flask

ab = Flask('')

@ab.route('/')
def main():
    return "Your bot is alive!"

def run():
    ab.run(host = "0.0.0.0", port = 5001)

def keep_alive():
    server = Thread(target = run)
    server.start()
