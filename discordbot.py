import discord
from discord.ext import commands
import os
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Set command prefix and bot token from environment variables
PREFIX = os.getenv('PREFIX')
TOKEN = os.getenv('TOKEN')

# Set up Google Sheets API credentials
creds = ServiceAccountCredentials.from_json_keyfile_name('daylighttmr-bcd50a44ed0c.json', ['https://www.googleapis.com/auth/spreadsheets'])

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
@bot.command(name='roll')
async def roll(ctx):
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

# Get data from Google Spreadsheet
@bot.command(name='get-data')
async def get_data(ctx):
    try:
        # Authenticate with Google Sheets API
        gc = gspread.authorize(creds)

        # Open the Google Spreadsheet by ID
        sheet_id = '17hI1pPPxGqAtPJuJzT9eP8ZbJeNE9eOmsFbLjk5Fo58'
        worksheet = gc.open_by_key(sheet_id).sheet1

        # Get all data from the first worksheet
        data = worksheet.get_all_values()

        # Send the data as a Discord message
        await ctx.send('Data from the Google Spreadsheet:')
        for row in data:
            await ctx.send(row)

    except Exception as e:
        print(f'Error: {e}')
        await ctx.send(f'Error: {e}')

# Run the bot
bot.run(TOKEN)
