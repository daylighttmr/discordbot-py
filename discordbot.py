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


# Create dictionary to store member's worksheet names
member_sheets = {와플: 'NPC 닥터 닥터 카마이클-시보마나'}    
    
# Register user's worksheet
@bot.command(name='등록')
async def register_sheet(ctx, sheet_name: str):
    # Save the sheet name in a dictionary with user ID as the key
    member_id = ctx.author.id
    member_sheets[member_id] = sheet_name
    
    # Reply to the message with the registration confirmation
    await ctx.reply(f"🌇 {ctx.author.name}의 시트 '{sheet_name}' 등록 완료")

# Get data from registered sheet for the user who sent the command

async def get_member_worksheet(ctx):
    member_id = ctx.author.id
    sheet_name = member_sheets.get(member_id)
    
    if sheet_name is None:
        await ctx.reply("You haven't registered a sheet yet!")
        return None
    
    try:
        # Authenticate with Google Sheets API
        gc = gspread.authorize(creds)
        
        # Open the Google Spreadsheet by ID
        sheet_id = '1zb5gLeAns7CMUGHlk-4cCC9Tf5V2s4nq_K1Ja7p9U4Y'
        spreadsheet = gc.open_by_key(sheet_id)
        
        # Retrieve the worksheet by name
        worksheet = spreadsheet.worksheet(sheet_name)
        
        return worksheet
    
    except gspread.exceptions.WorksheetNotFound:
        await ctx.reply(f"Sheet '{sheet_name}' not found in the spreadsheet.")
    
    except Exception as e:
        await ctx.reply(f"An error occurred: {str(e)}")
    
    return None

# Command to retrieve 손재주 value
@bot.command(name='손재주')
async def get_data_손재주(ctx):
    worksheet = await get_member_worksheet(ctx)
    
    if worksheet is not None:
        try:
            # Retrieve the value from the specified cell
            cell_value = worksheet.acell('AJ26').value
            
            # Reply to the message with the retrieved value
            await ctx.reply(f"'{worksheet.title}'에서 손재주는 '{cell_value}'.")
        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'AJ26' not found in the worksheet.")

# Command to retrieve 운전 value
@bot.command(name='운전')
async def get_data_운전(ctx):
    worksheet = await get_member_worksheet(ctx)
    
    if worksheet is not None:
        try:
            # Retrieve the value from the specified cell
            cell_value = worksheet.acell('AJ28').value
            
            # Reply to the message with the retrieved value
            await ctx.reply(f"'{worksheet.title}'에서 운전은 '{cell_value}'.")
        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'AJ28' not found in the worksheet.")
            
 # Command to roll 2D6 dice and add to cell Z28
@bot.command(name='눈치')
async def roll_and_add(ctx):
    worksheet = await get_member_worksheet(ctx)
    
    if worksheet is not None:
        try:
            # Roll two six-sided dice
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            
            # Retrieve the current value from cell Z28
            cell_value = worksheet.acell('Z28').value
            
            # Convert the current value to an integer and add the dice roll
            sum_value = cell_value + dice1 + dice2
            
            # Reply to the message with the dice roll and the updated total
            await ctx.reply(f"🎲 {dice1}, {dice2}! /r 눈치 기술 {cell_value}, 총합 {sum_value}.")
        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'Z28' not found in the worksheet.")
            
            
  # Command to retrieve HP value and optionally add a number to it
@bot.command(name='HP')
async def get_and_add_hp(ctx, value: int = None):
    worksheet = await get_member_worksheet(ctx)
    
    if worksheet is not None:
        try:
            # Retrieve the current value from cell J22
            current_value = int(worksheet.acell('J22').value)
            max_value = int(worksheet.acell('N22').value)
            
            if value is None:
                # If no value is specified, only retrieve and reply with the current value
                await ctx.reply(f"🌇 현재 체력: {current_value}.")
            else:
                # If a value is specified, add it to the current value and update cell J22
                new_value = current_value + value
                worksheet.update('J22', new_value)
                
                # Determine the message based on the new HP value
                message = "신체 상태"
                if new_value >= max_value:
                    message = "건강함"
                elif new_value == 1:
                    message = "빈사: 행동 불능"
                elif new_value < max_value / 4:
                    message = "치명상: 행동 페널티"
                elif 0.5 * max_value < new_value:
                    message = "경미한 부상"
                elif new_value >= 2:
                    message = "심한 부상"
                
                await ctx.reply(f"🌇 체력: {current_value} 에서 {new_value} 로 적용. 현재 신체 상태는 {message}")
        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'J22' or 'N22' not found in the worksheet.")



# Run the bot
bot.run(TOKEN)

