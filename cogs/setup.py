import datetime
import json
import os
import discord
from discord.ext import commands

class Verify(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.green, custom_id="Verify:Verify")
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You have been verified!", ephemeral=True)
        await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, name="Members"))

async def transcript(channel: discord.TextChannel):
    with open("tickets.json", mode="r") as f:
        data = json.load(f)

    msgs = [message async for message in channel.history(limit=None, oldest_first=True)]

    messages = []

    for message in msgs:
        messages.append(
            f"{datetime.datetime.now()} - {message.author}: {message.content}"
        )

    user = msgs[0].content.replace("<@", "").replace("!", "").replace(">", "")

    channel_data = data[channel.name] = {
        "opened": str(msgs[0].created_at),
        "closed": str(datetime.datetime.now()),
        "author": user,
        "messages": messages
    }

    with open("tickets.json", mode="w") as f:
        json.dump(data, f, indent=4)

    return

class CloseButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Close",
        custom_id="CloseButton:CloseButton",
        style=discord.ButtonStyle.green,
        emoji="🔒"
    )
    async def closeButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("This ticket will closed in 5 seconds...")
        await transcript(interaction.channel)
        await interaction.channel.delete(reason=f"Ticket closed by {interaction.user}")

class CreateTicketButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Create Ticket",
        custom_id="CreateTicketButton:CreateTicketButton",
        style=discord.ButtonStyle.green,
        emoji="🎟️"
    )
    async def createTicketButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open("tickets.json", mode="r") as f:
            data = json.load(f)
        data['id'] += 1
        helper = discord.utils.get(interaction.guild.roles, name="Helpers")
        moderators = discord.utils.get(interaction.guild.roles, name="Moderators")
        head_moderator = discord.utils.get(interaction.guild.roles, name="Head Moderator")
        administrators = discord.utils.get(interaction.guild.roles, name="Administrators")

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            helper: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            moderators: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            head_moderator: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            administrators: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
        }

        await interaction.response.defer(ephemeral=True)
        channel = await interaction.guild.create_text_channel(
            name=f"ticket-{data['id']}",
            reason=f"Ticket for {interaction.user}",
            topic=f"Ticket channel created for {interaction.user}",
            overwrites=overwrites
        )
        
        embed = discord.Embed(
            title=f"Ticket {data['id']}",
            description=f"This is a ticket channel created for {interaction.user.mention}",
            color=discord.Color.green()
        )
        await channel.send(content=interaction.user.mention, embed=embed, view=CloseButton())


class reactionRolesView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Red",
        custom_id="reactionRolesView:red",
        style=discord.ButtonStyle.green,
        emoji="🔴"
    )
    async def reactionRolesViewRed(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        role = discord.utils.get(interaction.guild.roles, name="Red")
        if not role:
            await interaction.edit_message(content=":x: This server does not have a role named `Red`.")
            return
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.edit_message(content=":white_check_mark: Successfully removed the `Red` role from you.")
            return
        await interaction.user.add_roles(role)
        await interaction.edit_message(content=":white_check_mark: Successfully gave you the `Red` role.")

    @discord.ui.button(
        label="Blue",
        custom_id="reactionRolesView:blue",
        style=discord.ButtonStyle.green,
        emoji="🔵"
    )
    async def reactionRolesViewBlue(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        role = discord.utils.get(interaction.guild.roles, name="Blue")
        if not role:
            await interaction.edit_message(content=":x: This server does not have a role named `Blue`.")
            return
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.edit_message(content=":white_check_mark: Successfully removed the `Blue` role from you.")
            return
        await interaction.user.add_roles(role)
        await interaction.edit_message(content=":white_check_mark: Successfully gave you the `Blue` role.")

    @discord.ui.button(
        label="Green",
        custom_id="reactionRolesView:green",
        style=discord.ButtonStyle.green,
        emoji="🟢"
    )
    async def reactionRolesViewGreen(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        role = discord.utils.get(interaction.guild.roles, name="Green")
        if not role:
            await interaction.edit_message(content=":x: This server does not have a role named `Green`.")
            return
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.edit_message(content=":white_check_mark: Successfully removed the `Green` role from you.")
            return
        await interaction.user.add_roles(role)
        await interaction.edit_message(content=":white_check_mark: Successfully gave you the `Green` role.")

    @discord.ui.button(
        label="Yellow",
        custom_id="reactionRolesView:yellow",
        style=discord.ButtonStyle.green,
        emoji="🟡"
    )
    async def reactionRolesViewYellow(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        role = discord.utils.get(interaction.guild.roles, name="Yellow")
        if not role:
            await interaction.edit_message(content=":x: This server does not have a role named `Yellow`.")
            return
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.edit_message(content=":white_check_mark: Successfully removed the `Yellow` role from you.")
            return
        await interaction.user.add_roles(role)
        await interaction.edit_message(content=":white_check_mark: Successfully gave you the `Yellow` role.")

    @discord.ui.button(
        label="Purple",
        custom_id="reactionRolesView:purple",
        style=discord.ButtonStyle.green,
        emoji="🟣"
    )
    async def reactionRolesViewPurple(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        role = discord.utils.get(interaction.guild.roles, name="Purple")
        if not role:
            await interaction.edit_message(content=":x: This server does not have a role named `Purple`.")
            return
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.edit_message(content=":white_check_mark: Successfully removed the `Purple` role from you.")
            return
        await interaction.user.add_roles(role)
        await interaction.edit_message(content=":white_check_mark: Successfully gave you the `Purple` role.")

    @discord.ui.button(
        label="Black",
        custom_id="reactionRolesView:black",
        style=discord.ButtonStyle.green,
        emoji="⚫"
    )
    async def reactionRolesViewBlack(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        role = discord.utils.get(interaction.guild.roles, name="Black")
        if not role:
            await interaction.edit_message(content=":x: This server does not have a role named `Black`.")
            return
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.edit_message(content=":white_check_mark: Successfully removed the `Black` role from you.")
            return
        await interaction.user.add_roles(role)
        await interaction.edit_message(content=":white_check_mark: Successfully gave you the `Black` role.")

    @discord.ui.button(
        label="White",
        custom_id="reactionRolesView:white",
        style=discord.ButtonStyle.green,
        emoji="⚪"
    )
    async def reactionRolesViewWhite(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        role = discord.utils.get(interaction.guild.roles, name="White")
        if not role:
            await interaction.edit_message(content=":x: This server does not have a role named `White`.")
            return
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.edit_message(content=":white_check_mark: Successfully removed the `White` role from you.")
            return
        await interaction.user.add_roles(role)
        await interaction.edit_message(content=":white_check_mark: Successfully gave you the `White` role.")

    

def is_owner(interaction: discord.Interaction):
    return interaction.user == interaction.guild.owner

class Setup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        
        self.main_guild: int = self.bot.main_guild

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log("cogs.setup is now ready")
        self.bot.add_view(CloseButton())
        self.bot.add_view(reactionRolesView())
        self.bot.add_view(CreateTicketButton())
        self.bot.add_view(Verify())
        await self.bot.tree.sync(
            guild=discord.Object(id=int(os.getenv("MAIN_GUILD")))
        )

    @discord.app_commands.command(
        name="setup",
        description="Sets up the server."
    )
    @discord.app_commands.guilds(int(os.getenv("MAIN_GUILD")))
    @discord.app_commands.check(is_owner)
    async def setup_command(
        self,
        interaction: discord.Interaction
    ):
        await interaction.response.defer()
        for channel in interaction.guild.channels:
            await channel.delete()
        for role in interaction.guild.roles:
            if role.name == "@everyone" or role.name == "k ?": continue
            await role.delete()
        for emoji in interaction.guild.emojis:
            await emoji.delete(reason="Setting up the server.")

        for img in os.listdir("./assets/emojis"):
            with open(f"./assets/emojis/{img[:-4]}", "rb") as image: 
                f = image.read()
            byte = bytearray(f) 
            await interaction.guild.create_custom_emoji(
                name=img[:-4],
                image=byte
            )

        owner = await interaction.guild.create_role(
            reason="Setting up the server.",
            name="Owner",
            permissions=discord.Permissions().all(),
            hoist=True,
            mentionable=False
        )

        head_administrator = await interaction.guild.create_role(
            reason="Setting up the server.",
            name="Head Administrator",
            permissions=discord.Permissions().all(),
            hoist=True,
            mentionable=False
        )

        all_without_admin = discord.Permissions().all()
        all_without_admin.administrator = False

        administrators = await interaction.guild.create_role(
            reason="Setting up the server.",
            name="Administrators",
            permissions=all_without_admin,
            hoist=True,
            mentionable=False
        )

        moderator_permissions = discord.Permissions(
            send_messages=True,
            view_channel=True,
            add_reactions=True,
            attach_files=True,
            change_nickname=True,
            connect=True,
            create_instant_invite=True,
            deafen_members=True,
            embed_links=True,
            use_external_emojis=True,
            use_external_stickers=True,
            manage_nicknames=True,
            manage_messages=True,
            moderate_members=True,
            move_members=True,
            mute_members=True,
            read_message_history=True,
            read_messages=True,
            speak=True,
            stream=True,
            use_application_commands=True,
            use_embedded_activities=True,
            view_audit_log=True,
            create_private_threads=False,
            create_public_threads=False
        )

        head_moderator = await interaction.guild.create_role(
            reason="Setting up the server.",
            name="Head Moderator",
            permissions=moderator_permissions,
            hoist=True,
            mentionable=False
        )

        muted_permissions = discord.Permissions(
            send_messages=False,
            view_channel=True,
            add_reactions=False,
            attach_files=False,
            change_nickname=True,
            connect=False,
            create_instant_invite=True,
            deafen_members=False,
            embed_links=False,
            use_external_emojis=False,
            use_external_stickers=False,
            read_message_history=True,
            read_messages=True,
            speak=False,
            stream=False,
            use_application_commands=False,
            create_private_threads=False,
            create_public_threads=False
        )

        muted = await interaction.guild.create_role(
            reason="Setting up the server.",
            name="Muted",
            permissions=muted_permissions,
            hoist=False,
            mentionable=False
        )

        moderators = await interaction.guild.create_role(
            reason="Setting up the server.",
            name="Moderators",
            permissions=moderator_permissions,
            hoist=True,
            mentionable=False
        )

        helper_permissions = discord.Permissions(
            send_messages=True,
            view_channel=True,
            add_reactions=True,
            attach_files=True,
            change_nickname=True,
            connect=True,
            create_instant_invite=True,
            embed_links=True,
            use_external_emojis=True,
            use_external_stickers=True,
            manage_nicknames=True,
            manage_messages=True,
            moderate_members=True,
            mute_members=True,
            read_message_history=True,
            read_messages=True,
            speak=True,
            stream=True,
            use_application_commands=True,
            use_embedded_activities=True,
            create_private_threads=False,
            create_public_threads=False
        )

        helpers = await interaction.guild.create_role(
            reason="Setting up the server.",
            name="Helpers",
            permissions=helper_permissions,
            hoist=True,
            mentionable=False
        )

        trial_helper = await interaction.guild.create_role(
            reason="Setting up the server.",
            name="Trial Helper",
            permissions=helper_permissions,
            hoist=True,
            mentionable=False
        )

        member_permissions = discord.Permissions(
            send_messages=True,
            view_channel=True,
            add_reactions=True,
            attach_files=True,
            change_nickname=True,
            connect=True,
            create_instant_invite=True,
            embed_links=True,
            use_external_emojis=True,
            use_external_stickers=True,
            read_message_history=True,
            read_messages=True,
            speak=True,
            stream=True,
            use_application_commands=True,
            use_embedded_activities=True,
            create_private_threads=False,
            create_public_threads=False
        )

        members = await interaction.guild.create_role(
            reason="Setting up the server.",
            name="Members",
            permissions=member_permissions,
            hoist=True,
            mentionable=False
        )

        level_100 = await interaction.guild.create_role(
            reason="Setting up the server.",
            name="Level 100",
            permissions=discord.Permissions.none(),
            hoist=True,
            mentionable=False
        )

        level_80 = await interaction.guild.create_role(
            reason="Setting up the server.",
            name="Level 80",
            permissions=discord.Permissions.none(),
            hoist=True,
            mentionable=False
        )

        level_60 = await interaction.guild.create_role(
            reason="Setting up the server.",
            name="Level 60",
            permissions=discord.Permissions.none(),
            hoist=True,
            mentionable=False
        )

        level_40 = await interaction.guild.create_role(
            reason="Setting up the server.",
            name="Level 40",
            permissions=discord.Permissions.none(),
            hoist=True,
            mentionable=False
        )

        level_20 = await interaction.guild.create_role(
            reason="Setting up the server.",
            name="Level 20",
            permissions=discord.Permissions.none(),
            hoist=True,
            mentionable=False
        )

        level_10 = await interaction.guild.create_role(
            reason="Setting up the server.",
            name="Level 10",
            permissions=discord.Permissions.none(),
            hoist=True,
            mentionable=False
        )

        level_5 = await interaction.guild.create_role(
            reason="Setting up the server.",
            name="Level 5",
            permissions=discord.Permissions.none(),
            hoist=True,
            mentionable=False
        )

        red = await interaction.guild.create_role(
            reason="Setting up the server.",
            name="Red",
            permissions=discord.Permissions.none(),
            hoist=False,
            mentionable=False,
            color=discord.Color.red()
        )

        blue = await interaction.guild.create_role(
            reason="Setting up the server.",
            name="Blue",
            permissions=discord.Permissions.none(),
            hoist=False,
            mentionable=False,
            color=discord.Color.blue()
        )

        green = await interaction.guild.create_role(
            reason="Setting up the server.",
            name="Green",
            permissions=discord.Permissions.none(),
            hoist=False,
            mentionable=False,
            color=discord.Color.green()
        )

        yellow = await interaction.guild.create_role(
            reason="Setting up the server.",
            name="Yellow",
            permissions=discord.Permissions.none(),
            hoist=False,
            mentionable=False,
            color=discord.Color.yellow()
        )

        purple = await interaction.guild.create_role(
            reason="Setting up the server.",
            name="Purple",
            permissions=discord.Permissions.none(),
            hoist=False,
            mentionable=False,
            color=discord.Color.purple()
        )

        black = await interaction.guild.create_role(
            reason="Setting up the server.",
            name="Black",
            permissions=discord.Permissions.none(),
            hoist=False,
            mentionable=False,
            color=0x000001
        )

        white = await interaction.guild.create_role(
            reason="Setting up the server.",
            name="White",
            permissions=discord.Permissions.none(),
            hoist=False,
            mentionable=False,
            color=0xFFFFFF
        )

        information_category_overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(
                send_messages=False,
                view_channel=False,
                create_private_threads=False,
                create_public_threads=False
            ),
            members: discord.PermissionOverwrite(
                send_messages=False,
                view_channel=True,
                create_private_threads=False,
                create_public_threads=False
            ),
            helpers: discord.PermissionOverwrite(
                send_messages=False,
                view_channel=True,
                create_private_threads=False,
                create_public_threads=False
            ),
            trial_helper: discord.PermissionOverwrite(
                send_messages=False,
                view_channel=True,
                create_private_threads=False,
                create_public_threads=False
            ),
            moderators: discord.PermissionOverwrite(
                send_messages=False,
                view_channel=True,
                create_private_threads=False,
                create_public_threads=False
            ),
            head_moderator: discord.PermissionOverwrite(
                send_messages=False,
                view_channel=True,
                create_private_threads=False,
                create_public_threads=False
            )
        }

        server_category = await interaction.guild.create_category(
            name="SERVER",
            overwrites=information_category_overwrites,
            reason="Setting up the server."
        )

        rules_channel = await server_category.create_text_channel(
            name="📜┆rules"
        )

        announcements_channel = await server_category.create_text_channel(
            name="📢┆announcements"
        )

        server_info = await server_category.create_text_channel(
            name="❓┆server-info"
        )

        reaction_roles = await server_category.create_text_channel(
            name="📎┆reaction-roles"
        )

        tickets = await server_category.create_text_channel(
            name="🎫┆tickets"
        )
    
        general_category_overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(
                send_messages=False,
                view_channel=False,
                create_private_threads=False,
                create_public_threads=False
            ),
            members: discord.PermissionOverwrite(
                send_messages=True,
                view_channel=True,
                create_private_threads=False,
                create_public_threads=False
            ),
            helpers: discord.PermissionOverwrite(
                send_messages=True,
                view_channel=True,
                create_private_threads=False,
                create_public_threads=False
            ),
            trial_helper: discord.PermissionOverwrite(
                send_messages=True,
                view_channel=True,
                create_private_threads=False,
                create_public_threads=False
            ),
            moderators: discord.PermissionOverwrite(
                send_messages=True,
                view_channel=True,
                create_private_threads=False,
                create_public_threads=False
            ),
            head_moderator: discord.PermissionOverwrite(
                send_messages=True,
                view_channel=True,
                create_private_threads=False,
                create_public_threads=False
            )
        }

        general_category = await interaction.guild.create_category(
            name="GENERAL",
            reason="Setting up the server.",
            overwrites=general_category_overwrites
        )

        #make a chat channel
        chat_channel = await general_category.create_text_channel(
            name="🗣┆chat",
        )
        
        media_channel = await general_category.create_text_channel(
            name="📷┆media"
        )
        
        bot_commands_channel = await general_category.create_text_channel(
            name="🤖┆bot-commands"
        )
        
        looking_for_party = await general_category.create_text_channel(
            name="🎮┆looking-for-party"
        )

        gaming_discussion = await general_category.create_text_channel(
            name="🎮┆gaming-discussion"
        )

        memes_channel = await general_category.create_text_channel(
            name="🤣┆memes"
        )

        voice_category_overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(
                connect=False,
                view_channel=False,
                create_private_threads=False,
                create_public_threads=False
            ),
            members: discord.PermissionOverwrite(
                connect=True,
                view_channel=True,
                create_private_threads=False,
                create_public_threads=False
            ),
            helpers: discord.PermissionOverwrite(
                connect=True,
                view_channel=True,
                create_private_threads=False,
                create_public_threads=False
            ),
            trial_helper: discord.PermissionOverwrite(
                connect=True,
                view_channel=True,
                create_private_threads=False,
                create_public_threads=False
            ),
            moderators: discord.PermissionOverwrite(
                connect=True,
                view_channel=True,
                create_private_threads=False,
                create_public_threads=False
            ),
            head_moderator: discord.PermissionOverwrite(
                connect=True,
                view_channel=True,
                create_private_threads=False,
                create_public_threads=False
            )
        }

        voice_category = await interaction.guild.create_category(
            name="VOICE",
            reason="Setting up the server.",
            overwrites=voice_category_overwrites
        )

        vc_1 = await voice_category.create_voice_channel(
            name="🎤┆voice-chat-1"
        )
        vc_2 = await voice_category.create_voice_channel(
            name="🎤┆voice-chat-2"
        )
        vc_3 = await voice_category.create_voice_channel(
            name="🎤┆voice-chat-3"
        )

        gaming_vc_1 = await voice_category.create_voice_channel(
            name="🎮┆gaming-voice-chat-1"
        )

        gaming_vc_2 = await voice_category.create_voice_channel(
            name="🎮┆gaming-voice-chat-2"
        )

        gaming_vc_3 = await voice_category.create_voice_channel(
            name="🎮┆gaming-voice-chat-3"
        )

        music_vc = await voice_category.create_voice_channel(
            name="🎵┆music-voice-chat"
        )

        #make a staff category

        staff_category_overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(
                send_messages=False,
                view_channel=False,
                create_private_threads=False,
                create_public_threads=False
            ),
            members: discord.PermissionOverwrite(
                send_messages=False,
                view_channel=False,
                create_private_threads=False,
                create_public_threads=False
            ),
            helpers: discord.PermissionOverwrite(
                send_messages=True,
                view_channel=True,
                create_private_threads=False,
                create_public_threads=False
            ),
            trial_helper: discord.PermissionOverwrite(
                send_messages=True,
                view_channel=True,
                create_private_threads=False,
                create_public_threads=False
            ),
            moderators: discord.PermissionOverwrite(
                send_messages=True,
                view_channel=True,
                create_private_threads=False,
                create_public_threads=False
            ),
            head_moderator: discord.PermissionOverwrite(
                send_messages=True,
                view_channel=True,
                create_private_threads=False,
                create_public_threads=False
            )
        }

        staff_category = await interaction.guild.create_category(
            name="STAFF",
            reason="Setting up the server.",
            overwrites=staff_category_overwrites
        )

        #make a staff rules channel
        staff_rules_channel = await staff_category.create_text_channel(
            name="📜┆staff-rules",
        )

        #make a staff chat channel
        staff_chat_channel = await staff_category.create_text_channel(
            name="🗣┆staff-chat",
        )

        #make a staff logs channel
        staff_logs_channel = await staff_category.create_text_channel(
            name="📜┆staff-logs",
        )

        #make a staff vc channel
        staff_vc_channel = await staff_category.create_voice_channel(
            name="🎤┆staff-vc",
        )
        
        verify_channel_overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(
                send_messages=False,
                view_channel=True,
                create_private_threads=False,
                create_public_threads=False
            ),
            members: discord.PermissionOverwrite(
                send_messages=False,
                view_channel=False,
                create_private_threads=False,
                create_public_threads=False
            ),
            helpers: discord.PermissionOverwrite(
                send_messages=False,
                view_channel=False,
                create_private_threads=False,
                create_public_threads=False
            ),
            trial_helper: discord.PermissionOverwrite(
                send_messages=False,
                view_channel=False,
                create_private_threads=False,
                create_public_threads=False
            ),
            moderators: discord.PermissionOverwrite(
                send_messages=False,
                view_channel=False,
                create_private_threads=False,
                create_public_threads=False
            ),
            head_moderator: discord.PermissionOverwrite(
                send_messages=False,
                view_channel=False,
                create_private_threads=False,
                create_public_threads=False
            )
        }
        
        verify_channel = await interaction.guild.create_text_channel(
            name="📜┆verify",
            overwrites=verify_channel_overwrites
        )

        over = {muted: discord.PermissionOverwrite(
            send_messages=False,
            view_channel=True,
            add_reactions=False,
            attach_files=False,
            change_nickname=True,
            connect=False,
            create_instant_invite=True,
            deafen_members=False,
            embed_links=False,
            use_external_emojis=False,
            use_external_stickers=False,
            read_message_history=True,
            read_messages=True,
            speak=False,
            stream=False,
            use_application_commands=False,
            create_private_threads=False,
            create_public_threads=False
            )
        }

        for channel in interaction.guild.text_channels:
            await channel.edit(
                overwrites=channel.overwrites | over
            )

        with open('embeds.json', mode='r') as f:
            data = json.load(f)
        channel = None
        for dictionary in data:
            for channell in interaction.guild.channels:
                if channell.name[2:] == dictionary:
                    channel = channell
            if channel:
                if channel == verify_channel:
                    view = Verify()
                    embed = discord.Embed.from_dict(data[dictionary])
                    await channel.send(embed=embed, view=view)
                elif channel == reaction_roles:
                    view = reactionRolesView()
                    embed = discord.Embed.from_dict(data[dictionary])
                    await channel.send(embed=embed, view=view)
                elif channel == tickets:
                    view = CreateTicketButton()
                    embed = discord.Embed.from_dict(data[dictionary])
                    await channel.send(embed=embed, view=view)
                else:
                    embed = discord.Embed.from_dict(data[dictionary])
                    await channel.send(embed=embed)
            else:
                print(f"Channel {dictionary} not found.")

        await chat_channel.send(":white_check_mark: Server Setup complete!")

async def setup(bot: commands.Bot):
    await bot.add_cog(Setup(bot))