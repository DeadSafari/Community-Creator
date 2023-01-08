import asyncio
import datetime
import json
import discord
from discord.ext import commands
import time as Time
from cogs.functions import add_moderation_log, delete_moderation_log, get_mod_log
from uuid import uuid4
import os

class Delete(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log("cogs.moderation.delete is now ready!")

    @discord.app_commands.command(
        name="delete",
        description="Deletes the specified mod log."
    )
    @discord.app_commands.describe(
        uuid="The UUID of the log to delete."
    )
    @discord.app_commands.checks.has_any_role("Moderators", "Head Moderator", "Administrators", "Head Administrator", "Owner")
    @discord.app_commands.guilds(int(os.getenv("MAIN_GUILD")))
    async def _delete(self, interaction: discord.Interaction, uuid: str):
        await interaction.response.defer()
        try:
            logs = await get_mod_log(uuid)
        except:
            await interaction.edit_original_response(content=":x: This log does not exist.")
            return
        await delete_moderation_log(uuid)
        await interaction.edit_original_response(content=":white_check_mark: This log has been deleted.")
        return

async def setup(bot: commands.Bot):
    await bot.add_cog(Delete(bot))