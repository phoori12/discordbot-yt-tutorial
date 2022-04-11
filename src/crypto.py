import os
import asyncio
import discord
from discord.utils import get
from binance.spot import Spot
from dotenv import load_dotenv  # มีไว้แอบ token ครับ 4 บรรทัดนี้ ไม่งั้นเดี๋ยวมันไม่ให้ผมเอาโค้ดลง github
load_dotenv()
api_key = os.getenv('APIKEY')
api_sec = os.getenv('API_SECRET')
binanceClient = Spot(key=api_key, secret=api_sec)

class crpytoAlertAPI:
    def __init__(self, bot):
        self.bot = bot
        self.alerts = []
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.loopCheck())    

    def getPrice(self, currency): # btc => BTCUSDT jkashdffaUSDT
        currency = str(currency).upper() + "USDT"
        try:
            price = binanceClient.ticker_price(currency)
        except Exception:
            return -999
        
        return price

    async def setAlert(self, ctx, currency, price):
        curr_price = self.getPrice(currency)
        if curr_price == -999:
            await ctx.channel.send("Pair not found")
            return 0
        self.alerts.append([ctx.guild.id,ctx.channel.id,currency,price])
        #print(self.alerts)

    async def showAlerts(self, ctx):
        allAlerts = "``` Alerts! \n"
        for i in range(len(self.alerts)):
                if self.alerts[i][0] == ctx.guild.id:
                    allAlerts += f"==> {self.alerts[i][2]} at {self.alerts[i][3]}\n"
        await ctx.channel.send(allAlerts + "```")            
       
    async def loopCheck(self):
        while True:
            if self.alerts:
                for i in range(len(self.alerts)):
                    temp_price = self.getPrice(self.alerts[i][2])["price"]
                    #print(f"{float(self.alerts[i][3])}, {float(temp_price)}")
                    if float(temp_price) >= float(self.alerts[i][3]):
                        #print(f"{self.alerts[i][2]} reach threshold")
                        await self.sendGuildMessage(self.alerts[i])
                        self.alerts.pop(i)
                        #print(self.alerts)
            await asyncio.sleep(1)

    async def sendGuildMessage(self, alerts):
        custom_guild = discord.utils.get(self.bot.guilds, id=alerts[0])
        custom_channel = discord.utils.get(custom_guild.channels, id=alerts[1])
        await custom_channel.send(f'```ini\n[{alerts[2]} has reached {alerts[3]}$!!!]\n```') 






