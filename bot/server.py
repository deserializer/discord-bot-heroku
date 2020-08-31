from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main():
  return 'discord.gg/KXX7BHE'

def run():
  app.run(host='0.0.0.0', port=8080)

def server():
  server = Thread(target=run)
  server.start()
