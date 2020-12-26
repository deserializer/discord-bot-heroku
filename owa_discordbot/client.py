import csv
from pathlib import Path
from typing import List, Dict

import discord, random

class OwaClient(discord.Client):
    def __init__(self, *args, config={}, **kwargs):
        super().__init__()
        self._config = config
        self._prefix = self._config["prefix"]
        self._questions: List[str] = []
        self._load_question_csv(self._config["csv_dir"])
        self._discord_token = self._config["discord_token"]

    def _load_question_csv(self, csv_dir:str):
        csv_dir = Path(csv_dir)
        with open(csv_dir, "r") as f:
            data = csv.reader(f)
            for row in data:
                self._questions.append(row[0])

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.content.startswith(self._prefix):
            cmd = message.content.split(self._prefix)[1]
            if cmd == "q" or cmd == "question":
                # generate question
                picked_question = random.choice(self._questions)
                await message.channel.send(picked_question)
            # TODO
            # elif cmd == "wyr":
            #     # would you rather
            elif cmd == "help" or cmd == "h":
                await message.channel.send(f"-- OwaOwa Bot v0.1 --\nPrefix: `{self._prefix}`\n\nCommand:\n`q` for random question\n`h` for help\n\nExample: `{self._prefix}help`")

    def run(self,  *args, **kwargs):
        return super().run(self._discord_token, *args, **kwargs)
