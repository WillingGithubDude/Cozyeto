import discord
import time
import datetime
import os
import pymongo
from discord.utils import get
from discord.ext import commands
from discord import File
from datetime import datetime, timedelta

logchannel = 815379976047296542
guildID=786436071961395208
mailcategory=831691345894703144

cluster = pymongo.MongoClient(os.environ['Mongo-DB-secret'])
db = cluster["discord"]
black_list = db["blacklist"]


async def get_user(member):
  user = black_list.find_one({"_id": member.id})
  if user == None:
    black_list.insert_one({"_id": member.id, "blacklist": False})
    user = black_list.find_one({"_id": member.id})
  return user


class ModMail(commands.Cog):
    """A list of mail commands"""

    def __init__(self, bot: commands.bot):
        self.bot = bot


    @commands.command(name="blacklist", description="Blacklists a user")
    @commands.has_permissions(kick_members=True)
    async def blacklist(self, ctx, member: discord.Member):
        user = await get_user(member)
        if user["blacklist"] == False:
          black_list.delete_one(user)
          black_list.insert_one({"_id": member.id, "blacklist": True})
          await ctx.send(f"{member} has been blacklisted")
        else:
          await ctx.send("The person is already blacklisted")

    @commands.command(name="whitelist", description="Whitelists a user")
    @commands.has_permissions(kick_members=True)
    async def whitelist(self, ctx, member:discord.Member):
        user = await get_user(member)
        if user["blacklist"] == True:
          black_list.delete_one(user)
          black_list.insert_one({"_id": member.id, "blacklist": False})
          await ctx.send(f"{member} has been whitelisted")
        else:
          await ctx.send("That user is already whitelisted")


    @commands.command(name="viewblacklist", description="Shows the list of blacklisted members")
    @commands.has_permissions(kick_members=True)
    async def viewblacklist(self, ctx):
      blacklist=[]
      for result in black_list.find():
        if result["blacklist"] == True:
          blacklist.append(f"<@!{result['_id']}>")
      embed = discord.Embed(title="Blacklisted users", description="\n".join(blacklist),colour=discord.Colour.blue(), timestamp=datetime.now())
      await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_message(self, message):
      guild = self.bot.get_guild(guildID)
      category = discord.utils.get(guild.categories, id=mailcategory)
      global log
      log=discord.utils.get(guild.channels, id=logchannel)
      overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=False)}

      if str(message.channel.type) == "private":
        if message.author != self.bot.user:
          if await get_user(message.author)["blacklist"] == True:
            await message.author.send(f"You are blacklisted from this guild")
          else:
            c=None
            for channel in category.channels:
              if channel.topic==f"{message.author.id}":
                  c=channel.topic
                  break
            if c==None:
                channel = await guild.create_text_channel(name=f"{message.author.name}-{message.author.discriminator}", category=category, overwrite=overwrites, topic=f"{message.author.id}")

            embed= discord.Embed(title=f"New message", description= message.content,colour=discord.Colour.red(), timestamp=datetime.now())
            embed.set_author(name=message.author, icon_url=message.author.avatar_url)
            embed.set_footer(text=message.author.id, icon_url=self.bot.user.avatar_url)
            await channel.send(embed=embed)

            embed2=discord.Embed(title=f"Message sent", description= message.content,colour=discord.Colour.green(), timestamp=datetime.now())
            embed2.set_author(name=message.author, icon_url=message.author.avatar_url)
            embed2.set_footer(text=message.author.id, icon_url=self.bot.user.avatar_url)
            await message.author.send(embed=embed2)


      elif message.channel.category==category:
        if message.author != self.bot.user:
          person=message.guild.get_member(int(message.channel.topic))
          if person == None:
            return await message.channel.send("Member not found")
          
          ctx = await self.bot.get_context(message)
          if ctx.valid == False and message.content.startswith("=") == False:
            try:
              embed=discord.Embed(title=f"Message sent", description= message.content,colour=discord.Colour.green(), timestamp=datetime.now())
              embed.set_author(name=message.author, icon_url=message.author.avatar_url)
              embed.set_footer(text=person.id, icon_url=self.bot.user.avatar_url)

              embed2=discord.Embed(title="New message", description= message.content,colour=discord.Colour.red(), timestamp=datetime.now())
              embed2.set_author(name=message.author, icon_url=message.author.avatar_url)
              embed2.set_footer(text=person.id, icon_url=self.bot.user.avatar_url)
              try:
                await person.send(embed=embed2)
                await message.channel.send(embed=embed)
                await message.delete()
              except:
                await message.channel.send('That user has DMs disabled!')
            except:
              await message.channel.send("User not found")


    @commands.command(name="close", description="Closes a ticket")
    @commands.has_permissions(kick_members=True)
    async def close(self, ctx, *, reason="No reason provided"):
      logs=self.bot.get_channel(logchannel)
      if ctx.channel.category.id == mailcategory:
          user= ctx.guild.get_member(int(ctx.channel.topic))
          await ctx.send("Closing...")
          logcontent=[]
          async for message in ctx.channel.history(limit=None, oldest_first=True):
              for embed in message.embeds:
                logcontent.append(f'__**{embed.title}**__ by {embed.author.name}: {embed.description}\n{embed.timestamp.strftime("%m/%d/%Y, %H:%M %p")}')
          logcontent.append(f'__**Ticket Closed**__ by {ctx.author}: {reason}\n{time.strftime("%m/%d/%Y, %H:%M %p")}')
          log="\n".join(logcontent)
          try:
            embed2=discord.Embed(title="Ticket closed", description= reason,colour=discord.Colour.dark_red(), timestamp=datetime.now())
            embed2.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            embed2.set_footer(text=user.id, icon_url=self.bot.user.avatar_url)
            await user.send(embed=embed2)
          except:
            pass
          
          embed3=discord.Embed(title="Ticket closed", description=log, timestamp=datetime.now())
          if len(embed3) < 2048:
              await logs.send(embed=embed3)
          else:
              filename=f"{user}.txt"
              with open(filename, 'w') as f:
                f.write(f"Ticket logs for {user}:\n{log}")
              await logs.send(file=File(filename))
              os.remove(filename)

          await ctx.channel.delete()


    @commands.command(name="aclose", description="Closes a ticket anonymously", usage="eto aclose (reason)")
    @commands.has_permissions(kick_members=True)
    async def aclose(self, ctx, *, reason="No reason provided"):
      logs=self.bot.get_channel(logchannel)
      if ctx.channel.category.id == mailcategory:
          user=get(ctx.guild.members, id=int(ctx.channel.topic))
          await ctx.send("Closing...")
          logcontent=[]
          async for message in ctx.channel.history(limit=None, oldest_first=True):
              for embed in message.embeds:
                logcontent.append(f'__**{embed.title}**__ by {embed.author.name}: {embed.description}\n{embed.timestamp.strftime("%m/%d/%Y, %H:%M %p")}')
          logcontent.append(f'__**Ticket Closed (anonymous)**__ by {ctx.author}: {reason}\n{time.strftime("%m/%d/%Y, %H:%M %p")}')
          log="\n".join(logcontent)
          try:
            embed=discord.Embed(title="Ticket closed", description= reason,colour=discord.Colour.dark_purple(), timestamp=datetime.now())
            embed.set_author(name="Anonymous#0000", icon_url="https://s3.amazonaws.com/appforest_uf/f1493101482859x646389236906543400/YeVk_bj_.jpg")
            embed.set_footer(text=user.id, icon_url=self.bot.user.avatar_url)
            await user.send(embed=embed)
          except:
            pass

          embed3=discord.Embed(title="Ticket closed", description=log, timestamp=datetime.now())
          if len(embed3) < 2048:
              await logs.send(embed=embed3)
          else:
              filename=f"{user}.txt"
              with open(filename, 'w') as f:
                f.write(f"Ticket logs for {user}:\n{log}")
              await logs.send(file=File(filename))
              os.remove(filename)
          await ctx.channel.delete()


    @commands.command(name="areply", description="Sends an anonymous reply", usage="eto areply (message)")
    @commands.has_permissions(kick_members=True)
    async def areply(self, ctx, *, message=None):
        if ctx.channel.category.id == mailcategory:
          if message==None:
            await ctx.message.delete()
            await ctx.send("You need to provide a message", delete_after=5)
          else:
            user=get(ctx.guild.members, id=int(ctx.channel.topic))

            try:
              embed=discord.Embed(title=f"Message sent (anonymous)", description= message, colour=discord.Colour.dark_purple(), timestamp=datetime.now())
              embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
              embed.set_footer(text=user.id, icon_url=self.bot.user.avatar_url)

              embed2=discord.Embed(title="New message", description= message,colour=discord.Colour.dark_purple(), timestamp=datetime.now())
              embed2.set_author(name="Anonymous#0000", icon_url="https://s3.amazonaws.com/appforest_uf/f1493101482859x646389236906543400/YeVk_bj_.jpg")
              embed2.set_footer(text=user.id, icon_url=self.bot.user.avatar_url)
              try:
                await user.send(embed=embed2)
                await ctx.send(embed=embed)
                await ctx.message.delete()
              except:
                await ctx.send('That user has DMs disabled!')
            except:
              await ctx.send("User not found")


#---------------------------------------------------------------------
#---------------------------END COG HERE------------------------------
#---------------------------------------------------------------------


def setup(bot: commands.Bot):
    bot.add_cog(ModMail(bot))