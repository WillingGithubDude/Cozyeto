import discord
from datetime import datetime
from discord.ext import commands

logchannel = 815379976047296542
logchannel2 = 818020807649394708
joinchannel = 799645293116391425
wordstorychannel = 824503746167177216
botrole = 823071010613362758
msgID = 824502147507945472
msgID2 = 824521761789837332
msgID3 = 848736293072011275
guildID=786436071961395208
quotechannel = 825522469749784587
#----reaction roles---
Notification = 823079511109271582
NSFW = 823079403901681712
Minecraft = 824500410596196392
Singaporean = 873388307147526156
ThirdClass = 823068271765880833
PingMe = 846957184637075517
guild_ids = {
        786436071961395208: {
          873389324081717359: {
            "ping": {
              PingMe
              },
            "⛏️": {
              Minecraft
              },
            "📰": {
              Notification
              },
            "🔞": {
              NSFW
              }
          },
          873402098404978748: {
            "cozyeto": {
              Singaporean,
              ThirdClass
              }
          }
        }
      } #guild -> message -> emoji -> role


class Logging_List(commands.Cog):
    """A list of what gets logged."""

    def __init__(self, bot: commands.bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(joinchannel)
        if member.id != 798974970801815552:
          await channel.send(f"Welcome to the server {member.mention} <:cozyeto:821564618577149982>!")
        embed= discord.Embed(title= "Member joined", description=f"{member} joined the server!", colour=discord.Colour.teal(), timestamp=datetime.now())
        embed.set_footer(text=member.id)
        embed.set_author(name=member, icon_url= member.avatar_url)
        await self.bot.get_channel(logchannel).send(embed=embed)
  


    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
      if member.id != 798974970801815552:
        await self.bot.get_channel(joinchannel).send(f"{member.mention} has left the server... <:cozyluna:821565371865366570>")
      embed= discord.Embed(title=f"{member} left the server!", description=" ", colour=discord.Colour.dark_orange(),
      timestamp=datetime.now())
      embed.set_footer(text=member.id)
      embed.set_author(name=member, icon_url= member.avatar_url)
      await self.bot.get_channel(logchannel).send(embed=embed)
#823081523544195073 or 

    @commands.Cog.listener()
    async def on_message(self, message):
      if message.channel.id == quotechannel:
        if not message.attachments:
          await message.delete()
      if isinstance(message.channel, discord.abc.GuildChannel):
        if message.channel.category:
          if message.channel.category.id not in [823077495049420810, 823081523544195073]:
            if "fag" in message.content:
              try:
                await message.author.send("You have been kicked from Singapore: Slur usage")
              except:
                pass
              await message.author.kick(reason="slur")


    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
      message=message_after
      mainchannel = self.bot.get_channel(wordstorychannel)
      role = message.guild.get_role(botrole)
      if message.channel==mainchannel:
        if " " in message.content or "\n" in message.content:
          await message.delete()
      if role not in message.author.roles:
        embed=discord.Embed(title='Message edited!', description= f"**Before:** \n {message_before.content} \n **After:** \n {message.content}", colour=discord.Colour.orange(), timestamp=datetime.now())
        embed.add_field(name="In: ", value=str(message_before.channel.mention), inline=True)
        embed.set_footer(text=message.author.id)
        embed.set_author(name=message.author, icon_url=message.author.avatar_url)
        await self.bot.get_channel(logchannel2).send(embed=embed)
    

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        logging = self.bot.get_channel(logchannel2)
        logging2 = self.bot.get_channel(863627945049849856)
        betterlog = self.bot.get_channel(863628589257064448)
        embed=discord.Embed(title='Message deleted', description=str(message.content), colour=discord.Colour.blue(), timestamp=datetime.now())
        embed.add_field(name="In: ", value=str(message.channel.mention), inline=True)
        embed.set_footer(text=message.author.id)
        embed.set_author(name=message.author,icon_url=message.author.avatar_url)
        if message.attachments:
          embed.add_field(name = "Attachments: ", value=str(message.attachments), inline=False)
          files = []
          await betterlog.send(embed=embed)
          for attachment in message.attachments:
            image = await attachment.to_file()
            files.append(image)
            await betterlog.send(file=image)
          if message.guild.id != 843624966174933029:
            await logging.send(embed=embed, files=files)
        if message.embeds:
          embeds=[]
          for embed1 in message.embeds:
            embeds.append(f"Title: {embed1.title}\nDescription: {embed1.description}")
          embeds="\n".join(embeds)
          embed.add_field(name="Embeds", value=embeds, inline=False)
        if message.guild.id != 843624966174933029:
          await logging.send(embed=embed)
        await logging2.send(embed=embed)



    @commands.Cog.listener()
    async def on_user_update(self, before, after):
      logs=self.bot.get_channel(logchannel)
      if before.avatar != after.avatar:
        embed=discord.Embed(title=f"Avatar updated", description="**Before**:" ,colour=discord.Colour.blurple())
        embed.set_author(name=after, icon_url=after.avatar_url)
        embed.set_image(url=before.avatar_url)
        await logs.send(embed=embed)
        embed2=discord.Embed(title=" ", description="**After**:" ,colour=discord.Colour.blurple(), timestamp=datetime.now())
        embed2.set_image(url=after.avatar_url)
        embed2.set_footer(text=after.id)
        await logs.send(embed=embed2)
      if before.name + before.discriminator != after.name + after.discriminator:
        embed=discord.Embed(title=f"Username updated", description=f"**Before**: {before.name}#{before.discriminator}\n**After**: {after.name}#{after.discriminator}" ,colour=discord.Colour.blurple(), timestamp=datetime.now())
        embed.set_author(name=after, icon_url=after.avatar_url)
        embed.set_footer(text=after.id)
        await logs.send(embed=embed)


    @commands.Cog.listener()
    async def on_member_update(self, before, after):
      logs=self.bot.get_channel(logchannel)
      if before.nick != after.nick:
        embed=discord.Embed(title=f"Nickname updated", description=f"**Before**: {before.nick}\n**After**: {after.nick}" ,colour=discord.Colour.blurple(), timestamp=datetime.now())
        embed.set_author(name=after, icon_url=after.avatar_url)
        embed.set_footer(text=after.id)
        await logs.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
      for guild_id in guild_ids:
        if payload.guild_id == guild_id:
          for message_id in guild_ids[guild_id]:
            if payload.message_id == message_id:
              for emoji in guild_ids[guild_id][message_id]:
                if payload.emoji.name == emoji:
                  guild = self.bot.get_guild(guild_id)
                  roles = {guild.get_role(role) for role in guild_ids[guild_id][message_id][emoji]}
                  return await payload.member.add_roles(*roles)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
      for guild_id in guild_ids:
        if payload.guild_id == guild_id:
          for message_id in guild_ids[guild_id]:
            if payload.message_id == message_id:
              for emoji in guild_ids[guild_id][message_id]:
                if payload.emoji.name == emoji:
                  guild = self.bot.get_guild(guild_id)
                  roles = {guild.get_role(role) for role in guild_ids[guild_id][message_id][emoji]}
                  member = guild.get_member(payload.user_id)
                  return await member.remove_roles(*roles)



#----------------------------------------------------------------
#------------------------END COG HERE----------------------------
#----------------------------------------------------------------


def setup(bot: commands.Bot):
    bot.add_cog(Logging_List(bot))