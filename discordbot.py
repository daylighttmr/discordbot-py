import discord
from discord.ext import commands
import os
import random
import gspread
from google.oauth2.service_account import ServiceAccountCredentials

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Set command prefix and bot token from environment variables
PREFIX = os.getenv('PREFIX')
TOKEN = os.getenv('TOKEN')

# Set up Google Sheets API credentials
scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
creds = ServiceAccountCredentials.from_json_keyfile_name('daylighttmr-bcd50a44ed0c.json', scopes)
client = gspread.authorize(creds)

sheet_id = '17hI1pPPxGqAtPJuJzT9eP8ZbJeNE9eOmsFbLjk5Fo58'
sheet = client.open_by_key(sheet_id).sheet1

# Write to a cell in the Google Sheet
sheet.update_cell(1, 1, 'Hello, world!')

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

# Random paragraph
paragraphs = [
    "This is the first paragraph.",
    "Here is another paragraph.",
    "This is the third paragraph.",
    "Yet another paragraph.",
    "And finally, a fifth paragraph."
]

@bot.command(name='go')
async def random_paragraph(ctx):
    random_p = random.choice(paragraphs)
    embed = discord.Embed(title="Random Paragraph", description=random_p)
    await ctx.send(embed=embed)

# Run the bot
bot.run(TOKEN)
