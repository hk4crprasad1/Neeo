from gemini_pro_bot.bot import start_bot

from flask import Flask,render_template
from threading import Thread
import os

app = Flask(__name__)
@app.route('/')
def index():
    return "Alive"
def run():
  app.run(host='0.0.0.0',port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    keep_alive()
    start_bot()
