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

    
@bot.command(name='1D6')
async def roll_dice(ctx):
    dice_roll = random.randint(1, 6)
    await ctx.reply(f"🎲 {dice_roll}!")
    
    
@bot.command(name='2D6')
async def add_dice(ctx, num1: int = 0, num2: int = 0):
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    dice_sum = dice1 + dice2 + num1 + num2
    
    if dice_sum >= 12:
        await ctx.reply(f"🎲 {dice1} , {dice2}. \r 결과는 {dice_sum}, :star2: *특별 성공* :star2:")
    elif dice_sum >= 10:
        await ctx.reply(f"🎲 {dice1} , {dice2}. 결과는 {dice_sum}, :star2: *도전 성공*")
    elif dice_sum >= 8:
        await ctx.reply(f"🎲 {dice1} , {dice2}. 결과는 {dice_sum}, :star: *일반 성공*")
    else:
        await ctx.reply(f"🎲 {dice1} , {dice2}. 결과는 {dice_sum}. ")

        
@bot.command(name='YN')
async def yes_or_no(ctx):
    responses = ["YES", "NO", "YUP", "NOPE", "👍", "👎", "⭕️", "❌"]
    response = random.choice(responses)
    await ctx.reply(response)

# Random paragraph
paragraphs = [
    "This is the first paragraph.",
    "Here is another paragraph.",
    "This is the third paragraph.",
    "Yet another paragraph.",
    "And finally, a fifth paragraph."
]

@bot.command(name='GO')
async def random_paragraph(ctx):
    random_p = random.choice(paragraphs)
    embed = discord.Embed(title="Random Paragraph", description=random_p)
    await ctx.send(embed=embed)


# Register user's worksheet
@bot.command(name='register')
async def register_sheet(ctx, sheet_name: str):
    # Save the sheet name in a dictionary with user ID as the key
    member_id = ctx.author.id
    member_sheets[member_id] = sheet_name
    
    # Reply to the message with the registration confirmation
    await ctx.reply(f"Registered sheet '{sheet_name}' for user {ctx.author.name}.")

# Get data from registered sheet for the user who sent the command

@bot.command(name='치료')
async def get_data_치료(ctx):
    await retrieve_cell_range(ctx, "AJ27:AK27", "치료")

@bot.command(name='운전')
async def get_data_운전(ctx):
    await retrieve_cell_range(ctx, "AJ28:AK28", "운전")

@bot.command(name='손재주')
async def get_data_손재주(ctx):
    await retrieve_cell_range(ctx, "AJ26:AK26", "손재주")

async def retrieve_cell_range(ctx, cell_range, command_name):
    # Retrieve the sheet name for the user
    member_id = ctx.author.id
    sheet_name = member_sheets.get(member_id)
    
@bot.command(name='getdata')
async def get_data(ctx, cell: str):
    # Retrieve the sheet name for the user
    member_id = ctx.author.id
    sheet_name = member_sheets.get(member_id)
    
    # Check if the user has registered a sheet
    if sheet_name is None:
        await ctx.reply("You haven't registered a sheet yet!")
        return
    
    try:
        # Authenticate with Google Sheets API
        gc = gspread.authorize(creds)
        
        # Open the Google Spreadsheet by ID
        sheet_id = '1zb5gLeAns7CMUGHlk-4cCC9Tf5V2s4nq_K1Ja7p9U4Y'
        spreadsheet = gc.open_by_key(sheet_id)
        
        # Retrieve the worksheet by name
        worksheet = spreadsheet.worksheet(sheet_name)
        
        # Retrieve the value from the specified cell
        value = worksheet.acell(cell).value
        
        # Reply to the message with the retrieved value
        await ctx.reply(f"The value in sheet '{sheet_name}' at cell '{cell}' is '{value}'.")
    
    except gspread.exceptions.WorksheetNotFound:
        await ctx.reply(f"Sheet '{sheet_name}' not found in the spreadsheet.")
    
    except gspread.exceptions.CellNotFound:
        await ctx.reply(f"Cell '{cell}' not found in sheet '{sheet_name}'.")


# Run the bot
bot.run(TOKEN)

