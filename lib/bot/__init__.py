#imports
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown)
from discord.ext.commands import Context
from discord import Embed, File
from discord.errors import HTTPException, Forbidden
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from asyncio import sleep
from glob import glob
from datetime import datetime

from ..db import db

# Things that will stay the same
PREFIX = "+"
OWNER_IDS = [292106118031736832]
COGS = [path.split("/")[-1][:-3] for path in glob("./lib/cogs/*.py")] #Makes a list of all the files in ./lib/cogs
#change ("\\") to ("/") for linux
INGORE_EXCEPTIONS = (CommandNotFound, BadArgument)

class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)
            
    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f" {cog} cog ready")
    
    def all_ready(self):
        return all ([getattr(self, cog) for cog in COGS])

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.cogs_ready = Ready()
        
        self.guild = None
        self.scheduler = AsyncIOScheduler()
        
        db.autosave(self.scheduler)
        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS)
        
    def setup(self): #setting up all of the cogs and saying they are ready
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f" {cog} Cog Loaded")
            
        print("Setup Complete")
        
    def run(self): # This will run in cmd when the bot is ran
        #self.VERSION = version
        
        print("Running setup...")
        self.setup()
        
        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN =tf.read()
        
        print("Running bot...")
        super().run(self.TOKEN, reconnect=True)
    
    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)
        
        if ctx.command is not None and ctx.guild is not None:
            if self.ready:
                    await self.invoke(ctx)
                    
            else:
                await ctx.send("I'm not ready to recieve commands. Please wait a few seconds.")
            
    
    async def amongus_game(self): #Creates the timed message
        await self.stdout.send("@everyone Let's play Among Us you fucks... ")
        
    
    async def on_connect(self): #Lets you know the bot is connected
        print("Bot Connected")
    
    async def on_disconnect(self):
        print("Bot Disconnected")
        
    async def on_error(self, err, *args, **kwargs): #Error handling
        if err == "on_command_error":
            await args[0].send("Somthing went wrong.")
        
        await self.stdout.send("An error has occured!") #intro message
        raise
        
    async def on_command_error(self,ctx, exc): #On command error handling
        if isinstance(exc, CommandNotFound):
            pass
            
        elif any([isinstance(exc, error) for error in INGORE_EXCEPTIONS]):
            pass
            
        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("One or more required arguments are missing.")
        
        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(f"That command is on {str(exc.cooldown.type).split('.')[-1]} cooldown. Try again in {exc.retry_after:,.2f} sec.")
        
        elif hasattr(exc, "original"):
            # if isinstance(exc.original, HTTPException):
                # await ctx.send("Unable to send Message.")
                
            if isinstance(exc.original, Forbidden):
                await ctx.sendd("I do not have permission to do that.")
            
            else:
                raise exc.original
        else:
            raise exc
    
    async def on_ready(self): #When the bot comes online it will create a message
        if not self.ready:
            self.guild = self.get_guild(615291969874296945) #this is the server ID for the friend server
            #self.stdout = self.get_channel(766485670091948052) #This is the test channel
            self.stdout = self.get_channel(615291969886879977) #This is the genral channel
            self.scheduler.add_job(self.amongus_game, CronTrigger(day_of_week=6, hour=14, minute=55, second=0)) # how to set a timed message
            self.scheduler.start()
        
            #channel = self.get_channel(766485670091948052) #This is the channel ID
            #await channel.send("Now Online!") #intro message
            
            embed = Embed(title="Nebula is now online!", colour=0x952ea3, timestamp=datetime.utcnow()) #Creates an embed for the intro message can also add decription
            embed.set_author(name="Nebula", icon_url=self.guild.icon_url) #addes the server icon, and my name to the embed
            #embed.set_footer(text="This is a footer!") #Sets a footer
            #embed.set_thumbnail(url=self.guild.icon_url) #adding an HTML as a thumbnail
            #embed.set_image(url=self.guild.icon_url) #adding an HTML image to the embed
            await self.stdout.send(embed = embed) #sends the message
            
            #await channel.send(file=File("./data/images/amongus.jpg")) #this is the command for sending files
            
            while not self.cogs_ready.all_ready():
                await sleep(0.5)
            
            self.ready = True
            print("Bot Ready") #lets you know that the bot is ready
            
        else:
            print("Bot Reconnected")
        
    async def on_message(self, message):
        if not message.author.bot: 
            await self.process_commands(message)
        
    
bot = Bot()