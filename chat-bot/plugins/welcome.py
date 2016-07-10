from plugin import Plugin
import logging
import discord

log = logging.getLogger('discord')


class Welcome(Plugin):

    fancy_name = "Welcome"

    async def on_member_join(self, member):
        server = member.server
        storage = await self.get_storage(server)
        
        # Send server welcome if enabled
        server_welcome_enabled = await storage.get('server_welcome_disabled') is None
        if server_welcome_enabled:
            welcome_message = await storage.get('welcome_message')
            welcome_message = welcome_message.replace(
                "{server}",
                server.name
            ).replace(
                "{user}",
                member.mention
            )
            destination = server
            channel_name = await storage.get('channel_name')
            channel = discord.utils.find(lambda c: c.name == channel_name or
                                         c.id == channel_name,
                                         server.channels)
            if channel is not None:
                destination = channel

            await self.mee6.send_message(destination, welcome_message)
        
        # Send Direct Mssage welcome if enabeld
        dm_welcome_enabled = await storage.get('dm_welcome_enabled') is not None
        if dm_welcome_enabled:
            welcome_message = await storage.get('dm_welcome_message')
            welcome_message = welcome_message.replace(
                "{server}",
                server.name
            ).replace(
                "{user}",
                member.mention
            )
            await self.mee6.send_message(member, welcome_message)

    async def on_member_remove(self, member):
        server = member.server
        storage = await self.get_storage(server)
        gb_message = await storage.get('gb_message')
        gb_enabled = (await storage.get('gb_disabled')) is None
        if not gb_enabled:
            return
        if not gb_message:
            return

        gb_message = gb_message.replace(
            "{server}",
            server.name
        ).replace(
            "{user}",
            member.name
        )
        channel_name = await storage.get('channel_name')

        destination = server
        channel = discord.utils.find(lambda c: c.name == channel_name or
                                     c.id == channel_name,
                                     server.channels)
        if channel is not None:
            destination = channel

        await self.mee6.send_message(destination, gb_message)
