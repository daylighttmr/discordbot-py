import discord
from discord.ext import commands
import os
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from dotenv import load_dotenv
load_dotenv()

# Set command prefix and bot token from environment variables
PREFIX = os.getenv('PREFIX')
TOKEN = os.getenv('TOKEN')

# Set up Google Sheets API credentials
creds = ServiceAccountCredentials.from_json_keyfile_name('daylighttmr-bcd50a44ed0c.json', ['https://www.googleapis.com/auth/spreadsheets'])

# Create bot instance
bot = commands.Bot(command_prefix=PREFIX)

# File path for storing the member sheets data
DATA_FILE = "member_sheets.json"

# Load member sheets data from file
def load_member_sheets():
    try:
        with open(DATA_FILE, "r", encoding='UTF-8') as file:
            json_data = file.read()
            data_dict = json.loads(json_data)
            return data_dict
    except FileNotFoundError:
        return {}

# Save member sheets data to file
def save_member_sheets(member_sheets):
    with open(DATA_FILE, "w", encoding='UTF-8') as file:
        json.dump(member_sheets, file, ensure_ascii=False)

# Load member sheets data on bot startup
def setup_bot():
    global member_sheets
    member_sheets = load_member_sheets()
    print(f"Logged in as {bot.user}.")



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

# Load member sheets data after bot is ready
@bot.event
async def on_ready():
    setup_bot()

    
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
    
@bot.command(name='AWHO')
async def awho(ctx):
    anames = ["포모나 머피". "그라시아 블랑코", "닉 켄드릭", "데이빗", "에이버리 윌리엄스", "베네 산드루", "레베카", "베티 웰즈", "네이선 퍼소프", "로버트 '롭' 글렌", "스테파니 루비오", "함영선 데오도라", "필립 웰랜드", "로미오 피아프", "니키 빅"]
    callname = random.choice(anames)
    await ctx.reply(callname)
    
@bot.command(name='BWHO')
async def bwho(ctx):
    bnames = ["케일럼 반 웨스턴", "데이비드 조니 바니스터", "리코 버호벤", "크리스 가데니아", "헤벨 로헬", "밀러 제이", "로저 하워드", "올리버 윈스턴", "가브리엘 코스타", "이노스 마셜", "빌리 깁스", "벤자민 위버", "알마 던스트", "크레이그 켈먼", "다니엘 포터필드", "오스틴 박"]
    namecall = random.choice(bnames)
    await ctx.reply(namecall)
    
    
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
@bot.command(name='등록')
async def register_sheet(ctx, sheet_name: str):
    # Save the sheet name in the member_sheets dictionary
    member_id = ctx.author.id
    # print('member_id:', member_id)
    # print('id type:', type(member_id))
    # print('전체 m.s:', member_sheets)
    # print('타입:', type(member_sheets))
    member_sheets[str(member_id)] = sheet_name
    # print('m_s dict 업데이트:', member_sheets[member_id])
    # print('업데이트 후 m.s:', member_sheets)

    # Save the member_sheets dictionary to file
    save_member_sheets(member_sheets)
    await update_member_worksheet(ctx, member_sheets)
    # Reply to the message with the registration confirmation
    await ctx.reply(f"🌇 {ctx.author.name}의 시트 '{sheet_name}' 등록 완료")

# Get data from registered sheet for the user who sent the command

async def get_member_worksheet(ctx):
    member_id = ctx.author.id
    sheet_name = member_sheets.get(str(member_id))
    
    if sheet_name is None:
        await ctx.reply("😵 시트를 등록해주세요.")
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

async def update_member_worksheet(ctx, member_sheets):
    print('update_member_worksheet start ====>')
    sheet_name = "JSON"
    try:
        # Authenticate with Google Sheets API
        gc = gspread.authorize(creds)
        
        # Open the Google Spreadsheet by ID
        sheet_id = '1zb5gLeAns7CMUGHlk-4cCC9Tf5V2s4nq_K1Ja7p9U4Y'
        spreadsheet = gc.open_by_key(sheet_id)
        
        # Retrieve the worksheet by name
        
        worksheet = spreadsheet.worksheet(sheet_name)

    
        try:
            worksheet.update('A1', str(member_sheets))

        except Exception as e:
            print(e)
            return {'code' : -2, 'action_result_str' : 'reservation 오류. 메세지를 캡쳐 후 총괄에게 문의 바랍니다.' + '\n\n' + str(e)}

        return worksheet
    
    except gspread.exceptions.WorksheetNotFound:
        await ctx.reply(f"Sheet '{sheet_name}' not found in the spreadsheet.")
    
    except Exception as e:
        await ctx.reply(f"An error occurred: {str(e)}")
    
    return None
            
# Command to roll 2D6 dice and add to cell
@bot.command(name='설득')
async def roll_and_add(ctx):
    worksheet = await get_member_worksheet(ctx)
    
    if worksheet is not None:
        try:
            # Roll two six-sided dice
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            
            # Retrieve the current value from cell Z28
            cell_value = int(worksheet.acell('Z26').value)
            
            # Calculate the sum of the dice roll and the cell value
            sum_value = cell_value + dice1 + dice2
            
            # Reply to the message with the dice roll and the updated total
            await ctx.reply(f"🎲 {dice1}, {dice2}! \r 설득 기술 {cell_value}, 총합 {sum_value}.")
        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'Z26' not found in the worksheet.")
            


@bot.command(name='위협')
async def roll_and_add(ctx):
    worksheet = await get_member_worksheet(ctx)
    
    if worksheet is not None:
        try:
            # Roll two six-sided dice
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            
            # Retrieve the current value from cell Z28
            cell_value = int(worksheet.acell('Z27').value)
            
            # Calculate the sum of the dice roll and the cell value
            sum_value = cell_value + dice1 + dice2
            
            # Reply to the message with the dice roll and the updated total
            await ctx.reply(f"🎲 {dice1}, {dice2}! \r 위협 기술 {cell_value}, 총합 {sum_value}.")
        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'Z27' not found in the worksheet.")
            
@bot.command(name='탐색')
async def feel(ctx, number: int = None):
    worksheet = await get_member_worksheet(ctx)
    
    if worksheet is not None:
        try:
            # Roll two six-sided dice
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            
            # Retrieve the current value from cell AK17
            cell_value = int(worksheet.acell('AK17').value)
            
            if number is not None:
                # Calculate the sum of the dice roll, cell value, and the mentioned number
                sum_value = cell_value + dice1 + dice2 + number
            else:
                # Calculate the sum of the dice roll and the cell value
                sum_value = cell_value + dice1 + dice2
            
            # Reply to the message with the dice roll and the updated total
            await ctx.reply(f"🎲 {dice1}, {dice2}! \r 탐색 {cell_value}, 총합 {sum_value}.")
        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'AK17' not found in the worksheet.")

@bot.command(name='통찰')
async def think(ctx, number: int = None):
    worksheet = await get_member_worksheet(ctx)
    
    if worksheet is not None:
        try:
            # Roll two six-sided dice
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            
            # Retrieve the current value from cell AK19
            cell_value = int(worksheet.acell('AK19').value)
            
            if number is not None:
                # Calculate the sum of the dice roll, cell value, and the mentioned number
                sum_value = cell_value + dice1 + dice2 + number
            else:
                # Calculate the sum of the dice roll and the cell value
                sum_value = cell_value + dice1 + dice2
            
            # Reply to the message with the dice roll and the updated total
            await ctx.reply(f"🎲 {dice1}, {dice2}! \r 통찰 {cell_value}, 총합 {sum_value}.")
        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'AK19' not found in the worksheet.")
            
            
@bot.command(name='눈치')
async def roll_and_add(ctx):
    worksheet = await get_member_worksheet(ctx)
    
    if worksheet is not None:
        try:
            # Roll two six-sided dice
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            
            # Retrieve the current value from cell Z28
            cell_value = int(worksheet.acell('Z28').value)
            
            # Calculate the sum of the dice roll and the cell value
            sum_value = cell_value + dice1 + dice2
            
            # Reply to the message with the dice roll and the updated total
            await ctx.reply(f"🎲 {dice1}, {dice2}! \r 눈치 기술 {cell_value}, 총합 {sum_value}.")
        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'Z28' not found in the worksheet.")
            

@bot.command(name='속임수')
async def roll_and_add(ctx):
    worksheet = await get_member_worksheet(ctx)
    
    if worksheet is not None:
        try:
            # Roll two six-sided dice
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            
            # Retrieve the current value from cell Z28
            cell_value = int(worksheet.acell('Z29').value)
            
            # Calculate the sum of the dice roll and the cell value
            sum_value = cell_value + dice1 + dice2
            
            # Reply to the message with the dice roll and the updated total
            await ctx.reply(f"🎲 {dice1}, {dice2}! \r 속임수 기술 {cell_value}, 총합 {sum_value}.")
        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'Z29' not found in the worksheet.")
            
            
# Command to roll 2D6 dice and add to cell Z30
@bot.command(name='사격')
async def roll_and_add(ctx):
    worksheet = await get_member_worksheet(ctx)
    
    if worksheet is not None:
        try:
            # Roll two six-sided dice
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            
            # Retrieve the current value from cell Z28
            cell_value = int(worksheet.acell('Z30').value)
            
            # Calculate the sum of the dice roll and the cell value
            sum_value = cell_value + dice1 + dice2
            
            # Reply to the message with the dice roll and the updated total
            await ctx.reply(f"🎲 {dice1}, {dice2}! \r 사격 기술 {cell_value}, 총합 {sum_value}.")
        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'Z30' not found in the worksheet.")
            
            
# Command to roll 2D6 dice and add to cell Z31
@bot.command(name='육탄전')
async def roll_and_add(ctx):
    worksheet = await get_member_worksheet(ctx)
    
    if worksheet is not None:
        try:
            # Roll two six-sided dice
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            
            # Retrieve the current value from cell Z28
            cell_value = int(worksheet.acell('Z31').value)
            
            # Calculate the sum of the dice roll and the cell value
            sum_value = cell_value + dice1 + dice2
            
            # Reply to the message with the dice roll and the updated total
            await ctx.reply(f"🎲 {dice1}, {dice2}! \r 육탄전 기술 {cell_value}, 총합 {sum_value}.")
        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'Z31' not found in the worksheet.")
            
            
# Command to roll 2D6 dice and add to cell Z32
@bot.command(name='무브먼트')
async def roll_and_add(ctx):
    worksheet = await get_member_worksheet(ctx)
    
    if worksheet is not None:
        try:
            # Roll two six-sided dice
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            
            # Retrieve the current value from cell Z28
            cell_value = int(worksheet.acell('Z32').value)
            
            # Calculate the sum of the dice roll and the cell value
            sum_value = cell_value + dice1 + dice2
            
            # Reply to the message with the dice roll and the updated total
            await ctx.reply(f"🎲 {dice1}, {dice2}! \r 무브먼트 기술 {cell_value}, 총합 {sum_value}.")
        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'Z32' not found in the worksheet.")
            
            
# Command to roll 2D6 dice and add to cell Z33
@bot.command(name='은신')
async def roll_and_add(ctx):
    worksheet = await get_member_worksheet(ctx)
    
    if worksheet is not None:
        try:
            # Roll two six-sided dice
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            
            # Retrieve the current value from cell Z28
            cell_value = int(worksheet.acell('Z33').value)
            
            # Calculate the sum of the dice roll and the cell value
            sum_value = cell_value + dice1 + dice2
            
            # Reply to the message with the dice roll and the updated total
            await ctx.reply(f"🎲 {dice1}, {dice2}! \r 은신 기술 {cell_value}, 총합 {sum_value}.")
        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'Z33' not found in the worksheet.")
            
                        
@bot.command(name='손재주')
async def craft(ctx, number: int = None):
    worksheet = await get_member_worksheet(ctx)
    
    if worksheet is not None:
        try:
            # Roll two six-sided dice
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            
            # Retrieve the current value from cell AJ26
            cell_value = int(worksheet.acell('AJ26').value)
            
            if number is not None:
                # Calculate the sum of the dice roll, cell value, and the mentioned number
                sum_value = cell_value + dice1 + dice2 + number
            else:
                # Calculate the sum of the dice roll and the cell value
                sum_value = cell_value + dice1 + dice2
            
            # Reply to the message with the dice roll and the updated total
            await ctx.reply(f"🎲 {dice1}, {dice2}! \r 손재주 기술 {cell_value}, 총합 {sum_value}.")
        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'AJ26' not found in the worksheet.")
            
            
@bot.command(name='치료')
async def heal(ctx, number: int = None):
    worksheet = await get_member_worksheet(ctx)
    
    if worksheet is not None:
        try:
            # Roll two six-sided dice
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            
            # Retrieve the current value from cell AJ27
            cell_value = int(worksheet.acell('AJ27').value)
            
            if number is not None:
                # Calculate the sum of the dice roll, cell value, and the mentioned number
                sum_value = cell_value + dice1 + dice2 + number
            else:
                # Calculate the sum of the dice roll and the cell value
                sum_value = cell_value + dice1 + dice2
            
            # Reply to the message with the dice roll and the updated total
            await ctx.reply(f"🎲 {dice1}, {dice2}! \r 치료 기술 {cell_value}, 총합 {sum_value}.")
        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'AJ27' not found in the worksheet.")
            

@bot.command(name='운전')
async def drive(ctx, number: int = None):
    worksheet = await get_member_worksheet(ctx)
    
    if worksheet is not None:
        try:
            # Roll two six-sided dice
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            
            # Retrieve the current value from cell AJ28
            cell_value = int(worksheet.acell('AJ28').value)
            
            if number is not None:
                # Calculate the sum of the dice roll, cell value, and the mentioned number
                sum_value = cell_value + dice1 + dice2 + number
            else:
                # Calculate the sum of the dice roll and the cell value
                sum_value = cell_value + dice1 + dice2
            
            # Reply to the message with the dice roll and the updated total
            await ctx.reply(f"🎲 {dice1}, {dice2}! \r 운전 기술 {cell_value}, 총합 {sum_value}.")
        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'AJ28' not found in the worksheet.")
            
            
@bot.command(name='요리')
async def cook(ctx, number: int = None):
    worksheet = await get_member_worksheet(ctx)
    
    if worksheet is not None:
        try:
            # Roll two six-sided dice
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            
            # Retrieve the current value from cell AJ29
            cell_value = int(worksheet.acell('AJ29').value)
            
            if number is not None:
                # Calculate the sum of the dice roll, cell value, and the mentioned number
                sum_value = cell_value + dice1 + dice2 + number
            else:
                # Calculate the sum of the dice roll and the cell value
                sum_value = cell_value + dice1 + dice2
            
            # Reply to the message with the dice roll and the updated total
            await ctx.reply(f"🎲 {dice1}, {dice2}! \r 요리 기술 {cell_value}, 총합 {sum_value}.")
        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'AJ29' not found in the worksheet.")
            

@bot.command(name='기계')
async def machina(ctx, number: int = None):
    worksheet = await get_member_worksheet(ctx)
    
    if worksheet is not None:
        try:
            # Roll two six-sided dice
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            
            # Retrieve the current value from cell AJ30
            cell_value = int(worksheet.acell('AJ30').value)
            
            if number is not None:
                # Calculate the sum of the dice roll, cell value, and the mentioned number
                sum_value = cell_value + dice1 + dice2 + number
            else:
                # Calculate the sum of the dice roll and the cell value
                sum_value = cell_value + dice1 + dice2
            
            # Reply to the message with the dice roll and the updated total
            await ctx.reply(f"🎲 {dice1}, {dice2}! \r 기계 기술 {cell_value}, 총합 {sum_value}.")
        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'AJ30' not found in the worksheet.")
            
            
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
                await ctx.reply(f"🌇 현재 체력: {current_value} / 최대 체력: {max_value}.")
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
            
      #정신력 커맨드
@bot.command(name='SP')
async def get_and_add_sp(ctx, value: int = None):
    worksheet = await get_member_worksheet(ctx)
    
    if worksheet is not None:
        try:
            # Retrieve the current value from cell J25
            current_value = int(worksheet.acell('J25').value)
            max_value = int(worksheet.acell('N25').value)
            
            if value is None:
                # If no value is specified, only retrieve and reply with the current value
                await ctx.reply(f"🌃 현재 정신력: {current_value} / 최대 정신력: {max_value}.")
            else:
                # If a value is specified, add it to the current value and update cell J25
                new_value = current_value + value
                worksheet.update('J25', new_value)
                
                if new_value < max_value * 0.25:
                    # If the condition is met, select a random description from the list
                    descriptions = [
                        "눈앞이 가리워진 것 같이, 모든 것이 무의미해진다⋯⋯.",
                        "목을 조르는 것 같은 압박에 휩싸인다.",
                        "불안의 수렁에 빠진 것 같이, 숨을 쉴 수 없다.",
                        "한계에 도달했다. 남은 것은 폐허와 파괴 뿐이다⋯⋯."
                    ]
                    embed_description = random.choice(descriptions)
                    
                    embed_title = "극도의 스트레스 상태!"
                    
                    # Append the common description
                    embed_description += "\n정신이 무너집니다. 스스로를, 혹은 타인을 망가뜨리지 않으면 견딜 수 없을 정도로. \r  💡 YN 명령어로, ⭕️: 자해 / ❌: 상해를 고릅니다. 운에 맡기지 않고 스스로 선택할 수도 있습니다."
                
                elif new_value <= max_value * 0.5:
                    embed_title = "스트레스 반응 발동!"
                    embed_description = random.choice([
                        "뭔가가 잘못됐다.",
                        "이게 아니야, 이런 게 아니야⋯⋯.",
                        "내면에서 뭔가가 망가져 간다."
                    ])
                    
                    # Append the common description and the text from cells F30 and F31
                    text1 = worksheet.acell('F30').value
                    text2 = worksheet.acell('F31').value
                    embed_description += f"\n💡 현재 정신력 {new_value}, 스트레스 반응 발동.\r YN 명령어로, ⭕️: {text1} / ❌: {text2} 중에서 고릅니다. 운에 맡기지 않고 스스로 선택할 수도 있습니다. 이 상태는 정신력을 회복할 때까지 계속됩니다."
                
                else:
                    await ctx.reply(f"🌃 정신력, {current_value}에서 {new_value}로 적용.")
                    return
                
                # Create and send the embed message
                embed = discord.Embed(title=embed_title, description=embed_description)
                await ctx.reply(embed=embed)
        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("One or more cells not found in the worksheet.")



# Run the bot
bot.run(TOKEN)

