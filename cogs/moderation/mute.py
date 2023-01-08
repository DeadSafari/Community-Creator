import asyncio
import datetime
import json
import discord
from discord.ext import commands
import time as Time
from cogs.functions import add_moderation_log
from uuid import uuid4
import os

class Mute(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log("cogs.moderation.mute is now ready!")
        self.loop = asyncio.get_running_loop()
        with open("tasks.json", mode="r") as f:
            data = json.load(f)
        for task in data['mutes']:
            guild = self.bot.get_guild(task['guild'])
            memebrID = task['member']
            try:
                user = await guild.fetch_member(memebrID)
            except: 
                data['mutes'].remove(task)
                continue
            seconds = (datetime.datetime.utcnow() - datetime.datetime.fromtimestamp(task['seconds'])).total_seconds()
            role = discord.utils.get(guild.roles, name="Muted")
            self.loop.call_later(seconds, asyncio.create_task, user.remove_roles(role))
        with open("tasks.json", mode="w") as f:
            json.dump(data, f, indent=4)

    @discord.app_commands.describe(
        member="The member to mute.",
        time="The time to mute the member for.",
        reason="The reason for muting the member."
    )
    @discord.app_commands.checks.has_any_role("Moderators", "Head Moderator", "Administrators", "Head Administrator", "Owner")
    @discord.app_commands.guilds(int(os.getenv("MAIN_GUILD")))
    async def _mute(self, interaction: discord.Interaction, member: discord.Member, time: str = None, reason: str = None):
        await interaction.response.defer()
        if discord.utils.get(interaction.guild.roles, name="Muted") in member.roles:
            await interaction.edit_original_response(content=":x: This user is already muted.")
            return
        if time:
            timeDict = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800, "o": 2592000, "y": 31536000}
            try:
                seconds = int(time[:-1]) * timeDict[time[-1].lower()]
            except KeyError:
                await interaction.edit_original_response(":x: Invalid time unit.")
                return
                
        else: 
            seconds = -1
        dmBed = discord.Embed(
            title=f"You have been muted in {interaction.guild.name}.",
            description=f"**Reason:** {reason}\n**Time:** {'Permanent' if time == None else time}\n**Moderator:** {interaction.user.mention}",
            color=0xff0000
        )
        try:
            await member.send(embed=dmBed)
        except:
            pass
        if not reason:
            reason = "No reason provided."
        if member == interaction.user:
            await interaction.edit_original_response(content=":x: You cannot mute yourself.")
            return
        if member.top_role >= interaction.user.top_role:
            await interaction.edit_original_response(content=":x: You cannot mute this user.")
            return
        try:
            await member.add_roles(discord.utils.get(interaction.guild.roles, name="Muted"))
        except Exception as e:
            await interaction.edit_original_response(content=f":x: An error occurred while muting the user.```py\n{e}```")
            return
        await add_moderation_log(
            user_id=member.id,
            moderator_id=interaction.user.id,
            time=seconds,
            Type="mute",
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
                title="Member Muted",
                description=f"**User:** {member.mention}\n**Moderator:** {interaction.user.mention}\n**Reason:** {reason}\n**Time:** {'Permanent' if time == None else time}",
                color=0xff0000
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_footer(text=f"User ID: {member.id}")
            await logs_channel.send(embed=embed)
        else:
            await interaction.edit_original_response(content=f":white_check_mark: {member.mention} has been muted. | No logs channel found.")
            return
        await interaction.edit_original_response(content=f":white_check_mark: {member.mention} has been muted.")
        if seconds == -1: return
        with open("tasks.json", "r") as f:
            tasks = json.load(f)
            tasks['mutes'].append({
                "member": member.id,
                "guild": interaction.guild.id,
                "seconds": datetime.datetime.timestamp(datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds))
            })
        with open("tasks.json", "w") as f:
            json.dump(tasks, f, indent=4)

        self.loop.call_later(seconds, asyncio.create_task, member.remove_roles(discord.utils.get(interaction.guild.roles, name="Muted")))

async def setup(bot: commands.Bot):
    await bot.add_cog(Mute(bot))