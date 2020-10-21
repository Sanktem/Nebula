from typing import Optional
from random import choice

from aiohttp import request
from discord import Member, Embed
from discord.ext.commands import command, Cog, BadArgument, cooldown, BucketType

class Not_In_Vid(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @command(name="meme", aliases=["Meme"])
    async def post_meme(self, ctx):
        meme_url = "https://some-random-api.ml/meme"
        async with request("GET", meme_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                meme_image = data["image"]
                meme_caption = data["caption"]
                
                embed = Embed(title=f"{meme_caption.title()}", color=ctx.author.color)
                embed.set_image(url=meme_image)
                
                await ctx.send(embed=embed)
            
            else:
                await ctx.send("No meme found")

    @command(name="fuck", aliases=["Fuck"])
    @cooldown(1, 15, BucketType.guild)
    async def fuck(self, ctx):
        """Tells someone to fuck off"""
        the_fucked = choice(ctx.channel.guild.members)
        await ctx.send(f"{ctx.author.display_name} says 'Fuck you' to {the_fucked.mention}")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Not_In_Vid")

def setup(bot):
    bot.add_cog(Not_In_Vid(bot))