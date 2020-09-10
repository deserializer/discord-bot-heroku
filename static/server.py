from flask import Flask, redirect, url_for, render_template
from threading import Thread
import os

app = Flask('')
port = os.getenv('PORT')

@app.route('/')
def main():
  return render_template('index.html')

def run():
  app.run(host='0.0.0.0', port=port)

def server():
  server = Thread(target=run)
  server.start()
