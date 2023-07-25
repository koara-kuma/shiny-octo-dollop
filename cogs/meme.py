import discord
from discord.ext import commands
import asyncio
import requests


class Meme(commands.Cog):
    def __init__(self, client):
        self.client = client

    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Meme cog is ready.')

    @commands.command()
    async def meme(self, ctx):
        # Reddit API endpoint for /r/memes
        url = "https://api.reddit.com/r/memes/random"

        try:
            # Make the request to the Reddit API
            response = requests.get(url, headers={"User-agent": "Your Bot Name"})

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Extract the JSON data from the response
                data = response.json()

                # Get the first post from the response (it's a list of posts)
                post = data[0]["data"]["children"][0]["data"]

                # Extract information from the post
                title = post["title"]
                image_url = post["url_overridden_by_dest"]

                # Create an embed to display the meme
                embed = discord.Embed(title=title, color=discord.Color.purple())
                embed.set_image(url=image_url)

                # Send the embed to the channel
                await ctx.send(embed=embed)
            else:
                await ctx.send("Failed to fetch a meme from Reddit.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    




async def setup(client):
    await client.add_cog(Meme(client))