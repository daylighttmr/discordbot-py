import discord
from discord.ext import commands
import os
import random

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Set command prefix and bot token from environment variables
PREFIX = os.getenv('PREFIX')
TOKEN = os.getenv('TOKEN')

# Create bot instance
bot = commands.Bot(command_prefix=PREFIX)

# Print bot information when ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}.')

# Respond to messages
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == f'{PREFIX}call':
        await message.channel.send("callback!")

    if message.content.startswith(f'{PREFIX}hello'):
        await message.channel.send('Hello!')

    await bot.process_commands(message)

# Roll 2d6 dice
@bot.command(name='rolldice')
async def rolldice(ctx):
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    dice_sum = dice1 + dice2
    await ctx.send(f"You rolled {dice1} and {dice2}. The total is {dice_sum}!")
    
    paragraphs = [
    "This is the first paragraph.",
    "Here is another paragraph.",
    "This is the third paragraph.",
    "Yet another paragraph.",
    "And finally, a fifth paragraph."
]

# Create a Discord client
client = discord.Client()

# Event listener for when the bot is ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user}.')

# Event listener for when a message is received
@client.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return

    # Check if the message starts with the command prefix and the command is "go"
    if message.content.startswith('!go'):
        # Choose a random paragraph from the list
        random_paragraph = random.choice(paragraphs)
        
        # Create an embed with the paragraph as the description and "Random Paragraph" as the title
        embed = discord.Embed(title="Random Paragraph", description=random_paragraph)
        
        # Send the embed to the same channel where the message was received
        await message.channel.send(embed=embed)

# Run the bot
bot.run(TOKEN)
