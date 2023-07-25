import discord
from discord.ext import commands
import asyncio

class Snipe(commands.Cog):
    def __init__(self, client):
        self.client = client

    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Snipe cog is ready.')
    




async def setup(client):
    await client.add_cog(Snipe(client))