import asyncio
import datetime
import json
import discord
from discord.ext import commands
import time as Time
from cogs.functions import add_moderation_log
from uuid import uuid4
import os

class Unban(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log("cogs.moderation.unban is now ready!")

    @discord.app_commands.command(
        name="unban",
        description="Unbans the specified user."
    )
    @discord.app_commands.describe(
        member="The member to unban.",
        reason="The reason for unbanning the member."
    )
    @discord.app_commands.checks.has_any_role("Moderators", "Head Moderator", "Administrators", "Head Administrator", "Owner")
    @discord.app_commands.guilds(int(os.getenv("MAIN_GUILD")))
    async def _unban(self, interaction: discord.Interaction, member: discord.User, reason: str = None):
        await interaction.response.defer()
        if not reason:
            reason = "No reason provided."
        if member == interaction.user:
            await interaction.edit_original_response(content=":x: You cannot unban yourself.")
            return
        if member.top_role >= interaction.user.top_role:
            await interaction.edit_original_response(content=":x: You cannot unban this user.")
            return
        try:
            await interaction.guild.unban(member)
        except Exception as e:
            await interaction.edit_original_response(content=f":x: An error occurred while unbanning the user.```py\n{e}```")
            return
        await add_moderation_log(
            user_id=member.id,
            moderator_id=interaction.user.id,
            time=-1,
            Type="unban",
            reason=reason,
            execution_time=int(Time.time()),
            uuid=str(uuid4())
        )
        for channel in interaction.guild.text_channels:
            if "staff-logs" == channel.name[-10:]:
                logs_channel = channel
                break
            else:
                logs_channel = None
        if logs_channel:
            embed = discord.Embed(
                title="Member Unbanned",
                description=f"**User:** {member.mention}\n**Moderator:** {interaction.user.mention}\n**Reason:** {reason}",
                color=0xff0000
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_footer(text=f"User ID: {member.id}")
            await logs_channel.send(embed=embed)
        else:
            await interaction.edit_original_response(content=f":white_check_mark: {member.mention} has been unbanned. | No logs channel found.")
            return
        await interaction.edit_original_response(content=f":white_check_mark: {member.mention} has been unbanned.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Unban(bot))