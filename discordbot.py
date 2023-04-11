from cmath import log
from distutils.sysconfig import PREFIX
import discord
from dotenv import load_dotenv
import os
load_dotenv()
import random
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

PREFIX = os.environ['PREFIX']
TOKEN = os.environ['TOKEN']
client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == f'{PREFIX}call':
        await message.channel.send("callback!")

    if message.content.startswith(f'{PREFIX}hello'):
        await message.channel.send('Hello!')
        
@bot.command(name='roll_dice')
async def roll_dice(ctx):
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    dice_sum = dice1 + dice2
    await ctx.send(f"You rolled {dice1} and {dice2}. The total is {dice_sum}!")
    

try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
