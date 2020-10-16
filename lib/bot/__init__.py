from discord.ext.commands import Bot as BotBase
from discord import Embed
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

PREFIX = "+"
OWNER_IDS = [292106118031736832]

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        #self.guild = None
        self.scheduler = AsyncIOScheduler()
        
        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS)
        
    def run(self):
        #self.VERSION = version
        
        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN =tf.read()
        
        print("Running bot...")
        super().run(self.TOKEN, reconnect=True)
    
    async def on_connect(self):
        print("Bot Connected")
    
    async def on_disconnect(self):
        print("Bot Disconnected")
    
    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(615291969874296945)
            print("Bot Ready")
        
            channel = self.get_channel(766485670091948052)
            await channel.send("Now Online!")
            
            embed = Embed(title="Now Online!", description="Nebula is now online.", colour=0xFF0000, timestamp=datetime.utcnow())
            #for name, value, inline in fields:                        
            #embed.add_field(name=name, value=value, inline=inline)
            embed.set_author(name="Sanktem", icon_url=self.guild.icon_url)
            embed.set_footer(text="This is a footer!")
            await channel.send(embed = embed)
            
            
            
        else:
            print("Bot Reconnected")
    
    async def on_message(self, message):
        pass
    
bot = Bot()