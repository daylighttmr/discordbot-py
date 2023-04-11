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

# Roll 2d6 dice
@bot.command(name='add_dice')
async def add_dice(ctx, num1: int, num2: int):
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    dice_sum = dice1 + dice2 + num1 + num2
    
    if dice_sum > 8:
        await ctx.send(f"You rolled {dice1} and {dice2}. The total is {dice_sum}! 일반 성공!")
    else:
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
        
        
@bot.command(name='체력')
async def 체력(ctx):
    # authenticate and open the spreadsheet
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    creds = ServiceAccountCredentials.from_json_keyfile_name('daylighttmr-bcd50a44ed0c.json', scope)
    client = gspread.authorize(creds)
    sheet_id = '17hI1pPPxGqAtPJuJzT9eP8ZbJeNE9eOmsFbLjk5Fo58'
    worksheet_name = str(ctx.author)

    try:
        worksheet = client.open_by_key(sheet_id).worksheet(worksheet_name)
    except gspread.exceptions.WorksheetNotFound:
        await ctx.send(f'No worksheet found for {worksheet_name}.')
        return

    # get the value of cell F14
    try:
        f14_value = worksheet.acell('F14').value
        await ctx.send(f'The value of F14 in your worksheet is {f14_value}.')
    except gspread.exceptions.CellNotFound:
        await ctx.send('F14 is not found in your worksheet.')
        
    # 워크시트 등록하기
    if message.content.startswith(f'{PREFIX}register '):
        sheet_name = message.content.split(' ')[1]
        member_sheets[message.author.id] = sheet_name
        await message.channel.send(f"Registered sheet '{sheet_name}' for user {message.author.name}.")

    await bot.process_commands(message)

# Retrieve data from registered sheet for user who sent command
@bot.command(name='getdata')
async def get_data(ctx, cell):
    member_id = ctx.author.id
    sheet_name = member_sheets.get(member_id)
    if sheet_name is None:
        await ctx.send("You haven't registered a sheet yet!")
        return
    try:
        sheet = client.open_by_key('<spreadsheet_id>').worksheet(sheet_name)
        value = sheet.acell('F14').value
        await ctx.send(f"The value at in sheet '{sheet_name}' is '{value}'.")
    except gspread.exceptions.WorksheetNotFound:
        await ctx.send(f"Sheet '{sheet_name}' not found in spreadsheet.")
    except gspread.exceptions.CellNotFound:
        await ctx.send(f"Cell not found in sheet '{sheet_name}'.")

# Run the bot
bot.run(TOKEN)
