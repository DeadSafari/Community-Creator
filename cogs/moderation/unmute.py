import asyncio
import datetime
import json
import os
import discord
from discord.ext import commands
import time as Time
from cogs.functions import add_moderation_log
from uuid import uuid4

class Unmute(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log("cogs.moderation.unmute is now ready!")

    @discord.app_commands.command(
        name="unmute",
        description="Unmutes the specified user."
    )
    @discord.app_commands.describe(
        member="The member to unmute.",
        reason="The reason for unmuting the member."
    )
    @discord.app_commands.checks.has_any_role("Moderators", "Head Moderator", "Administrators", "Head Administrator", "Owner")
    @discord.app_commands.guilds(int(os.getenv("MAIN_GUILD")))
    async def _unmute(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await interaction.response.defer()
        if discord.utils.get(interaction.guild.roles, name="Muted") not in member.roles:
            await interaction.edit_original_response(content=":x: This user is not muted.")
            return
        if not reason:
            reason = "No reason provided."
        if member == interaction.user:
            await interaction.edit_original_response(content=":x: You cannot unmute yourself.")
            return
        if member.top_role >= interaction.user.top_role:
            await interaction.edit_original_response(content=":x: You cannot unmute this user.")
            return
        dmBed = discord.Embed(
            title=f"You have been unmuted in {interaction.guild.name}.",
            description=f"**Reason:** {reason}\n**Moderator:** {interaction.user.mention}",
            color=0xff0000
        )
        try:
            await member.send(embed=dmBed)
        except:
            pass
        try:
            await member.remove_roles(discord.utils.get(interaction.guild.roles, name="Muted"))
        except Exception as e:
            await interaction.edit_original_response(content=f":x: An error occurred while unmuting the user.```py\n{e}```")
            return
        await add_moderation_log(
            user_id=member.id,
            moderator_id=interaction.user.id,
            time=-1,
            Type="unmute",
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
                title="Member Unmuted",
                description=f"**User:** {member.mention}\n**Moderator:** {interaction.user.mention}\n**Reason:** {reason}",
                color=0xff0000
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_footer(text=f"User ID: {member.id}")
            await logs_channel.send(embed=embed)
        else:
            await interaction.edit_original_response(content=f":white_check_mark: {member.mention} has been unmuted. | No logs channel found.")
            return
        await interaction.edit_original_response(content=f":white_check_mark: {member.mention} has been unmuted.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Unmute(bot))