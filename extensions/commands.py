import os
import re
import time
import typing
import asyncio
import discord
import datetime
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

  # @commands.command()
  # async def join(self, ctx, channel: discord.VoiceChannel):
  #   voiceclient = await channel.connect()
  #   print(voiceclient.endpoint)
  #   invite = await channel.create_invite(target_type=discord.InviteTarget.embedded_application, target_application_id=755600276941176913)
  #   await ctx.send(invite)
  
  # @commands.command()
  # async def leave(self, ctx):
  #   active_vcs = self.bot.voice_clients
  #   if active_vcs:
  #     for voiceChannel in active_vcs:
  #       await voiceChannel.disconnect()
    
  # @commands.command()
  # async def info(self, ctx):
  #   invite = await self.bot.fetch_invite("https://discord.gg/GVbanQWtJJ")
  #   print(invite.target_application)
  #   print(invite.target_type)

  @commands.command(name="ban", description="Bans a member")
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


  @commands.command(name="kick", description="Kicks a member")
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


  @commands.command(name="mute", description="Mutes a member", aliases=("stfu", "shutup"))
  @commands.has_permissions(kick_members=True)
  async def mute(self, ctx, member: discord.Member, duration:int=None, *, units=None):
    if duration==None:
      duration=0
    await ctx.message.delete()
    role = discord.utils.get(ctx.guild.roles, name = mutedrole)
    perm=False
    await member.add_roles(role)
    if units == "s":
      wait = 1 * duration
      unit = "seconds"
    elif units == "m":
      wait = 60 * duration
      unit = "minutes"
    elif units == "h":
      wait = 3600 * duration
      unit = "hours"
    else:
      msg = f"Muted {member.mention} permanently!"
      perm = True
    if perm == False:
      msg=f"Muted {member.mention} for {duration} {unit}!"
    await ctx.send(msg)
    embed = discord.Embed(title= "A user has been muted!", 
    description=ctx.author.mention + msg, colour=discord.Colour.dark_red(), timestamp=datetime.now())
    embed.set_footer(text=member.id)
    embed.set_author(name= member,icon_url=member.avatar_url)
    await self.bot.get_channel(logchannel).send(embed=embed)
    if perm==False:
      await asyncio.sleep(wait)
      rolecheck = [role.name for role in member.roles]
      if mutedrole in rolecheck:
        await member.remove_roles(role)
        await ctx.send(f"{member.mention} has been unmuted!")
        embed= discord.Embed(title=f"{member} was automatically unmuted", description=" ",colour=discord.Colour.dark_red(), timestamp=datetime.now())
        embed.set_footer(text=member.id)
        embed.set_author(name= member,icon_url=member.avatar_url)
        await self.bot.get_channel(logchannel).send(embed=embed)


  @commands.command(name="unmute", description="Unmutes a member")
  @commands.has_permissions(ban_members=True)
  async def unmute(self, ctx, member: discord.Member):
      role = discord.utils.get(ctx.guild.roles, name = mutedrole)
      await member.remove_roles(role)
      await ctx.message.delete()
      await ctx.send(f"Unmuted {member.mention}")
      embed=discord.Embed(title= f"{member} was unmuted!", description=" ",colour=discord.Colour.dark_red(), timestamp=datetime.now())
      embed.set_footer(text=member.id)
      embed.set_author(name=member, icon_url=member.avatar_url)
      await self.bot.get_channel(logchannel).send(embed=embed)


  @commands.command(name="warn", description="Gives a member a warning")
  @commands.has_permissions(kick_members=True)
  async def warn(self, ctx, member: discord.Member, *, reason=None):
    await ctx.message.delete()
    if reason==None:
      reason="No reason provided"
    try:
      await member.send(f"You have been warned: {reason}")
    except:
      pass
    await ctx.send(f"Warned **{member}**: {reason}")
    embed= discord.Embed( title= f"{member} was warned!", description=f"**Reason**: {reason}", colour=discord.Colour.blue(),timestamp=datetime.now())
    embed.set_footer(text=member.id)
    embed.set_author(name=member,icon_url=member.avatar_url)
    await self.bot.get_channel(logchannel).send(embed=embed)


  @commands.command(name="nick", description="Gives a member a nickname")
  @commands.has_permissions(manage_nicknames=True)
  async def nick(self, ctx, MemberOrRole: typing.Union[discord.Member, discord.Role], *, nick=None):
    obj = MemberOrRole
    if isinstance(obj, discord.Member):
      await obj.edit(nick=nick)
      await ctx.message.delete()
      if nick==None:
        await ctx.send(content=f"Reset {obj}'s nickname")
      else:
        await ctx.send(content=f"{obj}'s nickname is now '{nick}'")
    elif isinstance(obj, discord.Role):
      await ctx.send("Working...")
      for member in obj.members:
        await member.edit(nick=nick)
      if nick == None:
        await ctx.send(f"All of {obj.mention}'s members have had their nickname reset")
      else:
        await ctx.send(f"All of {obj.mention}'s members have had their nicknames changed to {nick}")
    else:
      await ctx.send("Thats not a valid member or role")


  @commands.command(name="purge", description="Purges an amount of messages")
  @commands.has_permissions(administrator=True)
  async def purge(self, ctx, amount: int):
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


  @commands.command(name="slowmode", description="Sets the slowmode for a channel")
  @commands.has_permissions(administrator=True)
  async def slowmode(self, ctx, seconds:int=None):
    if seconds==None:
      seconds=0
    await ctx.message.delete()
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")


#----------------------------------------------------------------
#------------------------END COG HERE----------------------------
#----------------------------------------------------------------


class Miscellaneous(commands.Cog):
    """A list of other commands"""

    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(name="help", description="Shows this message")
    async def help(self, ctx, *, command=None):
      if command != None:
        command=self.bot.get_command(command)
        if command==None:
          return await ctx.send("That's not a valid command")
        embed=discord.Embed(title=command.name.capitalize(), description=command.description)
        embed.add_field(name="Usage", value=f"{ctx.prefix}{command.qualified_name} {command.signature}\nArguments in <> are required and arguments in [] are optional")
        if isinstance(command, discord.ext.commands.Group):
          embed.add_field(name="Subcommands", value=", ".join([subcommand.name for subcommand in command.commands]))
        if command.brief:
          embed.add_field(name="Details", value=command.brief)
        if command.aliases:
          embed.add_field(name="Aliases", value=", ".join(command.aliases))
      else:
        dev=self.bot.get_user(837555094404333608)
        embed=discord.Embed(title="Commands", description=f"Here is a list of commands for {self.bot.user.name}, type '{self.bot.command_prefix}help' on a command for more info on that command'")
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


    @commands.command(name="send", description="Sends a message to a member", usage="eto send (member) (message)")
    @commands.has_permissions(administrator=True)
    async def send(self, ctx, obj: typing.Union[discord.TextChannel, discord.Member], *, words):
      await ctx.message.delete()
      await obj.send(words)
      await ctx.send(f"Sent '{words}' to {obj}!")

    @send.error
    async def send_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandInvokeError):
            msg = await ctx.send('That user has DMs disabled!')
            await asyncio.sleep(5)
            await msg.delete()
        elif isinstance(error, commands.BadUnionArgument):
            msg = await ctx.send("That's not a valid member/channel")
        await asyncio.sleep(5)
        await msg.delete


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

#----------------------------------------------------------------
#------------------------END COG HERE----------------------------
#----------------------------------------------------------------


def setup(bot: commands.Bot):
    bot.add_cog(Moderation(bot))
    bot.add_cog(Miscellaneous(bot))
    bot.add_cog(ErrorHandler(bot))