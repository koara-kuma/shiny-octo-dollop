import discord
from discord.ext import commands

class Hello(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Hello cog is ready.')
    
    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f'Hello, {ctx.author.mention}!')

async def setup(client):
    await client.add_cog(Hello(client))

