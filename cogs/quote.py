import discord
from discord.ext import commands

class Quote(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Quote cog is ready.')
    
    @commands.command()
    async def quote(self, ctx, messageid: int):
        # Fetch the message from the specified message ID
        try:
            message = await ctx.fetch_message(messageid)
        except discord.NotFound:
            return await ctx.send("Message not found. Make sure you provide a valid message ID.")
        
        if message.author == self.client.user:
            return await ctx.send("You can't quote me!")
        else:
            # Check if the quotes channel already exists
            quotes_channel = discord.utils.get(ctx.guild.channels, name="quotes")

            # If the channel doesn't exist, create a new one
            if not quotes_channel:
                overwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=True),
                    ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
                }
                quotes_channel = await ctx.guild.create_text_channel(name="quotes", overwrites=overwrites)

            # Send the quote message to the quotes channel
            await quotes_channel.send(f'"{message.content}" - {message.author.mention} submitted by {ctx.author.mention}')


async def setup(client):
    await client.add_cog(Quote(client))