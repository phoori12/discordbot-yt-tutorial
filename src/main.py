import discord
from discord.utils import get
from discord.ext import commands
from datetime import datetime, timedelta
from songs import songAPI 

# อันนี้ ไม่ต้องสนใจครับ เป็น library ไว้แอบ token
import os
from dotenv import load_dotenv  # มีไว้แอบ token ครับ 4 บรรทัดนี้ ไม่งั้นเดี๋ยวมันไม่ให้ผมเอาโค้ดลง github
load_dotenv()
token = os.getenv('TOKEN')
#############################################

# wrapper / decorator 

message_lastseen = datetime.now()
message2_lastseen = datetime.now()

bot = commands.Bot(command_prefix='!',help_command=None)

songsInstance = songAPI()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def test(ctx, *, par):
    await ctx.channel.send("You typed {0}".format(par))

@bot.command() 
async def help(ctx):
    # help
    # test
    # send
    emBed = discord.Embed(title="Tutorial Bot help", description="All available bot commands", color=0x42f5a7)
    emBed.add_field(name="help", value="Get help command", inline=False)
    emBed.add_field(name="test", value="Respond message that you've send", inline=False)
    emBed.add_field(name="send", value="Send hello message to user", inline=False)
    emBed.set_thumbnail(url='https://media-exp1.licdn.com/dms/image/C560BAQFHd3L0xFcwcw/company-logo_200_200/0/1550868149376?e=2159024400&v=beta&t=LyKtz-V4W8Gfwzi2ZqmikaI9GcUXI3773_aa3F3nIhg')
    emBed.set_footer(text='test footer', icon_url='https://media-exp1.licdn.com/dms/image/C560BAQFHd3L0xFcwcw/company-logo_200_200/0/1550868149376?e=2159024400&v=beta&t=LyKtz-V4W8Gfwzi2ZqmikaI9GcUXI3773_aa3F3nIhg')
    await ctx.channel.send(embed=emBed)
    
@bot.command()
async def send(ctx):
    print(ctx.channel)
    await ctx.channel.send('Hello')

@bot.event #async/await
async def on_message(message):
    global message_lastseen, message2_lastseen
    if message.content == '!user':
        await message.channel.send(str(message.author.name) + ' Hello')
    elif message.content == 'นายชื่ออะไร' and datetime.now() >= message_lastseen:
        message_lastseen = datetime.now() + timedelta(seconds=5)
        await message.channel.send('ฉันชื่อ ' + str(bot.user.name))
        #logging 
        print('{0} เรียกใช้ นายชื่ออะไร ตอน {1} และจะใช้ได้อีกทีตอน {2}'.format(message.author.name,datetime.now(),message_lastseen))
    elif message.content == 'ผมชื่ออะไร' and datetime.now() >= message2_lastseen:
        message2_lastseen = datetime.now() + timedelta(seconds=5)
        await message.channel.send('นายชื่อ ' + str(message.author.name))
    elif message.content == '!logout':
        await bot.logout()
    await bot.process_commands(message)

@bot.command() 
async def play(ctx,* ,search: str):
    await songsInstance.play(ctx, search)

@bot.command()
async def stop(ctx):
    await songsInstance.stop(ctx)

@bot.command()
async def pause(ctx):
    await songsInstance.pause(ctx)

@bot.command()
async def resume(ctx):
    await songsInstance.resume(ctx)

@bot.command()
async def leave(ctx):
    await songsInstance.leave(ctx)

@bot.command()
async def queueList(ctx):
    await songsInstance.queueList(ctx)

@bot.command()
async def skip(ctx):
    await songsInstance.skip(ctx)
    

bot.run(token)