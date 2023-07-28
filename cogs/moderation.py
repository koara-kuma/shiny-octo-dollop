import discord
from discord.ext import commands
import asyncio

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.snipe_message_content = None
        self.snipe_message_author = None
        self.snipe_message_attachments = None
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Moderation cog is ready.')
    
    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def nuke(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            await ctx.send("You need to type the channel's name after the command.")
            return

        nuke_channel = discord.utils.get(ctx.guild.channels, name=channel.name)

        if nuke_channel is not None:
            channel_position = nuke_channel.position
            await ctx.send("A tactical nuke is dropping in 10 seconds! Evacuate to the nearest bunker :radioactive:")
            await asyncio.sleep(10)
            new_channel = await nuke_channel.clone(reason="Has been Nuked!")
            await nuke_channel.delete()
            await new_channel.edit(position=channel_position, sync_permissions=True)
            await new_channel.send(f"{ctx.message.author.name} has decided to drop a tactical nuke on this chat, cleaning it of all its messages.")

        else:
            await ctx.send(f"No channel named {channel.name} was found!")

async def setup(client):
    await client.add_cog(Moderation(client))