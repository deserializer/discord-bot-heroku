#import
import os
TOKEN = os.getenv("TOKEN")


#cleint (the bot)
client = discord.client()

#Do stuff

if __name__ == "__main__":
    client.run(TOKEN)
