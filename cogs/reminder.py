import discord
from discord.ext import commands
import asyncio
import re

class Reminder(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Reminder cog is ready.')

    @commands.command()
    async def remind(self, ctx, time_str, *, reminder):
        user = ctx.message.author

        time_seconds = self.convert_time_to_seconds(time_str)
        if time_seconds is None:
            await ctx.send("Invalid time format. Please use a valid time format (e.g., '1d', '2h', '30m').")
            return

        embed = discord.Embed(color=discord.Color.orange())
        embed.add_field(name='Reminder set!', value=f'I will remind you about {reminder} in {time_str}.')
        await ctx.send(embed=embed)

        await asyncio.sleep(time_seconds)

        embed = discord.Embed(color=discord.Color.orange())
        embed.add_field(name=f'Hi {user.name}', value=f'{ctx.author.mention} You asked me to remind you about {reminder} {time_str} ago.')
        await ctx.send(embed=embed)

    def convert_time_to_seconds(self, time_str):
        time_formats = {
            r"(\d+)d": 86400,  # Days to seconds
            r"(\d+)h": 3600,   # Hours to seconds
            r"(\d+)m": 60,     # Minutes to seconds
            r"(\d+)s": 1,      # Seconds
        }

        total_seconds = 0
        for pattern, seconds_per_unit in time_formats.items():
            match = re.match(pattern, time_str)
            if match:
                total_seconds += int(match.group(1)) * seconds_per_unit

        return total_seconds

async def setup(client):
    await client.add_cog(Reminder(client))
