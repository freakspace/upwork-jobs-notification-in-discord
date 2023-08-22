import os
import asyncio
import locale

from dotenv import load_dotenv

import discord
from discord.ext import commands

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(intents=intents, auto_sync_commands=True)

cogs_list = ["upwork"]

for cog in cogs_list:
    print(f"Loading {cog}")
    bot.load_extension(f"cogs.{cog}")


def main():
    environment = os.getenv("ENVIRONMENT")
    print(f"Running bot in: {environment}")
    token = os.getenv("DISCORD_TOKEN")

    loop = asyncio.get_event_loop()
    loop.create_task(bot.start(token))

    loop.run_forever()


if __name__ == "__main__":
    main()
