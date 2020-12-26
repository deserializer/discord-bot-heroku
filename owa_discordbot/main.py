from owa_discordbot import settings
from owa_discordbot.client import OwaClient

client = OwaClient(config=settings.OWA_CONFIG)
client.run()
