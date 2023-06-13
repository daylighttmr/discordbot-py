import discord
from discord.ext import commands
import os
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from dotenv import load_dotenv
load_dotenv()
import re

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


# 230517 JAMONG - 추가 인자 연산 기능 추가
def add_cal(additional_arg):
    add_list = []
    tmp_flag = False
    start_i = ''
    end_i = ''
    for i in range(len(additional_arg)):
        print(i, additional_arg[i])
        if tmp_flag==False:
            if additional_arg[i] == '+':
                tmp_flag = True
                start_i = i
            elif additional_arg[i] == '-':
                tmp_flag = True
                start_i = i
        elif tmp_flag == True:
            if additional_arg[i] in ['+', '-']:
                if start_i + 1 == i:
                    print('연산자 두개가 동시에 나오는 에러')
                    return 0
                else:
                    end_i = i

        if (start_i != '' and end_i != '') or (start_i != '' and i+1 == len(additional_arg)):
            if end_i == '':
                end_i = None
            

            add_list.append(int(additional_arg[start_i:end_i]))
            start_i = i
            end_i = ''
    return sum(add_list)

def success_level(dice):
    if dice >= 12:
        return ", :star2: *특별 성공*"
    elif dice >= 10:
        return ", :star2: *도전 성공*"
    elif dice >= 8:
        return ", :star: *일반 성공*"
    else:
        return "."

# 230517 JAMONG - 커맨드 리스트 정리 
# commands_list = ['!1D6', '!2D6', '!YN', '!AWHO', '!BWHO', '!WHO', '!NIGHT', '!등록', '!설득', '!위협', '!탐색', '통찰', '눈치', '속임수', '사격', '육탄전', '무브먼트', '은신', '손재주', '치료', '운전', '요리', '기계', 'HP', 'SP']
# startswith_commans_list = ['설득', '위협', '탐색', '통찰', '눈치', '속임수', '사격', '육탄전', '무브먼트', '은신', '손재주', '치료', '운전', '요리', '기계']

# Respond to messages
@bot.event
async def on_message(message):
    print('message.content:', message.content)
    if message.author == bot.user:
        return

    if message.content == f'{PREFIX}call':
        await message.channel.send("callback!")

    if message.content.startswith(f'{PREFIX}hello'):
        await message.channel.send('Hello!')

    # 230517 JAMONG - 스레드 메세지에도 응답하도록 수정
    # if message.content in commands_list:
    #     if isinstance(message.channel, discord.ThreadChannel):  # 스레드 응답
    #         await bot.process_commands(message) 
    #     else:
    #         await bot.process_commands(message)  # 명령어를 처리하기 위해 process_commands를 호출합니다.

    await bot.process_commands(message)



# Load member sheets data after bot is ready
@bot.event
async def on_ready():
    setup_bot()

    
    
@bot.command(name='1D6')
async def roll_dice(ctx, additional_args:str=None):
    sum_value = random.randint(1, 6)

    if additional_args != None:
        sum_value += add_cal(additional_args)
            
    await ctx.reply(f"🎲 {sum_value}!")
    
    
@bot.command(name='2D6')
async def add_dice(ctx, additional_args:str=None):
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    sum_value = dice1 + dice2
    
    if additional_args != None:
        sum_value += add_cal(additional_args)

    await ctx.reply(f"🎲 {sum_value}!")
        

        
@bot.command(name='YN')
async def yes_or_no(ctx):
    responses = ["YES", "NO", "YUP", "NOPE", "👍", "👎", "⭕️", "❌"]
    response = random.choice(responses)
    await ctx.reply(response)
    
@bot.command(name='AWHO')
async def awho(ctx):
    anames = anames = ["그라시아 블랑코", "닉 켄드릭", "데이빗", "에이버리 윌리엄스", "베네 산드루", "베티 웰즈", "네이선 퍼소프", "로버트 '롭' 글렌", "스테파니 루비오", "함영선 데오도라", "로미오 피아프", "니키 빅"]
    callname = random.choice(anames)
    await ctx.reply(callname)
    
@bot.command(name='BWHO')
async def bwho(ctx):
    bnames = ["케일럼 반 웨스턴", "데이비드 조니 바니스터", "리코 버호벤", "크리스 가데니아", "헤벨 로헬", "밀러 제이", "로저 하워드", "가브리엘 코스타", "이노스 마셜", "벤자민 위버", "알마 던스트", "크레이그 켈먼", "다니엘 포터필드", "오스틴 박"]
    namecall = random.choice(bnames)
    await ctx.reply(namecall)
    
@bot.command(name='WHO')
async def who(ctx):
    names = ["그라시아 블랑코", "닉 켄드릭", "데이빗", "에이버리 윌리엄스", "베네 산드루", "베티 웰즈", "네이선 퍼소프", "로버트 '롭' 글렌", "스테파니 루비오", "함영선 데오도라", "로미오 피아프", "니키 빅", "케일럼 반 웨스턴", "데이비드 조니 바니스터", "리코 버호벤", "크리스 가데니아", "헤벨 로헬", "밀러 제이", "로저 하워드", "가브리엘 코스타", "이노스 마셜", "벤자민 위버", "알마 던스트", "크레이그 켈먼", "다니엘 포터필드", "오스틴 박", "에인슬리 칼헌"]
    call = random.choice(names)
    await ctx.reply(call)
    
benelines = [
    "조금만 더 참으면 다시 좋은 일이 일어날지도 몰라요!",
    "이들과 함께 할 수 있어서 좋은 일이죠. 그래서 슬퍼하고 힘들어 하기 어려워요. 무서움조차 잊어버릴 만큼 너무 행복한걸 어쩌겠어요?",
    "차라리요. 가끔 그런 생각을 해요. 맨 처음에 사고로 진작 죽어버렸다면 이렇게 괴롭지도 않았을텐데. 말세에서 다 허물어져가는 도덕성과 씨름하지 않아도 될텐데.",
    "사랑하는 것들을 지키기 위해서는 당연한 일이라고 생각했고 그 말대로 행동했죠. 그치만 봐요. 배려와 관용으로는 세상이 움직이지 않아요.",
    "인간성이란게 도대체 뭔가요? 파벨라에서 제일 사람답게 산다던 저조차도 이러는데요.",
    "돌아가고 싶어요. 근데 못가잖아요. 여긴 내 고향도 아니고요. 나만 이런 상황도 아니고... 그래서 그만 생각하는거죠. 차라리 그게 나으니까.",
    "여기가 숨막혀요! 내가 사랑하는건 돌아오지도 않는데, 내가 아는 고향은 여기가 아닌데. 날 일으켜 세워주는건 아무것도 없는데! 내가 여길 왜 사랑해! 왜! ",
    "괴로움에 몸부림쳐도 살아있어요. 그냥 다 고장난 사람처럼 숨만 쉬는게 아니라.",
    "그래도 나는 우리가 나눈 이야기가 정말 좋아요.",
    "금방 올게요"
]

@bot.command(name='베네')
async def 베네(ctx):
    random_bene = random.choice(benelines)
    await ctx.reply(random_bene)
    
    
gavlines = [
    "가브리엘이라고 불러요. 게이브, 가비, 울프. 다 상관없어요.",
    "혹시 치료가 필요한 사람있다면 언제든 찾아와도 좋아.",
    "코고는 소리는 어디로 항의 넣어야해?",
    "난 월마트에서 일했었어. 여행하면서 돈이 필요했거든. 돈을 다 벌면 동부로 가려고 했는데... 혹시 넌 뉴욕 가본 적 있어?",
    "하지만 날 도와주는 사람이 없었다면 이런 여행은 못했어. 미국 서부를 돌아다니면서 만나는 사람들은 다 좋았지. 물론 레드넥들도 있었지만 말이야. 말했다시피 여긴 시골이니까. 그리고 지금은... 좋은 사람들을 만난 것 같아. 너도.",
    "당신이 새 가족을 찾으라고 했죠? 덕분에 찾은 것 같아요.",
    "있잖아. 만약 네가 지켜야하는 것들과 꼭 해야만 하는 것들에서 고른다면 뭘 고를래?",
    "네, 맞아요. 이해해요. 저도 피아노를 막 배웠을 때 베토벤이 엘리제를 육십 번쯤 죽였을걸요.",
    "더 당하지 않게, 죽지 않게 행동해야지. 이미 벌어진 일이야. 되돌릴 수 없어.",
    "...슬퍼요. 진심으로요."
]

@bot.command(name='가브리엘')
async def 가브리엘(ctx):
    random_gav = random.choice(gavlines)
    await ctx.reply(random_gav)
    
filines = [
    "쉘—터가 싫다고? 아니! 으흐흐흐... 아니! 난 그냥 여기가 망가지는 모습을 보기가 싫었을 뿐이야!",
    "그—래. 뉴 산타 바바라... 흐흐흐. 여기에 잠시 머물게 될 줄 몰랐어. 바다가 트인... 거쳐—집을 갖게 될 거라곤 상상도 못했고.",
    "즐기는 게 최고라고. 사랑하는 걸 즐기고— 시대의 반항아처럼!",
    "염병 네가 진짜 엄마냐? 아니면—좀 자식한테 관심 많은 아빠?",
    "난—그냥. 삶을 즐기는 게 자유가 아닐까 해. 친구.",
    "좋아— 이 지루한 틈에 내가 노래를 불러주지. I know— I know I know, i know I know⋯ (I Don't To Push It 中)",
    "오, 세상에. 지금 내가 골든 햄스터? 으흐흐. 찍찍. 받아주세요.",
    "으흐흐—내가 맞춰보지. 난⋯네 번째가 될 거야. 세 번짼 너무 적고, 다섯 번짼 너무 많으니까.",
    "내가 그립긴 했구나!",
    "난 * 이제부터* 약을 끊겠어. 이러다 진짜 뒤질—거야. 흐흐흐..."
]

@bot.command(name='파이')
async def 파이(ctx):
    random_fi = random.choice(filines)
    await ctx.reply(random_fi)
    
    
voices = [
    "그라시아 블랑코: 저는 그라시아 블랑코라고 하고 라이프가드에요. 옷차림이 너무 당연한가요?",
    "그라시아 블랑코: 인생은 불행을 줄때 행운도 함께준다는 말이 있잖아요. 그 말이 정말 맞는거 같아요.",
    "그라시아 블랑코: 구한뒤에 깨어나서 감사하다는 소리를 들으면 그만큼 행복한게 없죠. 그래서 이름이 그라시아인가봐요. 그 소리가 절 행복하게 만드니까요!",
    "그라시아 블랑코: 울고 털어내고 멀쩡히 돌아오면 그게 강한거죠!",
    "그라시아 블랑코: 제 이름이 그라시아-감사하다는 뜻이잖아요. 이미 제 이름을 부를때마다 감사받고 있죠!",
    "그라시아 블랑코: 편하게 도움을 요청하라구요. 그게 라이프가드가 하는일이잖아요. Help! 라는 말에 바로 달려가 구하는거요.",
    "그라시아 블랑코: 파티에 호세쿠엘보가 있으면 그라시아가 파티에 왔다는 뜻이었죠.",
    "그라시아 블랑코: 이 세상에서도 인간다움을 잃지 않는 쪽이요. 바보같고 위험하다해도 그게 저니까요.",
    "그라시아 블랑코: 그래도 만만하게 보면 안된다는 거죠! 사워캔디처럼 턱을 아프게 해줄수도 있으니까요.(주먹을 불끈 쥔다)",
    "그라시아 블랑코: (아이를 보자 자신의 신념을 더욱 강하게 확신한다. 아이에게 힘든세상속에서도 선한사람으로 살아가야할 가치를 보여주자고.)",
    "그라시아 블랑코: (오랜만에 보는 새빨간 수영복을 입고 바다를 향해 걸어간다. 허리춤에는 수건과 물방울이 맺힌 물병을 들고 샌들의 발걸음 소리를 내며 콧노래를 부른다)",
    "그라시아 블랑코: 할머니가 이야기해주셨거든요! 큰 파도는 바다가 탐나는걸 가져가려고 그러는 거라고...",
    "케일럼 반 웨스턴: 사람답게 냄새 안 나는 상태에서 뒈지고 싶어. 내 유언장에 써 있는 욕구를 그렇게 비웃지 마, fellas.",
    "케일럼 반 웨스턴: 유머가 공포의 항생제라는 말 있잖아! 다들 정신은 안 뒤진 모양이네.",
    "케일럼 반 웨스턴: 에이! 씨. 모르겠다. 죽지 마.",
    "케일럼 반 웨스턴: 첫 번째 여친은 중학교 때였어. 열네 살이었고. 선물을 진짜 많이 사 줬어. 근데 걔가 뭐랬는지 알아? 넌 뇌로 생각하는 법을 모르는 것 같아. 그래서 열받아서 두번째 여친 사귈 땐 책을 많이 읽었어. 루소, 마키아벨리, 모어, 데카르트, 스피노자. 그랬더니 뭐라고 했게? 씨발 아는 척 좀 그만해.",
    "케일럼 반 웨스턴: 이런 씨발... 정치 같은 건 딱 질색이야. 좆 같은 세상.",
    "케일럼 반 웨스턴: 아니, 나 이미 최고의 셰픈데? 나보다 요리 잘하는 사람 여기 없어.",
    "케일럼 반 웨스턴: 나한테는 그게 위선처럼 느껴지니까. 문명적인 사람은 그래야 한다는 걸 알아. 그렇게 하는 게 좋아 보이기도 해. 근데 결정적인 순간에는 나는 선함보다 우리의 안전을 고를 거고 도덕보다 복수를 하고 싶어할 거야.",
    "케일럼 반 웨스턴: 슬픈 영화는 빤해서 별로 눈물 안 나고, 슬픈 일은... 글쎄... 슬픈 일에 울면 지는 거 같아서 싫어.",
    "케일럼 반 웨스턴: 난 그게 당연하다고 생각해. 그게 인간 기본이야. 죽기 일보 직전에 남한테 약 줄 생각 드는 쪽이 비정상이지. 그래서 그런 미친 인간들을 영웅이라고 부르는 거고. 숭고한 희생을 내도록 이야기하며 찬미하는 건 드물기 때문이지. 안 그래?",
    "케일럼 반 웨스턴: 사람은 이기적이기에 이타적이게 된대. 내가 살기 위해서 타인이 필요하니까 다른 사람을 돕는다는 거야. 약을 반 꺾어 줄 수는 없어도 내가 먹은 뒤에 그 사람 부축은 할 수 있을지도 몰라.",
    "케일럼 반 웨스턴: 아니, 굳이 애인 문제로 안 끌고 가도 대머리는 슬프잖아. 머리숱은 젊음의 상징이라고. 탈모 안 온 아저씨들 다 행운인 줄 알아. 60대에는 65%가 탈모가 온댔단 말이야.",
    "케일럼 반 웨스턴: 누구나 그래도 돼. 모두의 목숨은 소중하다고 공익광고는 말하지. 세상은 안 그래. 다들 자기 게 제일 중요하고, 그 다음은 가까운 사람들이고, 그럴 거야.",
    "케일럼 반 웨스턴: 존나 패배감 든다... 염기서열의 꼬임 한두개 차이로 이렇게나 차이가 나야 한다니...",
    "케일럼 반 웨스턴: 산다는 건 그림을 그리는 거야. 계속 지워지는 그림을. 파도와 싸우면서...",
    "케일럼 반 웨스턴: 다른 사람이 당하는 것까지는 알 바 아냐. 지금의 나한테는 당신들이 다야.",
    "케일럼 반 웨스턴: 전엔 죽고 싶다고 생각할 때가 있었는데, 진짜 죽을 것 같아지니까 오히려 살고 싶더라고요.",
    "케일럼 반 웨스턴: 목표는 매일 아침에 새로 세워. 7시에 일어나서 다이너를 성공적으로 여는 거지. 장기적인 생각은 안 해.",
    "케일럼 반 웨스턴: *한때는 그렇게도 밝았던 광채가 이제 영원히 사라진다 해도, ... 그 시절을 다시 돌이킬 수 없다 해도, ... 우리 슬퍼하기보다, 차라리 뒤에 남긴 것에서 힘을 찾으리.*",
    "크레이그 켈먼: 제발 주님한테 빨리 좀 구해달라고 해주면 안 될까? 씨발, 구해만 준다면 기도도 해볼 테니까... ",
    "크레이그 켈먼: 진짜로, …내가 뒤졌나? 거기, 너무 아프지 않게 한 대만 때려주지 그래?",
    "크레이그 켈먼: 우린 정말 개자식들이야. 하지만 그럼에도 살아갈 거고, 이렇게 웃는 날도 있을 거야. 괜찮아. 너무 무서워하지 않아도 돼. 세상은 망했지만, 삶은 이어질 거야.",
    "크레이그 켈먼: 그럴 땐 그냥 토해버려. 울고 소리 지르고 해. 다들 그러고 있으니까. 참으려고 하면 더 힘들어지는 거야. …더 오래 버텨야 하잖아.",
    "크레이그 켈먼: 난 우리가 해온 걸 잃어버리는 게 너무 두려워. 위험을 감수해 가면서 이런 세상에서 빨리 '자라지 못한' 애를 책임져 줄 순 없어.",
    "크레이그 켈먼: 그렇다고 죽을 수는 없을 것 아냐. 나는 바닥을 쳐서라도 살아남고 싶어.",
    "크레이그 켈먼: 나중에 온 사람들은 내 알 바 아니야. 내 몸 하나만으로도 힘들고 이외 서른 명 덕분에 인생이 벅차기 그지없어. 난 더 신경 쓰지 않을 거야.",
    "크레이그 켈먼: 그으래, 너희, 다 한통속이다, 이거지? 됐어!",
    "크레이그 켈먼: 씨발, 그래도 뒤지기 싫으면 사는 거지!",
    "크레이그 켈먼: 나한테도 취향이란 게 있어!",
    "크레이그 켈먼: 우린 어딘가 잘못됐고, 넌 그걸 알아야만 해. 그래야 그게 약점이 되지 않을 수 있어. (또한,) 나는 너와 같은 높이에서 파도를 맞이할 거야.",
    "크레이그 켈먼: …네가 내 아들이 아니라는 건 나도 알아. 그래도 해야만 해. 내 아들이 지금의 너와 같다면, 누군가가, … 누구라도 나처럼 해주었으면 좋겠으니까. 난, 네가 내 아들이 아니어도 해야만 해. ….",
    "크레이그 켈먼: 하얀 머리, 빨간 머리, 검정 머리. 좋아, 다 있군.",
    "크레이그 켈먼: 요즘 부쩍 삶과 생존이 다르다는 걸 느껴. 한쪽을 깎아내야 다른 한쪽을 살릴 수 있지. 나는 생각보다 생존을 위해 삶을 덜어낼 수 있는 사람이었던 것 같아. 그쪽은 어때?",
    "크레이그 켈먼: 이제 시끄럽게 굴 기운도 없는 모양이지?",
    "크레이그 켈먼: …더 해. 너 때문에? 난 같이 붙들고 울어줄 사람 아니야. 사실 너 그렇게 된 거 신경도 많이 안 써. 그러니까 나중에 맘 약해서 같이 우울해질 사람한테 쏟아내지 말고 하던 얘기 더 해봐.",
    "크레이그 켈먼: 백만분의 일을 생각하자고. 다른 곳으로 피신했던 가족이 집부터 확인했다가 메시지를 듣는다고 상상해. 백만분의 일의 확률로라도, 우리가 전화를 찾고, 전화가 마침 걸리고, 메시지를 남길 수 있다고.",
    "크레이그 켈먼: 구경났어? 다 꺼져, 이놈들아, 꺼져!",
    "크레이그 켈먼: 으이구, 사람이 걱정을 해주면 걱정으로 좀 받아라. 꼰대가 뭐냐, 꼰대가.",
    "크레이그 켈먼: 나 정 없는 거 이제 알았냐? 방해 되고 식량만 축낼 것 같으면 꼭 두고 갈 거야. 뒤도 안 돌아볼 거라고! 그러니까 약한 소리 말고 바득바득 같이 갈 생각을 해라, 이놈아.",
    "니키 빅: 누가 가족이야. 한 번도 그렇게 생각한 적 없어.",
    "니키 빅: 그런 말 좀 그만해. 고분고분 말 잘듣는 애가 좋으면 바깥에서 하나 더 주워오든가. 내가 이런 앤 줄은 예전부터 알고 있었으면서 이제 와서 이래!",
    "니키 빅: 절대 잊지 마. 난 날 버리는 사람을 용서하지 않아.",
    "니키 빅: 항상 부끄러웠어. 수치스럽고 숨고 싶었어.",
    "니키 빅: 하지만 이렇게 살고 싶지 않았다고 말할 순 없잖아. 그건 분명 날 비참하게 할 테니까.",
    "니키 빅: 놈들이 내 인생을 휘두르는 꼴이 보기 싫었어. 더는 얌전히 숨죽이고 기다리고 싶지 않았어.",
    "니키 빅: 가. 그럴 기분 아냐.",
    "니키 빅: 이해해달라고 한 적 없어. 이렇게 살기 싫으면 나가서 뒤져.",
    "니키 빅: 너도 먹어. 잘 먹고 다녀야 빨리 낫는대. 안 나으면 계속 아프잖아. 응?",
    "니키 빅: 옆에 있는다고 했잖아. 같이 있어도 괜찮다고 말했잖아! 왜 이제 와서 그러는데, 왜!",
    "니키 빅: 미안. 미안해. 정말 이럴 줄은 몰랐어. 그때 난, 그냥 내 생각 밖에 없어서, ......미안.",
    "니키 빅: 꺼져, 이 등신아!",
    "니키 빅: 아, 씨. 내 옷 어딨어? 분명 여기 뒀는데!",
    "니키 빅: 난 그냥, 가족이 필요해.",
    "니키 빅: 이제 와서 그깟 게 무슨 소용이야. 사실은 버스 같은 거 필요 없어. 그냥 이것저것 요구하는 게 좋아서 그랬어. 들어줄지도 모른다고 생각하니까, 이까짓 말 한마디 때문에 고민하는 게 어쩐지 기분 좋아서......",
    "니키 빅: 왜 처음부터 그렇게 말하지 않았어? 네 자존심이나 부끄러움이 나보다 중요했어?",
    "에인슬리 칼헌: 죽여 버렸어야 한다니요? 말 조심하세요! 우리 모두 끔찍하고 무서워도 죽을 만큼 위험을 감수해서 당신이 지금 살아 있는 거예요!",
    "에인슬리 칼헌: 당신은 늘 나에게 화가 나 있군요. 내가 뭘 하든 당신에겐 문제 행동일 거예요, 그리고 난 당신에게 영영 충분할 수 없었을 테고요. 그렇지 않아요? 가브리엘, 내가 가족이고 소중하다면, 내게 윽박지르지 말아요. 날 안아줘요.",
    "에인슬리 칼헌: 그거 알아요? 나는 원래 무척 무모한 여자예요. 나는 결혼하지 않고 애를 가질 정도로 무모했지요. 에이비, 내가 얼마나 무모하냐면, 출산을 4주 앞두고 연고가 하나도 없는 산타 바바라로 날아올 정도였어요. 그러니까, 당신도 익숙해질 때가 됐어요.",
    "에인슬리 칼헌: 이런 말씀을 드리게 되어 몹시 유감이지만, 저는 학교에서 무료 콘돔을 나눠주는 데 반대해요. 이것에 대해서 네 시간 정도의 충분한 토론을 하고 싶으면 저와 얼마든지 논의를 시작해도 좋아요.",
    "*여린 목소리*: 안녕, 샤일로."
    "에인슬리 칼헌: * [격양된 목소리]* 당신들은 비겁자들이에요! 당신들이 찾는 그 반군은 어린애일 뿐이잖아요! 우린—",
    "에인슬리 칼헌: 부끄럽지만 고백할 게 있어요. 나는 완벽하게 조형되고 세공된 유리 성 같은 세상에서 살아왔어요. 모든 게 내 계획대로였어요. 그렇지만 샤일로가 생긴 건 내 계획과 달랐어요. 산타 바바라 근처로 날아가게 된 것도 내 의지가 아니었죠. 하지만 지금 나는 이게 마음에 들어요. 나는 이런 사람이니까 계속 계획을 세울 거고, 어긋날 때마다 마음이 힘들겠죠. 그래도 넘어지는 걸 두려워하지 않도록 날 잡아줘요. 내가 완벽한 나만의 계획 안에 갇혀 있지 않도록요.",
    "에인슬리 칼헌: 다시는, 감히 내게, 그런 식으로 말하지 마세요. ⋯⋯봉사에 감사드려요.",
    "에인슬리 칼헌: 그렇게 크겠죠, 저에게 묻기도 할 거예요. “*엄마, 저 중에 누가 진짜 아빠에요?*”",
    "에인슬리 칼헌: 당신을 들은 대로 판단하지 않을 거예요. 제 말을 믿어요. 그러니 당신도 나를 그저 겉으로 보이는 것만으로 판단하지 않겠다고 약속해 주겠어요?",
    "에인슬리 칼헌: 못생기고 귀여워요.",
    "에인슬리 칼헌: 우리가 전쟁의 한 가운데 있다는 뜻이에요.",
    "에인슬리 칼헌: 가세요. 당신도 나도, 살려야 할 목숨이 있어요.",
    "*[롭의 목소리] ”그럼, 저도 기도 한 번 해볼까요. 대체 왜 우리에게 평화로운 날을 주지 않는거냐고.”* \r **에인슬리 칼헌**: 저는 그 기도의 응답은 이미 들은 것 같아요. ‘Because we don’t deserve it.’",
    "완벽한 팬케이크: 나, *[삑사리]*  나아는⋯ 당신에게 먹히기를 기다리고 있는, 팬케이크예요.",
    "에인슬리 칼헌: 당신은 바다와 사랑에 빠졌군요.",
    "에인슬리 칼헌: 지금이 아니면 물어볼 수 없을 것 같았어요. 당신도 지금이 아니면 말할 기회가 없을지도 몰라요.",
    "에인슬리 칼헌: 이⋯⋯ 보기 드문 디자인은⋯ 정말 보기가 드물어요. ⋯⋯세상에 하나 밖에 없고 정말 특별하네요. ⋯⋯강렬해요.",
    "에인슬리 칼헌: 우리는 끔찍한 사람들이에요. *[고저 없는 목소리]* 이 모든 현실이 닥친 건 우리에게 다른 선택이 없었기 때문이 아니라, 우리 각자가 다 자기 마음대로 했기 때문이에요. 이 세상이 망한 것도요. ⋯⋯대답이 마음에 드시나요?",
    "에인슬리 칼헌: 잘못한 건 아나요? 후회해요? 이제 와서! 그렇다면 살아요. 이를 악물고 죗값을 치러요. 살아서 끝까지 보도록 해요."
    "베티 웰즈: 나는 그냥... 참지 않았을 뿐이야. 지루함이든 걸려오는 시비든.",
    "베티 웰즈: 괜찮아, 저기 성질 드러운 영감탱보다는 훨씬 나아.",
    "베티 웰즈: 어린 아이의 말랑한 볼을 허락 없이 만지는 건 어른만의 특권인 줄 알았는데, 그것도 아닌가봐.",
    "베티 웰즈: 나 아직 식칼 들고 있어.",
    "베티 웰즈: ... 저건 못 들은 걸로 할래. 대답 안해도 되는 거잖아.",
    "베티 웰즈: 철저하게 인과관계를 따져서 뭐하나, 감정적으로 날뛰는 무리에 휩쓸릴텐데.",
    "베티 웰즈: 안 돼, 가지 마... 나 혼자 어떻게 하라고.",
    "베티 웰즈: 조금은 부정해주길 바랐어. 거짓말은 이럴 때 하라고 있는 거야.",
    "베티 웰즈: 당신 같은 사람 붙잡고 애처로운 눈으로 쳐다보고 있으면 하나 던져주더라.",
    "베티 웰즈: 내가 더 잘 싸운다는 걸 증명하기 위해 잭이랑 한바탕 해도 발언 철회 안 해줄 거지?",
    "베티 웰즈: 아, 나는 그쪽 딸 아닌데!",
    "베티 웰즈: 역사 진도 거기까지 안 나갔어? 장갑을 던지면 결투 신청이야.",
    "베티 웰즈: 술이 들어가면 별 거 아닌 것에도 너무 크게 웃는 것 같아.",
    "베티 웰즈: 무릎 꿇리면 무조건 아래가 될 것을..."
    "베티 웰즈: 무슨 소리! 예술은 어디에나 있어. 알아채지 못하는 것 뿐이지."
    "스테파니 루비오: 인간다운게 그러니까...뭔데? 눈앞의 불의와 악을 두고 홀로 선량하며, 목전의 죽음을 두고 초연하고, 불안과 두려움을 앞서 초탈 하며, 감정을 초월하여 결과적으로 탈속한 존재로 거듭나는게 인간다운거예요?",
    "스테파니 루비오: 고해 하세요.",
    "스테파니 루비오: 사람이...어느 정도 위치가 있다면...본인의 신념이나 기분이나, 의지를 표출하기 전에 한 번 더 생각해봐야 한다고 생각해요. 그게 책임감이고…",
    "스테파니 루비오: 밥 해주는 자기라면 우리 집에도 하나 가지고 싶은걸.",
    "스테파니 루비오: 피노키오 였다면 방금 발언으로 코가 3인치 늘었어요.",
    "스테파니 루비오: 원래 닮으면 안맞아요.",
    "스테파니 루비오: …자식 관리 똑바로 하세요.",
    "스테파니 루비오: 나는 그 사람이 어떻게 하면 상처를 받는지, 우는지, 정신이 나가는지 손에 쥔 것 처럼 알 수 있었거든. 그 여자의 절반은 나였으니까.",
    "스테파니 루비오: 애는 믿을 놈 하나 없으면 으레 그렇게 되는 법인데, 기왕 집까지 들였으면 신뢰? 같은 거 좀 줘 봐요. 혹시 쓸데없이 여자 들이거나 할 생각은 아니죠?",
    "스테파니 루비오: 내가 직접 죽이기 싫으니까 남에게 부탁한다고 해서...내가 ‘그렇지 않은 게’ 된다는 어중간한 생각으로 살기엔...대학 나왔어요 저.",
    "스테파니 루비오: 그런 말 하지 마요. 괜히 애처롭게.",
    "로미오 피아프: 당신이 기절하면 이 아이는 이 험난하고 고난가득한 떨거지들 사이에서 살아야 해요!! ",
    "로미오 피아프: 제자 하나 키울 생각 없으세요? 닥터.",
    "로미오 피아프: 간지는 누나가 담당할 테니 귀여움은 동생이 담당해라.",
    "로미오 피아프: 것 봐. 그러니 웃는 거 더 봐요.",
    "로미오 피아프: 코 밑에 레몬즙 발라놔요. 냄새 맡는 게 좀 나을 거예요.",
    "로미오 피아프: 키가 작아도 멋짐과 간지, 그리고 분위기가 있으면 다 작살나는 거야.",
    "로미오 피아프: 좋은 밤, 좋은 꿈. 새벽에 만나게 되면 또 보고.",
    "로미오 피아프: 어우, 실례합니다! 어우, 잠시만요! 사람 지나가요!",
    "로미오 피아프: Almost heaven… West Virginia~ Blue Ridge Mountains, Shenandoah River~",
    "로미오 피아프: 난 로미오 라고 해요. 다시 소개하지만 우린 민간인이고, 이곳엔 살기 위해 왔어요.",
    "로미오 피아프: 흐름을 극단적으로 보내지 마, 내 친구. 거기에 널 떠내려 보내지 마.",
    "로미오 피아프: 오늘 하루라도! 죽은 사람 하나 없게 해달라는  소원이 그렇게나 이뤄주기 힘들었냐, 어!!",
    "로미오 피아프: 아, 내가 사람 살리는 기적도 보여주는데 식재료 살리는 기적도 보여줄 수 있지!! 따악- 기다려 봐!",
    "로미오 피아프: 나도 사람이 좋아서, 그들을 위해서 내 일을 다하려는 거니까요. 그래서 외롭기도 싫고, 남겨지기도 싫어요.",
    "로미오 피아프: …괜찮을 거예요.",
    "로미오 피아프: 닥터 임마누엘은 나라는 기적의 도구를 세상에 남겨두고 갔죠.",
    "로미오 피아프: …난 죽은 사람은 못 살려. 죽은 사람은 못 살린다고.",
    "로미오 피아프: 이건 너를 보호해주는 수단이 될 거야. 내가 그랬던 것처럼."
]

@bot.command(name='RADIO')
async def RADIO(ctx):
    random_radio = random.choice(voices)
    await ctx.reply(random_radio)
    
       
    
# Random paragraph
paragraphs = [
    {"title": "고요한 밤", "content": "밤의 시간이 아주 느리게 흐르는 것 같다. 모든 게 괜찮을 거라는 안도감이 찾아온다. 침묵이 편안하다."},
    {"title": "방문", "content": "당신의 이웃에겐 별 일 없는가? 셋 모두 `!WHO` 를 굴려 나온 사람들의 집을 노크한다. 🌃 나이트 워치가 명령어에서 나온 사람들을 각자 태그해, 노크에 반응해 문을 열어준 사람들은 정신력을 1 회복합니다."},
    {"title": "추위", "content": "캘리포니아의 밤은 때때로 쌀쌀하다. 모닥불을 피우고 땔감이 될 만한 것을 좀 찾아봐야겠다. *[탐색:일반] 판정*\n\n🚦 **둘 이상 실패 경우** — 셋 모두 특수 상태 이상, [감기]를 얻음: 열이 오르고 기침을 자주 한다. [해열제]를 먹지 않으면 24시간 동안 모든 주사위 판정에 -1."},
    {"title": "하이에나", "content": "“이딴 데 뭐가 있다고 그래?” “잔말 말고 와 봐라, 쫌. 이런 데 줏어 먹을 게 쏠쏠하다고.” 대화 소리가 들린다. 불길한 예감을 따르듯이, 낯선 목소리들은 점점 이쪽으로 가까워지고 있다. “야, 꼭 이런 데 인간 있다고!” “쫄았냐? 자고 있을 때 죽여 버리면 돼!” 전리품을 찾으러 돌아다니는, 어리숙한 강도들이다. 🚥 *불침번 셋 모두 [위협:일반]을 하거나, 둘 모두 기습 공격을 시도해 육탄전 또는 사격 [피해량] 합산.*\n\n**둘 모두 위협 성공 —** “야, 튀어! 튀어!” 어둠 속에서 당신들의 살기 어린 목소리를 듣고는 그들은 뒷걸음질치다가 빠른 속도로 도망친다.\n**피해량 합이 25 이상인 경우 —** 죽거나 죽이거나, 우리는 후자를 택한다. 그들은 우리에게 이름 대신에 유용한 무기를 남겼다. [버터플라이 나이프] 피해량 1D6 +3 +(육탄전 기술보정), 세 번 사용하면 날이 부러질 것이다.\n**두 명 이상 위협을 실패했거나, 피해량이 24 이하인 경우 —** “악! XX!” 우리를 뒤늦게 발견하고 깜짝 놀란 그들은, 날붙이를 있는 힘껏 휘두르고 도망친다. *(모두 2D6의 체력을 잃습니다.)*"},
    {"title": "헤드라이트", "content": "자동차 소리가 점점 크게 들린다. 깜깜한 밤 가운데, 어떤 군용 차량의 전조등이 마치 무대 위의 주인공을 찾는 스포트라이트처럼 밝게 빛난다. 그들이 이곳에서 생존자의 흔적을 찾기 전에 숨어야 한다. 🚥 *[은신:일반] 판정.*\n\n**셋 모두 성공한 경우** — 우리가 있는 방향을 잠시 비추던 노란 빛은 금방 다른 곳으로 쏘아진다. 그들은 별다른 것을 찾지 못한다. 자동차 소리가 멀어진다⋯⋯, 그제야 편하게 숨을 쉬며 땀을 닦을 수 있다.\n**하나 이상 은신을 실패한 경우** — 그들이 당신의 움직임을 감지하고 사격한다! *(은신을 실패한 사람은 2D6의 체력을 잃습니다.)* 비명이나 신음을 있는 힘껏 참아야 한다. 그들은 잠시 차를 세우고 주변을 둘러보지만, “가자고, 그냥 망할 들개 새끼였어.” 우리가 숨은 곳을 찾지 못하고 가버릴 것이다."},
    {"title": "감염자", "content": "사람의 성대에서 나오는 기이한 으르렁거림이 귀에 거슬린다. ‘감염자’들이 한쪽 다리를 끌고 주변을 거닐고 있었다. 그것이 우리를 보았다. 그리고 울부짖으며, 우리를 향해 달려오기 시작한다. *육탄전 또는 사격 [피해량] 합산.*\n\n**피해량 합이 25 이상 —** 무사히 감염자를 쓰러뜨린다. 땀조차 흘리지 않은 것 같다.\n**피해량 합이 18 이상 —** 감염자의 이빨이 허공에 딱! 부딪힌다. 간담이 서늘하다. 쓰러뜨리긴 했지만 힘겨웠다. *둘 다 체력 1D6 감소*\n**피해량 합 10 이상 —** 괴력을 가지고 마구 휘두르는 감염자의 손과 그 날카로운 손톱⋯. 녀석이 우리 중 하나를 쓰러뜨리고, 물어뜯으려 하는 순간에 겨우 잡는다. 위험했다. *모두 체력 2D6 감소*\n**피해량 합 10 미만 —** 피를 향해 달려드는 녀석의 송곳니는 빠르고, 우리는 늦었다. 그 일은 순식간에 벌어졌다. 죽음은 어느 날 예고 없이 찾아오는 불청객이었다⋯⋯. *모두 체력 2D6 감소,* **!YN** *을 굴려 N이 나올 경우 감염*"},
    {"title": "유실물", "content": "저 멀리서 물자를 싣고 가던 차가 과속방지턱에 덜컹, 하며 길 위에 뭔가를 흘렸다. 이건⋯⋯.   🚥 *[탐색] 판정.*\n\n**특별 성공(12 이상) —** [소독약과 붕대] 2D6 치료를 가능하게 한다.\n**도전 성공 (10 이상) —** [항생제] 1D6 치료를 가능하게 한다. 추가 체력 +1\n**일반 성공 (8 이상) —** [담배 케이스] 누군가 늘씬한 담배 여섯 개피를 알루미늄 케이스에 예쁘게 담아 놓았다. 한 개피 피울 때마다 정신력 +1 (6/6)\n**실패(8 이하) —** 소스 같은 것을 닦고 버린 냅킨이다. 아니⋯ 피인가? 거리의 청소부가 된 당신에게 감사를."},
    {"title": "은혜의 밤", "content": "두 사람이 지키는 안전한 밤 속에서, 피로를 내려놓고 잠에 든 모든 사람들에게 축복이 임한다. 적어도 두려운 현실보다 나은, 좋은 꿈을 꾸기를.\n\n   **🌃나이트 워치를 제외한 모든 사람들, 이 메세지에 ♥ 이모지로 반응하고 정신력을 1 회복합니다.**"},
    {"title": "평온한 밤", "content": "밤은 두렵지만, 어두울 수록 별은 아름답게 빛나는 법이다. 사위는 조용하고, 밤은 아무 일 없이 흘러 간다. 평화를 누리라."},
    {"title": "밤친구들", "content": "아무 일도 일어나지 않았지만 특별한 밤이 되기도 한다. 좋아하던 영화, 주변 사람들, 취미, 우스웠던 순간⋯ 그런 것들을 밤새워 이야기하며, 그리움과 향수에 젖어든다.\n\n🚥 ’세상이 이렇게 되기 전에 좋아했던 것들’을 화제로 이야기를 나누고, 불침번들이 정신력을 1 회복합니다."}
]

@bot.command(name='NIGHT')
async def random_paragraph(ctx):
    worksheet = await get_member_worksheet(ctx)
    random_p = random.choice(paragraphs)
    embed = discord.Embed(title=random_p["title"], description=random_p["content"], color=discord.Color.green())
    await ctx.reply(embed=embed)

    # Update the value in cell J22 
    current_value = int(worksheet.acell('J22').value)
    new_value = current_value - 2
    worksheet.update('J22', new_value)

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
    print("시트 불러오는 중")
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
async def roll_and_add(ctx, additional_args:str=None):
    print('설득')
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
            if additional_args != None:
                sum_value += add_cal(additional_args)
            
            
            # Reply to the message with the dice roll and the updated total
            reply_content = f"🎲 {dice1}, {dice2}! \r 설득 기술 {cell_value}, 총합 {sum_value}"
            reply_content += success_level(sum_value)
            
            await ctx.reply(reply_content)
        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'Z26' not found in the worksheet.")
            


@bot.command(name='위협')
async def roll_and_add(ctx, additional_args:str=None):
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
            
            if additional_args != None:
                sum_value += add_cal(additional_args)


            reply_content = f"🎲 {dice1}, {dice2}! \r 위협 기술 {cell_value}, 총합 {sum_value}"
            reply_content += success_level(sum_value)
            
            await ctx.reply(reply_content)
        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'Z27' not found in the worksheet.")
            
@bot.command(name='탐색')
async def feel(ctx, additional_args:str=None):
    worksheet = await get_member_worksheet(ctx)
    
    if worksheet is not None:
        try:
            # Roll two six-sided dice
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            
            # Retrieve the current value from cell AK17
            cell_value = int(worksheet.acell('AK17').value)
           
           
            # Calculate the sum of the dice roll and the cell value
            sum_value = cell_value + dice1 + dice2
            
            if additional_args != None:
                sum_value += add_cal(additional_args)

            reply_content = f"🎲 {dice1}, {dice2}! \r 탐색 {cell_value}, 총합 {sum_value}"
            reply_content += success_level(sum_value)
            
            await ctx.reply(reply_content)
            
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'AK17' not found in the worksheet.")

@bot.command(name='통찰')
async def think(ctx, additional_args:str=None):
    worksheet = await get_member_worksheet(ctx)
    
    if worksheet is not None:
        try:
            # Roll two six-sided dice
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            
            # Retrieve the current value from cell AK19
            cell_value = int(worksheet.acell('AK19').value)
            
            # Calculate the sum of the dice roll and the cell value
            sum_value = cell_value + dice1 + dice2
            
            if additional_args != None:
                sum_value += add_cal(additional_args)

            reply_content = f"🎲 {dice1}, {dice2}! \r 통찰 {cell_value}, 총합 {sum_value}"
            reply_content += success_level(sum_value)
            
            await ctx.reply(reply_content)
        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'AK19' not found in the worksheet.")
            
            
@bot.command(name='눈치', )
async def roll_and_add(ctx, additional_args:str=None):
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
            
            if additional_args != None:
                sum_value += add_cal(additional_args)

            reply_content = f"🎲 {dice1}, {dice2}! \r 눈치 기술 {cell_value}, 총합 {sum_value}"
            reply_content += success_level(sum_value)
            
            await ctx.reply(reply_content)
        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'Z28' not found in the worksheet.")
            

@bot.command(name='속임수')
async def roll_and_add(ctx, additional_args:str=None):
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
            
            if additional_args != None:
                sum_value += add_cal(additional_args)

            reply_content = f"🎲 {dice1}, {dice2}! \r 속임수 기술 {cell_value}, 총합 {sum_value}"
            reply_content += success_level(sum_value)
            
            await ctx.reply(reply_content)

        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'Z29' not found in the worksheet.")
            
            
# Command to roll 2D6 dice and add to cell Z30
@bot.command(name='사격')
async def roll_and_add(ctx, additional_args:str=None):
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
            
            if additional_args != None:
                sum_value += add_cal(additional_args)

            
            reply_content = f"🎲 {dice1}, {dice2}! \r 사격 기술 {cell_value}, 총합 {sum_value}"
            reply_content += success_level(sum_value)
            
            await ctx.reply(reply_content)

        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'Z30' not found in the worksheet.")
            
            
# Command to roll 2D6 dice and add to cell Z31
@bot.command(name='육탄전')
async def roll_and_add(ctx, additional_args:str=None):
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
            
            if additional_args != None:
                sum_value += add_cal(additional_args)

            
            reply_content = f"🎲 {dice1}, {dice2}! \r 육탄전 기술 {cell_value}, 총합 {sum_value}"
            reply_content += success_level(sum_value)
            
            await ctx.reply(reply_content)

        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'Z31' not found in the worksheet.")
            
            
# Command to roll 2D6 dice and add to cell Z32
@bot.command(name='무브먼트')
async def roll_and_add(ctx, additional_args:str=None):
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
            
            if additional_args != None:
                sum_value += add_cal(additional_args)

            reply_content = f"🎲 {dice1}, {dice2}! \r 무브먼트 기술 {cell_value}, 총합 {sum_value}"
            reply_content += success_level(sum_value)
            
            await ctx.reply(reply_content)

        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'Z32' not found in the worksheet.")
            
            
# Command to roll 2D6 dice and add to cell Z33
@bot.command(name='은신')
async def roll_and_add(ctx, additional_args:str=None):
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
            
            if additional_args != None:
                sum_value += add_cal(additional_args)

            reply_content = f"🎲 {dice1}, {dice2}! \r 은신 기술 {cell_value}, 총합 {sum_value}"
            reply_content += success_level(sum_value)
            
            await ctx.reply(reply_content)

        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'Z33' not found in the worksheet.")
            
                        
@bot.command(name='손재주')
async def craft(ctx, additional_args:str=None):
    worksheet = await get_member_worksheet(ctx)
    
    if worksheet is not None:
        try:
            # Roll two six-sided dice
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            
            # Retrieve the current value from cell AJ26
            cell_value = int(worksheet.acell('AJ26').value)
            
            # Calculate the sum of the dice roll and the cell value
            sum_value = cell_value + dice1 + dice2
            
            if additional_args != None:
                sum_value += add_cal(additional_args)

            reply_content = f"🎲 {dice1}, {dice2}! \r 손재주 기술 {cell_value}, 총합 {sum_value}"
            reply_content += success_level(sum_value)
            
            await ctx.reply(reply_content)

        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'AJ26' not found in the worksheet.")
            
            
@bot.command(name='치료')
async def heal(ctx, additional_args:str=None):
    worksheet = await get_member_worksheet(ctx)
    
    if worksheet is not None:
        try:
            # Roll two six-sided dice
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            
            # Retrieve the current value from cell AJ27
            cell_value = int(worksheet.acell('AJ27').value)
            
            # Calculate the sum of the dice roll and the cell value
            sum_value = cell_value + dice1 + dice2
            
            if additional_args != None:
                sum_value += add_cal(additional_args)

            reply_content = f"🎲 {dice1}, {dice2}! \r 치료 기술 {cell_value}, 총합 {sum_value}"
            reply_content += success_level(sum_value)
            
            await ctx.reply(reply_content)

        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'AJ27' not found in the worksheet.")
            

@bot.command(name='운전')
async def drive(ctx, additional_args:str=None):
    worksheet = await get_member_worksheet(ctx)
    
    if worksheet is not None:
        try:
            # Roll two six-sided dice
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            
            # Retrieve the current value from cell AJ28
            cell_value = int(worksheet.acell('AJ28').value)
            
            # Calculate the sum of the dice roll and the cell value
            sum_value = cell_value + dice1 + dice2
            
            if additional_args != None:
                sum_value += add_cal(additional_args)

            
            reply_content = f"🎲 {dice1}, {dice2}! \r 운전 기술 {cell_value}, 총합 {sum_value}"
            reply_content += success_level(sum_value)
            
            await ctx.reply(reply_content)
        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'AJ28' not found in the worksheet.")
            
            
@bot.command(name='요리')
async def cook(ctx, additional_args:str=None):
    worksheet = await get_member_worksheet(ctx)
    
    if worksheet is not None:
        try:
            # Roll two six-sided dice
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            
            # Retrieve the current value from cell AJ29
            cell_value = int(worksheet.acell('AJ29').value)
            
            # Calculate the sum of the dice roll and the cell value
            sum_value = cell_value + dice1 + dice2
            
            if additional_args != None:
                sum_value += add_cal(additional_args)

            
            reply_content = f"🎲 {dice1}, {dice2}! \r 요리 기술 {cell_value}, 총합 {sum_value}"
            reply_content += success_level(sum_value)
            
            await ctx.reply(reply_content)
        
        except gspread.exceptions.CellNotFound:
            await ctx.reply("Cell 'AJ29' not found in the worksheet.")
            

@bot.command(name='기계')
async def machina(ctx, additional_args:str=None):
    worksheet = await get_member_worksheet(ctx)
    
    if worksheet is not None:
        try:
            # Roll two six-sided dice
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            
            # Retrieve the current value from cell AJ30
            cell_value = int(worksheet.acell('AJ30').value)
            
            # Calculate the sum of the dice roll and the cell value
            sum_value = cell_value + dice1 + dice2
            
            if additional_args != None:
                sum_value += add_cal(additional_args)

            
            reply_content = f"🎲 {dice1}, {dice2}! \r 기계 기술 {cell_value}, 총합 {sum_value}"
            reply_content += success_level(sum_value)
            
            await ctx.reply(reply_content)
        
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

