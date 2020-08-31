from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main():
  return 'https://discord.gg/6GPjN8C'

def run():
  app.run(host='0.0.0.0', port=8080)

def server():
  server = Thread(target=run)
  server.start()
