import os
import asyncio
import discord
import time
import random
import datetime
import re
import json
from PIL import Image
from io import BytesIO
from discord import File
from discord.ext import commands
from datetime import timedelta, datetime


permissions_error = 'You are not allowed to use this command!'

logchannel = 815379976047296542
botchannel = 798771440660906005
wordstorychannel = 824503746167177216
cozyetomailID = 831691345894703144
airline_ping = 835378894785609749
mutedrole = 'Muted'


class Moderation(commands.Cog):
    """A list of commands for moderation"""

    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(name="ban", description="Bans a member", usage="eto ban (member) (reason)")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await ctx.message.delete()
        try:
          await member.send(f"You have been banned from the server: {reason}")
        except:
          pass
        await member.ban(reason=f"{reason} | Offender: {ctx.author.id}")
        await ctx.send(f"{ctx.author.mention} Banned {member} with reason: {reason}")
        embed= discord.Embed(title=f"{ctx.author} banned {member}!", description=f"Reason: {reason}", colour=discord.Colour.dark_red(), timestamp=datetime.now())
        embed.set_footer(text=member.id)
        embed.set_author(name=member, icon_url= member.avatar_url)
        await self.bot.get_channel(logchannel).send(embed=embed)
        await ctx.send(f"Banned {member}")


    @commands.command(name="kick", description="Kicks a member", usage="eto ban (member) (reason)")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await ctx.message.delete()
        try:
          await member.send(f"You have been kicked from the server: {reason}")
        except:
          pass
        await member.kick(reason=reason)
        embed= discord.Embed(
        title=f"{ctx.author} kicked {member}!", description=f"Reason: {reason}", colour=discord.Colour.dark_red(), timestamp=datetime.now())
        embed.set_footer(text=member.id)
        embed.set_author(name=member, icon_url= member.avatar_url)
        await self.bot.get_channel(logchannel).send(embed=embed)
        await ctx.send(f"kicked {member}")
  

    @commands.command(name="mute", description="Mutes a member", usage="eto mute (member) (duration) (unit)")
    @commands.has_permissions(ban_members=True)
    async def mute(self, ctx, user : discord.Member, duration = 0, *, units = None):
      await ctx.message.delete()
      role = discord.utils.get(ctx.guild.roles, name = mutedrole)
      perm=False
      await user.add_roles(role)
      if units == "h" or units == "m" or units == "s":
        if units == "s":
          wait = 1 * duration
          unit = "seconds"
        elif units == "m":
          wait = 60 * duration
          unit= "minutes"
        elif units == "h":
          wait = 3600 * duration
          unit= "hours"
        msg=f"Muted {user.mention} for {duration} {unit}!"
      else:
        msg=f"Muted {user.mention} permanently!"
        perm=True
      await ctx.send(msg)
      embed= discord.Embed(title= "A user has been muted!", 
      description=ctx.author.mention + msg, colour=discord.Colour.dark_red(), timestamp=datetime.now())
      embed.set_footer(text=user.id)
      embed.set_author(name= user,icon_url=user.avatar_url)
      await self.bot.get_channel(logchannel).send(embed=embed)
      if perm==False:
        await asyncio.sleep(wait)
        rolecheck = [role.name for role in user.roles]
        if mutedrole in rolecheck:
          await user.remove_roles(role)
          await ctx.send(f"{user.mention} has been unmuted!")
          embed= discord.Embed(title=f"{user} was automatically unmuted", description=" ",colour=discord.Colour.dark_red(), timestamp=datetime.now())
          embed.set_footer(text=user.id)
          embed.set_author(name= user,icon_url=user.avatar_url)
          await self.bot.get_channel(logchannel).send(embed=embed)


    @commands.command(name="unmute", description="Unmutes a member", usage="eto unmute (member)")
    @commands.has_permissions(ban_members=True)
    async def unmute(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name = mutedrole)
        await member.remove_roles(role)
        await ctx.message.delete()
        await ctx.send(f"Unmuted {member.mention}")
        embed= discord.Embed(title= f"{member} was unmuted!", description=" ",colour=discord.Colour.dark_red(), timestamp=datetime.now())
        embed.set_footer(text=member.id)
        embed.set_author(name=member, icon_url=member.avatar_url)
        await self.bot.get_channel(logchannel).send(embed=embed)


    @commands.command(name="warn", description="Gives a member a warning", usage="eto warn (member) (reason)")
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason="No reason provided"):
      await ctx.message.delete()
      try:
        await member.send(f"You have been warned: {reason}")
      except:
        pass
      await ctx.send(f"Warned **{member}**: {reason}")
      embed= discord.Embed( title= f"{member} was warned!", description=f"**Reason**: {reason}", colour=discord.Colour.blue(),timestamp=datetime.now())
      embed.set_footer(text=member.id)
      embed.set_author(name=member,icon_url=member.avatar_url)
      await self.bot.get_channel(logchannel).send(embed=embed)


    @commands.command(name="nick", description="Gives a member a nickname", usage="eto nick (member) (nickname)\nNickname argument is optional")
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, obj, *, nick=None):
      if "@" in obj:
        obj = int(obj.strip('<@&!>'))
      member = ctx.guild.get_member(int(obj))
      if member != None:
        await member.edit(nick=nick)
        await ctx.message.delete()
        if nick==None:
          await ctx.send(content=f"Reset {member}'s nickname")
        else:
          await ctx.send(content=f"{member}'s nickname is now '{nick}'")
      else:
        role = ctx.guild.get_role(int(obj))
        if role != None:
          await ctx.send("Working...")
          for member in role.members:
            await member.edit(nick=nick)
          if nick == None:
            await ctx.send(f"All of {role.mention}'s members have had their nickname reset")
          else:
            await ctx.send(f"All of {role.mention}'s members have had their nicknames changed to {nick}")
        else:
          await ctx.send("Thats not a valid user/role")


    #@commands.command(name="nickall")
    #@commands.has_permissions(administrator=True)
    #async def nickall(self, ctx: commands.context, *, nick=None):
    #  msg=await ctx.send("Changing everyone's nickames...")
    #  await ctx.message.delete()
    #  members=[]
    #  for server_member in ctx.guild.members:
    #    try:
    #      await server_member.edit(nick=nick)
    #    except:
    #      members.append(f"{server_member.mention}")
    #  memberslist = '\n'.join(members)
    #  await msg.delete()
    #  if nick != None:
    #    await ctx.send(f"Set everyone's nickname to '{nick}'")
    #  else:
    #    await ctx.send("Reset everyone's nickname")
    #  if members != []:
    #    embed= discord.Embed(title="Could not change the following user's nickname:", description=memberslist)
    #    await ctx.send(embed=embed)


    @commands.command(name="purge", description="Purges an amount of messages", usage="eto purge (amount)")
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, *, amount: int):
        await ctx.message.delete()
        messages = await ctx.channel.purge(limit=amount)
        logs=self.bot.get_channel(logchannel)
        logging2 = self.bot.get_channel(863627945049849856)
        message_list=[]
        for message in messages:
          if message.attachments:
            message_list.append(f"__{message.author}:__ {message.content}\nattachments: {message.attachments}")
            for attachment in message.attachments:
              image = await attachment.to_file()
              await self.bot.get_channel(863628589257064448).send(file=image)
          elif message.embeds:
            message_list.append(f"__{message.author}:__ {message.content}\embeds: {message.embeds}")
          else:
            message_list.append(f"__{message.author}:__ {message.content}")
        messagelist = '\n'.join(message_list)
        embed= discord.Embed(title=f"{len(messages)} messages were purged!", description=messagelist,colour=discord.Colour.gold(), timestamp=datetime.now())
        embed.add_field(name="in:", value=ctx.channel.mention, inline=False)
        embed.add_field(name="By:", value=ctx.author.mention, inline=False)
        if len(embed.description) < 4096:
          await logging2.send(embed=embed)
          await logs.send(embed=embed)
        else:
          filename="purge_contents.txt"
          with open(filename, 'w') as f:
            f.write(f"Contents of purged messages from {messages[0].channel.name}\n{messagelist}")
          await logging2.send(file=File(filename))
          await logs.send(file=File(filename))
          os.remove(filename)


    @commands.command(name="slowmode", description="Sets the slowmode for a channel", usage="eto slowmode (seconds)")
    @commands.has_permissions(administrator=True)
    async def slowmode(self, ctx, seconds=0):
      await ctx.message.delete()
      await ctx.channel.edit(slowmode_delay=seconds)
      await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")

#---------------------------------------------------------------------
#---------------------------END COG HERE------------------------------
#---------------------------------------------------------------------


class Fun(commands.Cog):
    """A list of fun commands"""

    def __init__(self, bot: commands.bot):
        self.bot = bot


    @commands.command(name="gay", description="Sends an image of your or somebody's avatar with a rainbow overlay", usage="eto gay (member)\nMember argument is optional")
    async def gay(self, ctx):
      if ctx.channel.id == botchannel:
        asset = ctx.author.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        rawpfp = Image.open(data)
        pfp = rawpfp.resize((416, 416))
        front = Image.open("data/Rainbow.png")

        profile = pfp.convert("RGBA")
        overlay = front.convert("RGBA")

        new_img = Image.blend(profile, overlay, 0.5)
        new_img.save("new.png","PNG")
        await ctx.send(file=File("new.png"))


    @commands.command(name="snipe", description="Gets the most recent deleted message within the last 30 seconds", usage="eto snipe")
    async def snipe(self, ctx):
      with open("data/deleted_message.json") as f:
        try:
          msg=json.load(f)
          author=msg[str(ctx.channel.id)]["message"]["Author"]
          content=msg[str(ctx.channel.id)]["message"]["Content"]
          attachments=msg[str(ctx.channel.id)]["message"]["Attachments"]
          if content != None:
              member=ctx.guild.get_member(author)
              embed = discord.Embed(title = "Message sniped", description=content, color=member.color)
              embed.set_author(name = member, icon_url=member.avatar_url)
              x = len(attachments)/2
              if x == 0:
                await ctx.send(embed=embed)
              else:
                embed.add_field(name="Attachments", value="Here are the list of attachments:")
                await ctx.send(embed=embed)
                for i in range(0, int(x)):
                  embed2=discord.Embed(title=f"Attachment #{i+1}:",description= attachments[f"filename{i}"])
                  embed2.set_image(url=attachments[f"url{i}"])
                  await ctx.send(embed=embed2)
              msg[str(ctx.channel.id)]["message"]={}
              with open("data/deleted_message.json", "w") as f:
                json.dump(msg, f)
        except:
          await ctx.send("Cannot find a message to snipe")
      


    @commands.Cog.listener()
    async def on_message_delete(self, message):
      if message.author.id != 698344056475877397:
        with open("data/deleted_message.json") as f:
          msg = json.load(f)
          if str(message.channel.id) not in msg:
            msg[str(message.channel.id)] = {}
          attachmentlist={}
          number=len(message.attachments)
          for i in range(0, number):
            attachmentlist[f"filename{i}"]=message.attachments[i].filename
            attachmentlist[f"url{i}"]=message.attachments[i].url
          msg[str(message.channel.id)]["message"]={"Author":message.author.id, "Content":str(message.content), "Attachments":attachmentlist}
        with open("data/deleted_message.json", "w") as f:
          json.dump(msg, f)
  

    @commands.command(name="coinflip", aliases=["cf"], description="Flips a coin", usage="eto coinflip")
    async def coinflip(self, ctx):
        action= random.randint(0, 1)
        if(action == 0):
            flip= "Tails"
        elif(action == 1):
            flip= "Heads"
        embed= discord.Embed(title=f"{ctx.author.name} has flipped the coin!", description=f"The coin landed on {flip}!")
        await ctx.send(embed=embed)


    @commands.command(name="magic8ball", aliases=["m8b"], description="Tells your fortune", usage="eto magic8ball (question)")
    async def magic8ball(self, ctx, question=None):
      if question==None:
        return await ctx.send("You need to ask a question")
      ran = [
        "It is certain.", "It is decidedly so.", "Without a doubt.",
        "Yes – definitely.", "You may rely on it.", "As I see it, yes.",
        "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
        "Reply hazy, try again.", "Ask again later.",
        "Better not tell you now.", "Cannot predict now.",
        "Concentrate and ask again.", "Don't count on it.", "My reply is no.",
        "My sources say no.", "Outlook not so good.", "Very doubtful."
      ]
      ball = str(random.choice(ran))
      await ctx.send(f"{ctx.author.mention} :8ball: {ball}")


    @commands.command(name="rps", description="Rock paper scissors", usage="eto rps (choice)")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def rps(self, ctx, defend):
        choices = ["r", "p", "s"]
        attack = str(random.choice(choices))
        if defend == "s" and attack == "s":
            await ctx.send(
                "You picked `scissors`, I picked `scissors`. Draw!!"
            )
        elif defend == "s" and attack == "r":
            await ctx.send(
                "You picked `scissors`, I picked `rock`. You lost!")
        elif defend == "s" and attack == "p":
            await ctx.send(
                "You picked `scissors`, I picked `paper`. You won!"
            )
        elif defend == "p" and attack == "p":
            await ctx.send(
                "You picked `paper`, I picked `paper`. Draw!"
            )
        elif defend == "p" and attack == "s":
            await ctx.send(
                "You picked `paper`, I picked `scissors`. You lost!")
        elif defend == "p" and attack == "r":
            await ctx.send(
                "You picked `paper`, I picked `rock`. You won!"
            )
        elif defend == "r" and attack == "r":
            await ctx.send(
                "You picked `rock`, I picked `rock`. Draw!"
            )
        elif defend == "r" and attack == "p":
            await ctx.send(
                "You picked `rock`, I picked `paper`. You lost!")
        elif defend == "r" and attack == "s":
            await ctx.send(
                "You picked `rock`, I picked `scissors`. You won!"
            )


    @commands.command(name="translate", description="Translates a message to a given language", usage="eto translate (output language) (message)")
    async def translate(self, ctx, language, *, words):
      await ctx.send()


#---------------------------------------------------------------------
#---------------------------END COG HERE------------------------------
#---------------------------------------------------------------------


class Miscellaneous(commands.Cog):
    """A list of other commands"""

    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(name="help", description="Shows this message", usage="eto help (command)\nCommand argument is optional")
    async def help(self, ctx, *, decorator=None):
      if decorator != None:
        decorator=self.bot.get_command(decorator)
        if decorator==None:
          return await ctx.send("That's not a valid command")
        embed=discord.Embed(title=decorator.name.capitalize(), description=decorator.description)
        embed.add_field(name="Usage", value=decorator.usage)
        if isinstance(decorator, discord.ext.commands.Group):
          embed.add_field(name="Subcommands", value=", ".join([command.name for command in decorator.commands]))
        if decorator.aliases:
          embed.add_field(name="Aliases", value=", ".join(decorator.aliases))
      else:
        dev=self.bot.get_user(837555094404333608)
        embed=discord.Embed(title="Commands", description="Here is a list of commands for cozyeto, type 'eto help' on a command for more info on that command'")
        embed.set_footer(text=f"DM {dev.name}#{dev.discriminator} for help", icon_url=ctx.guild.icon_url)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        for cogname in self.bot.cogs:
          cog=self.bot.get_cog(cogname)
          try:
            commandlist={f"**{command.name}:** {command.description}" for command in cog.get_commands() if await command.can_run(ctx)==True}
          except:
            pass
          commands="\n".join(commandlist)
          if commandlist != set():
            embed.add_field(name=cogname, value= commands, inline=False)
      await ctx.send(embed=embed)


    @commands.command(name="profile", description="Gets the avatar of a user", usage="eto profile (member)\nMember argument is optional")
    async def profile(self, ctx, member: discord.Member = None):
      if member == None:
        member = ctx.author
      await ctx.send(member.avatar_url)


    @commands.command(name="status", description="Changes the bot's status", usage="eto status (status)")
    @commands.has_permissions(administrator=True)
    async def status(self, ctx, *, status):
      await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name=status))
      await ctx.channel.send("Changed cozyeto's status!")
      await ctx.message.delete()


    @commands.command(name="sa", description="Notifes you for Singapore Airlines flights", usage="eto sa")
    async def sa(self, ctx):
      role = ctx.guild.get_role(airline_ping)
      if ctx.channel == self.bot.get_channel(botchannel):
        if role in ctx.author.roles:
          await ctx.author.remove_roles(role)
          await ctx.send("You will no longer be notifed for Singapore Airlines flights")
        else:
          await ctx.author.add_roles(role)
          await ctx.send("You will now be notified for Singapore Airlines flights")


    @commands.command(name="send", description="Sends a message to a member", usage="eto send (member) (message)")
    @commands.has_permissions(administrator=True)
    async def send(self, ctx, member : discord.Member, *, words):
      await ctx.message.delete()
      await member.send(str(words))
      await ctx.send(f"Sent '{words}' to {member}!")

    @send.error
    async def send_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandInvokeError):
            msg = await ctx.send('That user has DMs disabled!')
            await asyncio.sleep(5)
            await msg.delete()


    @commands.command(name="type", description="Makes the bot send a message", usage="eto type (message)")
    async def type(self, ctx, *, message):
      user_regex = r"@&[a-zA-Z0-9]+"
      match = re.findall(user_regex, message)
      if match or "@everyone" in message or "@here" in message:
        await ctx.author.send('lol no')
        return
      else:
        if ctx.message.reference:
          await ctx.channel.send(content=message, reference=ctx.message.reference)
          await ctx.message.delete()
        else:
          await ctx.channel.send(message)
          await ctx.message.delete()


    @commands.command(name="sendmessage", description="Sends a message to a channel", usage="eto sendmessage (channel) (message)")
    @commands.has_permissions(manage_channels=True)
    async def sendmessage(self, ctx, channel:discord.TextChannel, *, words):
      if '@everyone' in words or '@here' in words:
            await ctx.message.delete() 
            await ctx.author.send('no')
      else:
        await channel.send(words)
        await ctx.channel.send(f"Sent '{words}' to {channel.mention}")


    @commands.command(name="ping", description="Gets the bot's current websocket and API latency", usage="eto ping")
    async def ping(self, ctx: commands.Context):
        start_time = time.time()
        message = await ctx.send("Testing Ping...")
        end_time = time.time()
        await message.edit(content=f"Pong! {round(self.bot.latency * 1000)}ms\nAPI: {round((end_time - start_time) * 1000)}ms")


    @commands.command(name="rules", description="Sends the server rules", usage="eto rules")
    @commands.cooldown(rate=1, per=30)
    async def rules(self, ctx):
            await ctx.channel.purge(limit=1)
            embed = discord.Embed(
                title='Rules',
                description=
                'These are the  rules of the server, and can change at any time',
                colour=discord.Colour.dark_grey())
            embed.add_field(
                name='1. No Toxicity:',
                value=
                "Don’t be too toxic around members. Try and keep drama out of this server. Directed swears should be kept at a minimum level.",
                inline=True)
            embed.add_field(
                name='2. No racial slurs:',
                value=
                "The use of racial slurs in chat will be a kick or a ban based on the usage.",
                inline=True)
            embed.add_field(
                name='3. No NSFW:',
                value=
                'All nsfw and/or porn should go in #nsfw. Keep sexual talk out of #singapore',
                inline=True)
            embed.add_field(
                name='4. No spam:',
                value=
                'Spam should be kept in #spam. Spamming anywhere else will result in a mute.',
                inline=True)
            embed.add_field(
                name='5. Keep this server private:',
                value=
                "When you are in WTB, don't mention this server at all, this includes any codenames. If you would like to tell somebody to go here, ping them in #singapore",
                inline=True)
            embed.set_footer(text='Type "eto help" in #bot-commands for a list of commands.')
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/821564618577149982.png?v=1")
            await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_message(self, message):
      mainchannel = self.bot.get_channel(wordstorychannel)
      if message.channel==mainchannel:
        if " " in message.content or "\n" in message.content:
            await message.author.send("No")
            await message.delete()



#---------------------------------------------------------------------
#---------------------------END COG HERE------------------------------
#---------------------------------------------------------------------


class ErrorHandler(commands.Cog):
    """A cog for global error handling."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error: commands.CommandError):
        """A global error handler cog."""
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.CommandOnCooldown):
            message=f"This command is on cooldown, please try again after {round(error.retry_after, 1)} seconds."
        #elif isinstance(error, commands.MissingPermissions):
            #message = "You are not allowed to run this command!"
        #elif isinstance(error, commands.UserInputError):
            #message= "Invalid arguments"
        else:
          raise error
        await ctx.send(message)

#---------------------------------------------------------------------
#---------------------------END COG HERE------------------------------
#---------------------------------------------------------------------


def setup(bot: commands.Bot):
    bot.add_cog(Moderation(bot))
    bot.add_cog(Fun(bot))
    bot.add_cog(Miscellaneous(bot))
    bot.add_cog(ErrorHandler(bot))