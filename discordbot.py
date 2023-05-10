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
    if dice_sum >=10:
        await ctx.reply(f"🎲 {dice1} , {dice2}. 결과는 {dice_sum}, :star2: *도전 성공*")
    if dice_sum >=8:
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

@bot.command(name='go')
async def random_paragraph(ctx):
    random_p = random.choice(paragraphs)
    embed = discord.Embed(title="Random Paragraph", description=random_p)
    await ctx.reply(embed=embed)



# Run the bot
bot.run(TOKEN)
