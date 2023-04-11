import discord
from discord.ext import commands
import re
import random

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}.')

@bot.command(name='sum')
async def sum_numbers(ctx):
    # Find all numbers in the message and sum them
    message = ctx.message.content
    numbers = re.findall(r'\d+', message)
    sum_of_numbers = sum(map(int, numbers))
    await ctx.send(f'The sum of the numbers in your message is {sum_of_numbers}!')

@bot.command(name='roll')
async def roll_dice(ctx):
    # Roll 2d6 dice
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
    bot.run(MTA5MjI3Mzc1NTQzNjM2MzgxNw.GGNE7q.QKuw00yBfQSi-MHpyAgKD6oiBSwClm_nXIPIEo)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
    print(e)
