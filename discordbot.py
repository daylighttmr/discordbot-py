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

# Create dictionary to store member's worksheet names
member_sheets = {}

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

    
@bot.command(name='1d6')
@bot.command(name='1D6')
async def roll_dice(ctx):
    dice_roll = random.randint(1, 6)
    await ctx.send(f"You rolled a {dice_roll}!")
    
    
@bot.command(name='2D6')
@bot.command(name='2d6')
async def add_dice(ctx, num1: int = 0, num2: int = 0):
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    dice_sum = dice1 + dice2 + num1 + num2
    
    if dice_sum > 8:
        await ctx.send(f"You rolled {dice1} and {dice2}. The total is {dice_sum}! 일반 성공!")
    else:
        await ctx.send(f"You rolled {dice1} and {dice2}. The total is {dice_sum}!")

        
@bot.command(name='yn')
@bot.command(name='YN')
async def yes_or_no(ctx):
    responses = ["Yes", "No", "Maybe", "Definitely", "Never", "Of course", "Absolutely", "Not a chance", "Sure", "Not likely"]
    response = random.choice(responses)
    await ctx.send(response)

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
        await ctx.send(f'An error occurred: {e}')
            
            # Register user's worksheet name
@bot.command(name='register')
async def register_sheet(ctx, sheet_name: str):
    member_sheets[ctx.author.id] = sheet_name
    await ctx.send(f"Registered sheet '{sheet_name}' for user {ctx.author.name}.")

# Retrieve data from registered sheet for user who sent command
@bot.command(name='getdata')
async def get_data(ctx, cell: str):
    member_id = ctx.author.id
    sheet_name = member_sheets.get(member_id)
    if sheet_name is None:
        await ctx.send("You haven't registered a sheet yet!")
        return
    try:
        worksheet = client.open_by_key(sheet_id).worksheet(sheet_name)
        value = worksheet.acell(cell).value
        await ctx.send(f"The value in sheet '{sheet_name}' at cell '{cell}' is '{value}'.")
    except gspread.exceptions.WorksheetNotFound:
        await ctx.send(f"Sheet '{sheet_name}' not found in spreadsheet.")
    except gspread.exceptions.CellNotFound:
        await ctx.send(f"Cell '{cell}' not found in sheet '{sheet_name}'.")

# Run the bot
bot.run(TOKEN)
