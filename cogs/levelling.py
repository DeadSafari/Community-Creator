import os
import discord
from discord.ext import commands
from DiscordLevelingCard import RankCard, Settings
import aiosqlite3

async def get_user_rank(user_id: int):
    # Connect to the database
    db = await aiosqlite3.connect('mydatabase.db')

    # Create a cursor
    c = await db.cursor()

    # Select all users from the 'levels' table, sorted by level in descending order
    await c.execute("SELECT * FROM levels ORDER BY level DESC")
    rows = await c.fetchall()

    # Find the rank of the user with the given ID
    rank = 1
    for row in rows:
        if row[0] == user_id:
            break
        rank += 1

    # Close the connection
    await db.close()

    return rank

async def add_user(user_id: int):
    # Connect to the database
    db = await aiosqlite3.connect('mydatabase.db')

    # Create a cursor
    c = await db.cursor()

    # Check if the user is in the database
    await c.execute("SELECT * FROM levels WHERE user_id=?", (user_id,))
    result = await c.fetchone()

    # If the user is not in the database, insert a new row with their data
    if not result:
        await c.execute("INSERT INTO levels (user_id, level, current_exp, max_exp) VALUES (?, ?, ?, ?)", (user_id, 1, 0, 100))

    # Commit the transaction and close the connection
    await db.commit()
    await db.close()

async def get_user_data(user_id: int):
    # Connect to the database
    db = await aiosqlite3.connect('mydatabase.db')

    # Create a cursor
    c = await db.cursor()

    # Select the user's data from the 'levels' table
    await c.execute("SELECT * FROM levels WHERE user_id=?", (user_id,))
    result = await c.fetchone()

    # If the user was found in the database, return their data as a dictionary
    if result:
        data = {
            'user_id': result[0],
            'level': result[1],
            'current_exp': result[2],
            'max_exp': result[3]
        }
        return data
    # If the user was not found in the database, return None
    else:
        return None

async def create_database_and_table():
    # Connect to the database
    db = await aiosqlite3.connect('mydatabase.db')

    # Create a cursor
    c = await db.cursor()

    # Create the 'levels' table
    await c.execute('''CREATE TABLE IF NOT EXISTS levels (
        user_id INTEGER PRIMARY KEY,
        level INTEGER,
        current_exp INTEGER,
        max_exp INTEGER
    )''')

    # Commit the transaction and close the connection
    await db.commit()
    await db.close()

async def update_user_data(user_id: int, level: int, current_exp: int, max_exp: int):
    # Connect to the database
    db = await aiosqlite3.connect('mydatabase.db')

    # Create a cursor
    c = await db.cursor()

    # Check if the user is in the database
    await c.execute("SELECT * FROM levels WHERE user_id=?", (user_id,))
    result = await c.fetchone()

    # If the user is in the database, update their data
    if result:
        await c.execute("UPDATE levels SET level=?, current_exp=?, max_exp=? WHERE user_id=?", (level, current_exp, max_exp, user_id))
    # If the user is not in the database, insert a new row with their data
    else:
        await c.execute("INSERT INTO levels (user_id, level, current_exp, max_exp) VALUES (?, ?, ?, ?)", (user_id, level, current_exp, max_exp))

    # Commit the transaction and close the connection
    await db.commit()
    await db.close()

class Levelling(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log("cogs.levelling is now ready!")
        await self.bot.tree.sync(
            guild=discord.Object(id=int(os.getenv("MAIN_GUILD")))
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.guild is None:
            return
        await add_user(message.author.id)
        data = await get_user_data(message.author.id)
        data['current_exp'] += 10
        if data['current_exp'] >= data['max_exp']:
            data['current_exp'] = 0
            data['level'] += 1
            data['max_exp'] += 100
            await update_user_data(message.author.id, data['level'], data['current_exp'], data['max_exp'])
            await message.channel.send(f"{message.author.mention} has leveled up to level {data['level']}!")
            if data['level'] == 5:
                role = discord.utils.get(message.guild.roles, name="Level 5")
                await message.author.add_roles(role)
            elif data['level'] == 10:
                role = discord.utils.get(message.guild.roles, name="Level 10")
                await message.author.add_roles(role)
            elif data['level'] == 20:
                role = discord.utils.get(message.guild.roles, name="Level 20")
                await message.author.add_roles(role)
            elif data['level'] == 40:
                role = discord.utils.get(message.guild.roles, name="Level 40")
                await message.author.add_roles(role)
            elif data['level'] == 60:
                role = discord.utils.get(message.guild.roles, name="Level 60")
                await message.author.add_roles(role)
            elif data['level'] == 80:
                role = discord.utils.get(message.guild.roles, name="Level 80")
                await message.author.add_roles(role)
            elif data['level'] == 100:
                role = discord.utils.get(message.guild.roles, name="Level 100")
                await message.author.add_roles(role)
        else:
            await update_user_data(message.author.id, data['level'], data['current_exp'], data['max_exp'])

    @discord.app_commands.command(
        name="level",
        description="Shows your level server."
    )
    @discord.app_commands.guilds(int(os.getenv("MAIN_GUILD")))
    async def _rank(self, interaction: discord.Interaction, member: discord.Member = None):
        await interaction.response.defer()
        if member is None:
            member = interaction.user
        if member.banner is not None:
            banner = member.banner.url
        else:
            banner = member.avatar.url
        
        await add_user(member.id)
        data = await get_user_data(member.id)

        rank = await get_user_rank(member.id)

        card_settings = Settings(
            background=banner,
            text_color="white",
            bar_color="#FFFFFF"
        )

        card = RankCard(
            settings=card_settings,
            avatar=member.avatar.url,
            level=data['level'],
            current_exp=data['current_exp'],
            max_exp=data['max_exp'],
            username=str(member),
            rank=rank
        )
        image = await card.card1()
        file = discord.File(image, filename="level.png")
        await interaction.edit_original_response(attachments=[file])


async def setup(bot: commands.Bot):
    await create_database_and_table()
    await bot.add_cog(Levelling(bot))