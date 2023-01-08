import asyncio
import datetime
import json
import discord
from discord.ext import commands
import time as Time
from cogs.functions import add_moderation_log, create_moderation_logs_table
from uuid import uuid4
import os


class Ban(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log("cogs.moderation.ban is now ready!")
        self.loop = asyncio.get_running_loop()
        with open("tasks.json", mode="r") as f:
            data = json.load(f)
        for task in data['bans']:
            memebrID = task['member']
            try:
                user = await self.bot.fetch_user(memebrID)
            except: 
                data['bans'].remove(task)
                continue
            seconds = (datetime.datetime.utcnow() - datetime.datetime.fromtimestamp(task['seconds'])).total_seconds()
            guild = self.bot.get_guild(task['guild'])
            self.loop.call_later(seconds, asyncio.create_task, guild.unban(user))
        with open("tasks.json", mode="w") as f:
            json.dump(data, f, indent=4)

    @discord.app_commands.command(
        name="ban",
        description="Bans the specified user."
    )
    @discord.app_commands.describe(
        member="The member to ban.",
        time="The time to ban the member for.",
        reason="The reason for banning the member."
    )
    @discord.app_commands.checks.has_any_role("Moderators", "Head Moderator", "Administrators", "Head Administrator", "Owner")
    @discord.app_commands.guilds(int(os.getenv("MAIN_GUILD")))
    async def _ban(self, interaction: discord.Interaction, member: discord.Member, time: str = None, reason: str = None, delete_message_days: int = 7):
        await interaction.response.defer()
        if time:
            timeDict = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800, "o": 2592000, "y": 31536000}
            try:
                seconds = int(time[:-1]) * timeDict[time[-1].lower()]
            except KeyError:
                await interaction.edit_original_response(":x: Invalid time unit.")
                return
        else: 
            seconds = -1
        if not reason:
            reason = "No reason provided."
        if member == interaction.user:
            await interaction.edit_original_response(content=":x: You cannot ban yourself.")
            return
        if member.top_role >= interaction.user.top_role:
            await interaction.edit_original_response(content=":x: You cannot ban this user.")
            return
        dmBed = discord.Embed(
            title=f"You have been banned from {interaction.guild.name}.",
            description=f"**Reason:** {reason}\n**Time:** {'Permanent' if time == None else time}\n**Moderator:** {interaction.user.mention}",
            color=0xff0000
        )
        try:
            await member.send(embed=dmBed)
        except:
            pass
        try:
            await member.ban(
                delete_message_days=delete_message_days,
                reason=reason
            )
        except Exception as e:
            await interaction.edit_original_response(content=f":x: An error occurred while banning the user.```py\n{e}```")
            return
        await add_moderation_log(
            user_id=member.id,
            moderator_id=interaction.user.id,
            time=seconds,
            Type="ban",
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
                title="Member Banned",
                description=f"**User:** {member.mention}\n**Moderator:** {interaction.user.mention}\n**Reason:** {reason}\n**Time:** {'Permanent' if time == None else time}",
                color=0xff0000
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_footer(text=f"User ID: {member.id}")
            await logs_channel.send(embed=embed)
        else:
            await interaction.edit_original_response(content=f":white_check_mark: {member.mention} has been banned. | No logs channel found.")
            return
        await interaction.edit_original_response(content=f":white_check_mark: {member.mention} has been banned.")
        if seconds == -1: return
        with open("tasks.json", "r") as f:
            tasks = json.load(f)
            tasks['bans'].append({
                "member": member.id,
                "guild": interaction.guild.id,
                "seconds": datetime.datetime.timestamp(datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds))
            })
        with open("tasks.json", "w") as f:
            json.dump(tasks, f, indent=4)

        self.loop.call_later(seconds, asyncio.create_task, interaction.guild.unban(member))

async def setup(bot: commands.Bot):
    await create_moderation_logs_table()
    await bot.add_cog(Ban(bot))