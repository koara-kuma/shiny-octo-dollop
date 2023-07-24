import discord
from discord.ext import commands
import random
import json
import os
import asyncio

if os.path.exists(os.getcwd() +"/config.json"):
    with open("./config.json") as f:
        configData = json.load(f)

else:
    configTemplate = {'Token': ""}
    
    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)

help_command = commands.DefaultHelpCommand(
    no_category = "Kasumi's commands"
)

client = commands.Bot(command_prefix = '!', help_command = help_command, intents= discord.Intents.all())

async def on_ready():
    print(f"We have logged in as {client.user}")

async def load():
    for filename in os.listdir("shiny-octo-dollop/cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded {filename}")

token = configData['Token']

async def main():
    async with client:
        await load()
        await client.start(token)

asyncio.run(main())






