from random import choice, randint
from typing import Optional

from aiohttp import request
from discord import Member, Embed
from discord.ext.commands import command, Cog, BadArgument, cooldown, BucketType

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @command(name="hello", aliases=["hi", "Hello", "Hi"]) #aliases=["command", "c"], hidden=True) #name of the command, other names for the commands, if hidden from the help command
    async def say_hello(self, ctx):
        """Says Hello"""
        await ctx.send(f"{choice(('Hello', 'Hi', 'Hey'))} {ctx.author.mention}!") #reacts to "+hello"
        
    @command(name="dice", aliases=["roll"])
    #@cooldown(1, 30, BucketType.user) #1 is times till cooldown 30 is time in secounde cooldown for a user
    async def roll_dice(self, ctx, die_string: str):
        """Rolls Dice"""
        dice, value = (int (term) for term in die_string.split("d"))
        
        if dice <= 25:
            rolls = [randint(1, value) for i in range(dice)]
            
            await ctx.send(" + ".join([str(r) for r in rolls]) + f" = {sum(rolls)}")
        
        else:
            await ctx.send("I can't roll that many dice, try a lower number")
        
    @command(name="slap", aliases=["hit"])
    async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = ("being a twat")):
        """Slaps your friends"""
        await ctx.send(f"{ctx.author.display_name} slapped {member.mention} for {reason}!")
        
    @slap_member.error
    async def slap_member_error(self, ctx, exc):
        if isinstance(exc, BadArgument):
            await ctx.send("I can't find the member.")
        
    @command(name="echo", aliases=["same"])
    @cooldown(1, 15, BucketType.guild)
    async def echo_message(self, ctx, *, message):
        """Says what you want"""
        await ctx.message.delete()
        await ctx.send(message)
        
    @command(name="fact")
    #@cooldown(3, 60, BucketType.guild)
    async def animal_fact(self, ctx, animal: str):
        """Gives you an Animal Fact"""
        if  (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala"):
            fact_url = f"https://some-random-api.ml/facts/{animal}"
            image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"
            
            async with request("GET", image_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    image_link = data["link"]
                    
                else:
                    image_link = None
            
            async with request("GET", fact_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    embed = Embed(title=f"{animal.title()} fact",
                                  description=data["fact"],
                                  color=ctx.author.color)
                    if image_link is not None:
                        embed.set_image(url=image_link)
                    
                    await ctx.send(embed=embed)
                    
                else:
                    await ctx.send(f"API returned a {response.status} status.")
         
        else: 
            await ctx.send("No facts are availble for that animal.")
        
    @Cog.listener()
    async def on_ready(self): # When ready it will do this 
        #await self.bot.stdout.send("Fun cog ready")
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Fun")
     
def setup(bot):
    bot.add_cog(Fun(bot))