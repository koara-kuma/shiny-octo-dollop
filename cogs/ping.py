import discord
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Ping cog is ready.')
    
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

async def setup(client):
    await client.add_cog(Ping(client))
