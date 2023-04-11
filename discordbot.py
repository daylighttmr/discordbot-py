import discord
from dotenv import load_dotenv
import os
import random
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}.')

@bot.command(name='roll')
async def roll(ctx):
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    dice_sum = dice1 + dice2
    await ctx.send(f"You rolled {dice1} and {dice2}. The total is {dice_sum}!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == f'{bot.command_prefix}call':
        await message.channel.send("callback!")

    if message.content.startswith(f'{bot.command_prefix}hello'):
        await message.channel.send('Hello!')

try:
    bot.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
    print(e)
