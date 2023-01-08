import asyncio
import datetime
import json
import discord
from discord.ext import commands
import time as Time
from cogs.functions import add_moderation_log, get_mod_logs
from uuid import uuid4
import os

class Modlogs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log("cogs.moderation.modlogs is now ready!")

    @discord.app_commands.command(
        name="modlogs",
        description="Shows the moderation logs of the specified user."
    )
    @discord.app_commands.describe(
        member="The member to show the logs of."
    )
    @discord.app_commands.checks.has_any_role("Moderators", "Head Moderator", "Administrators", "Head Administrator", "Owner")
    @discord.app_commands.guilds(int(os.getenv("MAIN_GUILD")))
    async def _modlogs(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.defer()
        logs = await get_mod_logs(member.id)
        if not logs:
            await interaction.edit_original_response(content=":x: This user has no moderation logs.")
            return
        embed = discord.Embed(
            title=f"Moderation Logs for {member}",
            color=0xff0000
        )

        embed.set_thumbnail(url=member.avatar.url)

        for log in logs:
            embed.add_field(
                name=f"Type: {log['type'].capitalize()} | {log['uuid']}",
                value=f"""
                **Moderator:** <@{log['moderator_id']}>
                **Reason:** {log['reason']}
                **Time:** {log['time'] if log['time'] != -1 else "Permanent"}
                **Execution Time:** <t:{log['execution_time']}:F>
                """,
                inline=False
            )
        await interaction.edit_original_response(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Modlogs(bot))
