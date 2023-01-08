import asyncio
import datetime
import json
import os
import discord
from discord.ext import commands
import time as Time
from cogs.functions import add_moderation_log
from uuid import uuid4

class Purge(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log("cogs.moderation.purge is now ready!")

    @discord.app_commands.command(
        name="purge",
        description="Deletes the specified amount of messages."
    )
    @discord.app_commands.guilds(int(os.getenv("MAIN_GUILD")))
    async def _purge(self, interaction: discord.Interaction, amount: int):
        await interaction.response.defer()
        messages = await interaction.channel.purge(limit=amount)
        a = str(uuid4())
        listMessages = []
        for message in messages:
            listMessages.append(
                f"{message.created_at} - {message.author}: {message.content}"
            )
        with open(a, 'w') as f:
            json.dump({"messages": listMessages}, f, indent=4)
        
        file = discord.File(a, filename=f"{a}.json")
        for channel in interaction.guild.text_channels:
            if "staff-logs" == channel.name[-10:]:
                logs_channel = channel
                break
            else:
                logs_channel = None
        if logs_channel:
            embed=discord.Embed(
                title="Channel Purged",
                description=f"Channel: {interaction.channel.mention}\nAmount: {amount}\nModerator: {interaction.user.mention}",
                color=0xff0000
            )
            embed.set_thumbnail(url=interaction.user.avatar.url)
            embed.set_footer(text=f"User ID: {interaction.user.id}")
            await logs_channel.send(embed=embed, file=file)
        os.remove("./"+a)
        await interaction.channel.send(content=f":white_check_mark: Successfully deleted {amount} messages.", delete_after=5)
        return

async def setup(bot: commands.Bot):
    await bot.add_cog(Purge(bot))