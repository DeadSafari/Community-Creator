import asyncio
import logging
import os
import traceback
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.token: str = os.getenv("TOKEN")

        self.logger: logging.Logger = logging.getLogger("Bot")

        self.log: function = self.logger.info

        self.main_guild: int = int(os.getenv("MAIN_GUILD"))

    async def on_ready(self):
        self.log("Successfully connected to Discord")
        self.log("=======================================")
        self.log(f"Logged in as: {self.user}")
        self.log(f"User ID: {self.user.id}")
        self.log("=======================================")

    async def on_error(self, error: Exception):
        traceback.print_exc()

bot = Bot(
    command_prefix=os.getenv("PREFIX"),
    case_insensitive=True,
    intents=discord.Intents.all(),
    owner_ids=[int(os.getenv("OWNER_ID"))]
)


async def load_cogs():
    for command in os.listdir('./cogs/moderation'):
        if command.endswith(".py"):
            try:
                bot.log("Attempting to load " + command)
                await bot.load_extension(f"cogs.moderation.{command[:-3]}")
                bot.log("Successfully loaded " + command)
            except:
                traceback.print_exc()
    for cog in os.listdir("./cogs"):
        if cog.endswith(".py"):
            if cog == "functions.py": continue
            try:
                bot.log("Attempting to load " + cog)
                await bot.load_extension(f"cogs.{cog[:-3]}")
                bot.log("Successfully loaded " + cog)
            except:
                traceback.print_exc()
    return

async def start():
    discord.utils.setup_logging()
    await bot.start(bot.token)

async def main():
    await bot.load_extension("jishaku")
    await load_cogs()
    await start()

asyncio.run(main())