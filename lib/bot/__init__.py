#imports
from discord.ext.commands import Bot as BotBase
from discord import Embed, File
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

# Things that will stay the same
PREFIX = "+"
OWNER_IDS = [292106118031736832]

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        #self.guild = None
        self.scheduler = AsyncIOScheduler()
        
        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS)
        
    def run(self): # This will run in cmd when the bot is ran
        #self.VERSION = version
        
        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN =tf.read()
        
        print("Running bot...")
        super().run(self.TOKEN, reconnect=True)
    
    async def on_connect(self): #Lets you know the bot is connected
        print("Bot Connected")
    
    async def on_disconnect(self):
        print("Bot Disconnected")
    
    async def on_ready(self): #When the bot comes online it will create a message
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(615291969874296945) #this is the server ID for the friend server
            print("Bot Ready") #lets you know that the bot is ready
        
            channel = self.get_channel(766485670091948052) #This is the channel ID
            #await channel.send("Now Online!") #intro message
            
            embed = Embed(title="Nebula is now online!", colour=0x952ea3, timestamp=datetime.utcnow()) #Creates an embed for the intro message can also add decription
            embed.set_author(name="Nebula", icon_url=self.guild.icon_url) #addes the server icon, and my name to the embed
            #embed.set_footer(text="This is a footer!") #Sets a footer
            #embed.set_thumbnail(url=self.guild.icon_url) #adding an HTML as a thumbnail
            #embed.set_image(url=self.guild.icon_url) #adding an HTML image to the embed
            await channel.send(embed = embed) #sends the message
            
            #await channel.send(file=File("./data/images/amongus.jpg")) #this is the command for sending files
            
        else:
            print("Bot Reconnected")
    
    async def on_message(self, message):
        pass
    
bot = Bot()