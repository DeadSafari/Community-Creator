import os
import discord
from discord.ext import commands
from cogs.functions import get_banned_words, add_banned_word, remove_banned_word, create_banned_words_table


class ChatFilter(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot: commands.Bot = bot

    group = discord.app_commands.Group(name="blacklist", description="...", guild_ids=[int(os.getenv("MAIN_GUILD"))])

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log("cogs.moderation.chatfilter is now ready!")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot: return
        if message.guild is None: return

        if message.guild.id != int(os.getenv("MAIN_GUILD")):
            return
        
        words = await get_banned_words()
        words = [x.lower() for x in words]


        messageContent = message.content.split(" ")
        for word in messageContent:
            if word.lower() in words:
                await message.delete()
                embed = discord.Embed(
                    description=f":x: {message.author.mention} you are not allowed to say that word!",
                    color=discord.Color.red()
                )
                await message.channel.send(embed=embed)
                return

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.author.bot: return
        if before.guild is None: return

        if before.guild.id != int(os.getenv("MAIN_GUILD")):
            return
        
        words = await get_banned_words()
        
        messageContent = after.content.split(" ")
        for word in messageContent:
            if word in words:
                await after.delete()
                embed = discord.Embed(
                    description=f":x: {after.author.mention} you are not allowed to say that word!",
                    color=discord.Color.red()
                )
                await after.channel.send(embed=embed)
                return

    @group.command(
        name="add",
        description="Adds a word to the blacklist."
    )
    @discord.app_commands.describe(word="The word to blacklist.")
    async def _add(self, interaction: discord.Interaction, word: str):
        await interaction.response.defer(ephemeral=True)
        words = await get_banned_words()
        if word in words:
            await interaction.edit_original_response(content=":x: That word is already blacklisted!")
            return
        await add_banned_word(word)
        await interaction.edit_original_response(content=":white_check_mark: The word has been blacklisted!")

    @group.command(
        name="remove",
        description="Removes a word from the blacklist."
    )
    @discord.app_commands.describe(word="The word to remove from the blacklist.")
    async def _remove(self, interaction: discord.Interaction, word: str):
        await interaction.response.defer(ephemeral=True)
        words = await get_banned_words()
        if word not in words:
            await interaction.edit_original_response(content=":x: That word is not blacklisted!")
            return
        await remove_banned_word(word)
        await interaction.edit_original_response(content=":white_check_mark: The word has been removed from the blacklist!")

    @group.command(
        name="list",
        description="Lists all the blacklisted words."
    )
    async def _list(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        words = await get_banned_words()
        if len(words) == 0:
            await interaction.edit_original_response(content=":x: There are no blacklisted words!")
            return
        await interaction.edit_original_response(content=f"**Blacklisted words:**\n{', '.join(words)}")
    
async def setup(bot: commands.Bot):
    await create_banned_words_table()
    await bot.add_cog(ChatFilter(bot))