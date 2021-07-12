import discord
import json
from datetime import datetime
from discord.utils import get
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
Singaporian = 823059666925518868
ThirdClass = 823068271765880833
PingMe = 846957184637075517


async def update_invites(guild):
  with open ("data/invites.json") as f:
    data = json.load(f)
  invite_list = await guild.invites()
  for invite in invite_list:
    data[str(invite.code)] = invite.uses
  with open ("data/invites.json", "w") as f:
    json.dump(data, f)


class Logging_List(commands.Cog):
    """A list of what gets logged."""

    def __init__(self, bot: commands.bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_invite_create(self, invite):
      await update_invites(invite.guild)


    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(joinchannel)
        guild = member.guild
        if member.id != 798974970801815552:
          await channel.send(f"Welcome to the server {member.mention} <:cozyeto:821564618577149982>!")
        with open("data/invites.json") as f:
          data = json.load(f)
        for old_invite in data:
          new_invite = await self.bot.fetch_invite(url = f"discord.gg/{old_invite}")
          if old_invite in await guild.invites():
            if data[old_invite] < new_invite.uses:
              code = old_invite
              break
          else:
            code = old_invite
            break
        embed= discord.Embed(title= f"{member} joined the server!", description=f"Invited by {new_invite.inviter.mention} with discord.gg/{code}", colour=discord.Colour.teal(), timestamp=datetime.now())
        embed.set_footer(text=member.id)
        embed.set_author(name=member, icon_url= member.avatar_url)
        await self.bot.get_channel(logchannel).send(embed=embed)
        await update_invites(guild)
  


    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
      if member.id != 798974970801815552:
        await self.bot.get_channel(joinchannel).send(f"{member.mention} has left the server... <:cozyluna:821565371865366570>")
      embed= discord.Embed(title=f"{member} left the server!", description=" ", colour=discord.Colour.dark_orange(),
      timestamp=datetime.now())
      embed.set_footer(text=member.id)
      embed.set_author(name=member, icon_url= member.avatar_url)   
      await self.bot.get_channel(logchannel).send(embed=embed)
      await update_invites(member.guild)
#823081523544195073 or 


    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
      if before.category.id == 863978081697267732:
        for obj in after.overwrites:
          perms = after.overwrites_for(obj)
          if perms.mention_everyone != False:
            perms.mention_everyone = False
            await after.set_permissions(obj, overwrite=perms)
          if perms.create_instant_invite != False:
            perms.mention_everyone = False
            await after.set_permissions(obj, overwrite=perms)

    @commands.Cog.listener()
    async def on_message(self, message):
      if message.channel.id == quotechannel:
        if not message.attachments:
          await message.delete()
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
          await logging.send(embed=embed, files=files)
        if message.embeds:
          embeds=[]
          for embed1 in message.embeds:
            embeds.append(f"Title: {embed1.title}\nDescription: {embed1.description}")
          embeds="\n".join(embeds)
          embed.add_field(name="Embeds", value=embeds, inline=False)
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
      if before.name != after.name:
        embed=discord.Embed(title=f"Username updated", description=f"**Before**: {before.name}#{before.discriminator}\n**After**: {after.name}#{after.discriminator}" ,colour=discord.Colour.blurple(), timestamp=datetime.now())
        embed.set_author(name=after, icon_url=after.avatar_url)
        embed.set_footer(text=after.id)
        await logs.send(embed=embed)
      if before.discriminator != after.discriminator:
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
    async def on_raw_reaction_add(self, payload=None):
        guild = discord.utils.get(self.bot.guilds, id=guildID)
        role = guild.get_role(Notification)
        role2 = guild.get_role(NSFW)
        role3 = guild.get_role(Minecraft)
        role4 = guild.get_role(PingMe)
        singaporian = guild.get_role(Singaporian)
        thirdclass = guild.get_role(ThirdClass)
        if payload is not None:
            if payload.message_id==msgID:
                if str(payload.emoji)=="<:cozyluna:786789373735469066>":
                    await payload.member.add_roles(role)
                elif str(payload.emoji)=="<:cozyeto:786789349253447690>":
                    await payload.member.add_roles(role2)
                elif str(payload.emoji) =="<:uncozyeto:805915542702653440>":
                    await payload.member.add_roles(role3)
            if payload.message_id==msgID2:
                if str(payload.emoji)=="<:cozyeto:786789349253447690>":
                    await payload.member.add_roles(singaporian)
                    await payload.member.add_roles(thirdclass)
            elif payload.message_id==msgID3:
              await payload.member.add_roles(role4)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload=None):
        guild = discord.utils.get(self.bot.guilds, id=guildID)
        role = guild.get_role(Notification)
        role2 = guild.get_role(NSFW)
        role3= guild.get_role(Minecraft)
        role4 = guild.get_role(PingMe)
        user = get(guild.members, id=payload.user_id)
        if payload is not None:
            if payload.message_id == msgID:
                if str(payload.emoji)=="<:cozyluna:821565371865366570>":
                    await user.remove_roles(role)
                elif str(payload.emoji)=="<:cozyeto:821564618577149982>":
                    await user.remove_roles(role2)
                elif str(payload.emoji) =="<:uncozyeto:805915542702653440>":
                    await user.remove_roles(role3)
            elif payload.message_id == msgID3:
                await user.remove_roles(role4)



#---------------------------------------------------------------------
#---------------------------END COG HERE------------------------------
#---------------------------------------------------------------------


def setup(bot: commands.Bot):
    bot.add_cog(Logging_List(bot))