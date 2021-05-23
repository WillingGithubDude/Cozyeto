import asyncio
import discord
import time
import os
import random
import datetime
import re
import tracemalloc
from keep_alive import keep_alive
from discord.utils import get
from discord import Member
from discord.ext import commands
from datetime import datetime, timedelta


intents = discord.Intents.default()
intents.members = True
tracemalloc.start()

client = commands.Bot(command_prefix='eto ', intents=intents)

token = os.environ.get("DISCORD_BOT_SECRET")

permissions_error = 'You are not allowed to use this command!'

invites = {}
logchannel = 815379976047296542
logchannel2 = 818020807649394708
joinchannel = 799645293116391425
wordstorychannel = 824503746167177216
suggestchannel = 823075391186403348
botchannel = 798771440660906005
botrole = 823071010613362758
serverID = 786436071961395208
quotechannel = 825522469749784587
msgID = 824502147507945472
msgID2 = 824521761789837332
msgID3 = 828733495806656544
cozyetomailID = 831691345894703144
airline_ping = 835378894785609749
mutedrole = 'Muted'


def find_invite_by_code(invite_list, code):
    for inv in invite_list:
        if inv.code == code:
            return inv


@client.event
async def on_member_join(member):
    coolchannel = client.get_channel(joinchannel)
    await coolchannel.send(f"Welcome to the server {member.mention} <:cozyeto:786789349253447690>!")
    for invite in invites[member.guild.id]:
        if invite.uses < find_invite_by_code(await member.guild.invites(), invite.code).uses:
          embed= discord.Embed(title= str(member) + " joined the server!", description=f"Invited by {invite.inviter.mention}", colour=discord.Colour.teal(), timestamp=datetime.now())
          await client.get_channel(logchannel).send(embed=embed)
          invites[member.guild.id] = await member.guild.invites()
          return


@client.event
async def on_member_remove(member):
    invites[member.guild.id] = await member.guild.invites()
    await client.get_channel(joinchannel).send(f"{member.mention} has left the server... <:cozyluna:786789373735469066>")
    embed= discord.Embed(title= str(member) + " left the server!", description=" ", colour=discord.Colour.dark_orange(),
    timestamp=datetime.now())
    await client.get_channel(logchannel).send(embed=embed)


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await ctx.message.delete()
    try:
      await member.send('You have been banned from the server: ' + str(reason))
    except:
      pass
    await member.ban(reason=reason)
    await ctx.send(str(ctx.author.mention) + ' Banned ' + str(member) + ' with reason: ' + str(reason))
    embed= discord.Embed(
    title= str(ctx.author) + " banned " + str(member) + "!", description="Reason: "+ str(reason), colour=discord.Colour.dark_red(), timestamp=datetime.now())
    await client.get_channel(logchannel).send(embed=embed)


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(permissions_error)
    else:
      raise error


@client.command()
@commands.has_permissions(administrator=True)
async def nickall(ctx, *, nick=None):
  msg=await ctx.send("Changing everyone's nickames...")
  await ctx.message.delete()
  members=[]
  for server_member in ctx.guild.members:
    try:
      await server_member.edit(nick=nick)
    except:
      members.append(f"{server_member.mention}")
  memberslist = '\n'.join(members)
  await msg.delete()
  if nick != None:
    await ctx.send(f"Set everyone's nickname to '{nick}'")
  else:
    await ctx.send("Reset everyone's nickname")
  if members != []:
    embed= discord.Embed(title="Could not nick the following users:", description=memberslist, colour=discord.colour.light_grey())
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member: discord.Member, *, nick=None):
    await member.edit(nick=nick)
    await ctx.message.delete()
    await ctx.send(f"{member}'s nickname is now {nick}")
    embed= discord.Embed(title=f"{ctx.author} changed {member}'s nickname!", 
    description=f"Their nickmame is now {nick}",colour=discord.Colour.dark_purple(), timestamp=datetime.now())
    await client.get_channel(logchannel).send(embed=embed)


@nick.error
async def nick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        msg = await ctx.send(permissions_error)
        await asyncio.sleep(5)
        await msg.delete()

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await ctx.message.delete()
    try:
      await member.send('You have been kicked from the server: ' + str(reason))
    except:
      pass
    await member.kick(reason=reason)
    await ctx.send(str(ctx.author.mention) + ' Kicked ' + str(member) + ' with reason: ' + str(reason))
    embed= discord.Embed(
    title= str(ctx.author) + " kicked " + str(member) + "!", description="Reason: "+ str(reason), colour=discord.Colour.dark_red(), timestamp=datetime.now())
    await client.get_channel(logchannel).send(embed=embed)


@client.command()
@commands.has_permissions(ban_members=True)
async def ghostkick(ctx, member: discord.Member, *, reason=None):
    await ctx.messsage.delete()
    await member.kick(reason=reason)
    embed= discord.Embed(
    title= str(ctx.author) + " ghost kicked " + str(member) + "!", description="Reason: "+ str(reason), colour=discord.Colour.dark_purple(),timestamp=datetime.now())
    await client.get_channel(logchannel).send(embed=embed)


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(permissions_error)


@client.command()
@commands.has_permissions(ban_members=True)
async def mute(ctx, user : discord.Member, duration= 0, units = None):
      await ctx.message.delete()
      role = discord.utils.get(ctx.message.guild.roles, name = mutedrole)
      perm=False
      await user.add_roles(role)
      if duration == int(duration):
        pass
      else: 
        duration=0
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
      embed.set_author(name= "w",icon_url=user.avatar_url)
      await client.get_channel(logchannel).send(embed=embed)
      if perm==False:
        await asyncio.sleep(wait)
        rolecheck = [role.name for role in user.roles]
        if mutedrole in rolecheck:
          await user.remove_roles(role)
          await ctx.send(f"{user.mention} has been unmuted!")
          embed= discord.Embed(title=f"{user} was automatically unmuted", description=" ",colour=discord.Colour.dark_red(), timestamp=datetime.now())
          embed.set_footer(text=user.id)
          embed.set_author(name= "᲼",icon_url=user.avatar_url)
          await client.get_channel(logchannel).send(embed=embed) 


@client.command()
@commands.has_permissions(ban_members=True)
async def unmute(ctx, member : discord.Member):
    role = discord.utils.get(ctx.message.guild.roles, name = mutedrole)
    await member.remove_roles(role)
    await ctx.send(f"Unmuted {member.mention}")
    embed= discord.Embed(title= f"{member} was unmuted!", description=" ",colour=discord.Colour.dark_red(), timestamp=datetime.now())
    embed.set_footer(text=member.id)
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    await client.get_channel(logchannel).send(embed=embed)


@client.command()
async def sa(ctx):
  role = ctx.guild.get_role(airline_ping)
  if ctx.channel == client.get_channel(botchannel):
    if role in ctx.author.roles:
      await ctx.author.remove_roles(role)
      await ctx.send("You will no longer be notifed for Singapore Airlines flights")
    else:
      await ctx.author.add_roles(role)
      await ctx.send("You will now be notified for Singapore Airlines flights")


@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(permissions_error)
    else:
      raise error


@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(permissions_error)
    else:
      raise error


@client.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    if reason == None:
      reason="No reason provided"
    await ctx.message.delete()
    try:
      await member.send(f"You have been warned: {reason}")
    except:
      pass
    await ctx.send(f"Warned **{member}**: {reason}")
    embed= discord.Embed( title= f"{member} was warned!", description=f"**Reason**: {reason}", colour=discord.Colour.blue(),timestamp=datetime.now())
    embed.set_footer(text=member.id)
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    await client.get_channel(logchannel).send(embed=embed)


@warn.error
async def warn_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(permissions_error)
    else:
      raise error


@client.command()
@commands.has_permissions(administrator=True)
async def update(ctx, member : discord.Member):
  role = ctx.guild.get_role(823070003489144843)
  await member.add_roles(role)
  await ctx.channel.send("ok")


@client.command()
@commands.has_permissions(administrator=True)
async def send(ctx, member : discord.Member, *, words):
  await ctx.message.delete()
  await member.send(str(words))
  await ctx.send(f"Sent '{words}' to {member}!")


@send.error
async def send_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send('That user has DMs disabled!')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(permissions_error)
    else:
      raise error


@client.command()
async def ping(ctx):
    ping = client.latency * 1000
    final = '%0.2f' % ping
    await ctx.send('Pong! `' + str(final) + ' ms`')


@client.command() 
async def type(ctx, *, message):
  if ctx.channel.id != wordstorychannel:
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


#@client.command() 
#@commands.has_permissions(send_tts_messages=True)
#async def tts(ctx, *, message):
#  user_regex = r"@&[a-zA-Z0-9]+"
#  match = re.findall(user_regex, message)
#  if match or "@everyone" in message or "@here" in message:
#    await ctx.author.send('lol no')
#  else:
#    await client2.send_message(ctx.channel, message, tts=True)
#    await ctx.message.delete()


@client.command()
@commands.has_permissions(manage_channels=True)
async def sendmessage(ctx, channel=None, *, words):
    if '@everyone' in words or '@here' in words:
        await ctx.message.delete() 
        await ctx.author.send('no')
    elif channel != None:
        try:
            chanel = await client.fetch_channel(channel)
            await chanel.send(words)
            await ctx.message.delete()
            await ctx.channel.send('Sent "' + str(words) + '" to ' + chanel.mention)
        except:
            pass


@sendmessage.error
async def sendmessage_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(permissions_error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Invalid arguments; 'eto sendmessage (channelID here) (message)'")
    else:
      raise error


@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, *, amount: int):
    global context
    context = ctx
    global number
    number = str(amount)
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)


@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(permissions_error)
    else:
      raise error


@client.command()
@commands.has_permissions(manage_messages=True)
async def slowmode(ctx, seconds: int):
    await ctx.message.delete()
    await ctx.channel.edit(slowmode_delay=str(seconds))
    await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")
    embed= discord.Embed(
    title=f"The cooldown in {ctx.channel} was changed!", 
    description= f"The cooldown is now {seconds} seconds", colour=discord.Colour.orange(), timestamp=datetime.now())
    embed.set_footer(text=ctx.author.id)
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    await client.get_channel(logchannel).send(embed=embed)


@slowmode.error
async def slowmode_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(permissions_error)
    elif isinstance(error, commands.BadArgument):
        await ctx.send("You must provide a number")
    else:
      raise error

@client.command()
async def embed(ctx, title, *, description):
    await ctx.message.delete()
    embed = discord.Embed(title=title, description=description, colour=discord.Colour.blue())
    await ctx.send(embed=embed)


@embed.error
async def embed_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        msg = await ctx.send("Invalid arguments; 'eto embed (title here) (message)'")
        await asyncio.sleep(5)
        await msg.delete
    else:
      raise error


@client.command()
async def profile(ctx, member: discord.Member = None):
 if member==None:
  member = ctx.author
 await ctx.send(member.avatar_url)


@profile.error
async def profile_error(ctx, error):
  if isinstance(error, commands.MemberNotFound):
    await ctx.send("Not a valid user")
  else:
      raise error


@client.command()
async def coinflip(ctx):
    action= random.randint(0, 1)
    if(action == 0):
        flip= "Tails"
    elif(action == 1):
        flip= "Heads"
    time.sleep(1)
    embed= discord.Embed(title=f"{ctx.author.name} has flipped the coin!", description=f"The coin landed on {flip}!")
    await ctx.send(embed=embed)

@client.command()
async def suggest(ctx, *, message):
  if ctx.channel == client.get_channel(botchannel):
    embed= discord.Embed(title= "New suggestion:", description=message,colour=discord.Colour.blue(), timestamp=datetime.now())
    embed.set_footer(text=ctx.author.id)
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    await client.get_channel(suggestchannel).send(embed=embed)
    await ctx.message.delete()

#@client.command()
#async def suggestions(ctx):
#  embed= discord.Embed(title= 'How to make a suggestion', description="Type 'eto suggest (suggestion)' in #bot-commands to make a suggestion \n This can be used for role requests as well if you are Second Class or higher",colour=discord.Colour.gold())
#  await client.get_channel(suggestchannel).send(embed=embed)
#  await ctx.message.delete()


@client.command()
async def magic8ball(ctx):
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
    await ctx.send(ctx.author.mention + ' :8ball: ' + ball)


@client.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def rps(ctx, defend):
    choices = ["s", "r", "p"]
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


@client.command()
async def rules(ctx):
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


@client.command()
@commands.has_permissions(administrator=True)
async def status(ctx, *,name):
  await client.change_presence(status=discord.Status.online, activity=discord.Game(name=name))
  await ctx.channel.send("Changed cozyeto's status!")
  await ctx.message.delete()
  embed= discord.Embed(title="cozyeto's status was changed!", description= str(name),colour=discord.Colour.green(), timestamp=datetime.now())
  embed.set_footer(text=ctx.author.id)
  embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
  await client.get_channel(logchannel).send(embed=embed)


@status.error
async def status_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        msg = await ctx.send(permissions_error)
        await asyncio.sleep(5)
        await msg.delete()
    else:
      raise error


@client.event
async def on_message(message):
  mainchannel = client.get_channel(wordstorychannel)
  guild = client.get_guild(serverID)
  global category
  category = discord.utils.get(guild.categories, id=cozyetomailID)
  overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=False)}
  if str(message.channel.type) == "private":
    if message.author == client.user:
        pass
    else:
      c=None
      for channel in category.channels:
        if channel.topic==f"{message.author.id}":
            c=channel.topic
            break
      if c==None:
          channel = await guild.create_text_channel(name=f"{message.author.name}-{message.author.discriminator}", category=category, overwrite=overwrites, topic=f"{message.author.id}")
          embed= discord.Embed(title=f"New message", description= message.content,colour=discord.Colour.green(), timestamp=datetime.now())
          embed.set_author(name=message.author, icon_url=message.author.avatar_url)
          await channel.send(embed=embed)
      else: 
        embed= discord.Embed(title=f"New message", description= message.content,colour=discord.Colour.green(), timestamp=datetime.now())
        embed.set_author(name=message.author, icon_url=message.author.avatar_url)
        await channel.send(embed=embed)
  elif message.channel.category==category:
    if message.author == client.user:
        pass
    else:
      global person
      if message.content.startswith("eto close") or message.content.startswith("eto areply") or message.content.startswith("eto aclose") :
        person=get(guild.members, id=int(message.channel.topic))
      elif message.content.startswith("="):
          pass
      else:
        await message.delete()
        embed=discord.Embed(title=f"Message sent", description= message.content,colour=discord.Colour.red(), timestamp=datetime.now())
        embed.set_author(name=message.author, icon_url=message.author.avatar_url)
        person=get(guild.members, id=int(message.channel.topic))
        embed2=discord.Embed(title="New message", description= message.content,colour=discord.Colour.red(), timestamp=datetime.now())
        embed2.set_author(name=message.author, icon_url=message.author.avatar_url)
        await message.channel.send(embed=embed)
        await person.send(embed=embed2)
  else:
    if message.channel==mainchannel:
      if " " in message.content or "\n" in message.content:
        try:
          await message.author.send("No")
        except:
          pass
        await message.delete()
    elif message.channel==client.get_channel(quotechannel):
      if message.attachments:
        await client.process_commands(message)
      else: 
        await message.delete()
  await client.process_commands(message)


@client.command()
async def close(ctx, *, message=None):
  if ctx.channel.category == category:
      if message==None:
        content="No reason provided"
      else:
        content=message
      embed=discord.Embed(title="Message chat closed", description= content,colour=discord.Colour.red(), timestamp=datetime.now())
      embed.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
      await person.send(embed=embed)
      await ctx.channel.delete()


@client.command()
async def aclose(ctx, *, message=None):
  if ctx.channel.category == category:
      if message==None:
        content="No reason provided"
      else:
        content=message
      embed=discord.Embed(title="Message chat closed", description= content,colour=discord.Colour.dark_purple(), timestamp=datetime.now())
      embed.set_author(name="top secret.#0000", icon_url="https://s3.amazonaws.com/appforest_uf/f1493101482859x646389236906543400/YeVk_bj_.jpg")
      await person.send(embed=embed)
      await ctx.channel.delete()


@client.command()
async def areply(ctx, *, message=None):
  if ctx.channel.category == category:
    await ctx.message.delete()
    embed=discord.Embed(title=f"Message sent (anonymous)", description= message ,colour=discord.Colour.dark_purple(), timestamp=datetime.now())
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    embed2=discord.Embed(title="New message", description= message,colour=discord.Colour.dark_purple(), timestamp=datetime.now())
    embed2.set_author(name="top secret.#0000", icon_url="https://s3.amazonaws.com/appforest_uf/f1493101482859x646389236906543400/YeVk_bj_.jpg")
    await ctx.channel.send(embed=embed)
    await person.send(embed=embed2)

  
  #nofilter1=client.get_channel(816844780386123786)
  #nofilter2=client.get_channel(786810234735820800)
  #nofilter3=client.get_channel(805903205568610344)
  #nofilter4=client.get_channel(817954488924372993)
  #else:
    #if message.channel==nofilter1 or message.channel==nofilter2 or message.channel==nofilter3 or message.channel==nofilter4:
      #process_message
    #else:
        #for word in badwords:
          #if word in message.content:
            #await message.delete()
            #msg = await message.channel.send("You can't say that...")
            #await asyncio.sleep(5)
            #await msg.delete()
          #else:
            #process_message


@client.event
async def on_message_edit(message_before, message_after):
  mainchannel = client.get_channel(wordstorychannel)
  role = message_after.guild.get_role(botrole)
  user = message_before.author
  if message_after.channel==mainchannel:
    if " " in message_after.content or "\n" in message_after.content:
      await message_after.delete()
  if role in user.roles: 
    pass
  else:
    embed=discord.Embed(title='Message edited!', description= "**Before:** \n" + str(message_before.content) + "\n **After:** \n" + str(message_after.content), colour=discord.Colour.orange(), timestamp=datetime.now())
    embed.add_field(name="In: ", value=str(message_before.channel.mention), inline=True)
    embed.set_footer(text=message_after.author.id)
    embed.set_author(name=message_before.author, icon_url=message_before.author.avatar_url)
    await client.get_channel(logchannel2).send(embed=embed)

@client.event
async def on_message_delete(message):
    logging = client.get_channel(logchannel2)
    if message.attachments:
      embed=discord.Embed(title='Message deleted', description=str(message.content), colour=discord.Colour.blue(), timestamp=datetime.now())
      embed.add_field(name="In: ", value=str(message.channel.mention), inline=True)
      embed.add_field(name = "attachments: ", value=str(message.attachments), inline=False)
      embed.set_footer(text=message.author.id)
      embed.set_author(name=message.author,icon_url=message.author.avatar_url)
      await logging.send(embed=embed)
    else:
      embed=discord.Embed(title='Message deleted', description=str(message.content), colour=discord.Colour.blue(), timestamp=datetime.now())
      embed.add_field(name="In: ", value=str(message.channel.mention), inline=True)
      embed.set_footer(text=message.author.id)
      embed.set_author(name=message.author,icon_url=message.author.avatar_url)
      await logging.send(embed=embed)


@client.event
async def on_bulk_message_delete(messages):
  global context
  messages_list = []
  for i in range(0, len(messages)):
    if messages[i].attachments:
      messages_list.append(f"__{str(messages[i].author)}:__ {str(messages[i].content)}\n attachments: {str(messages[i].attachments)}")
    else:
      messages_list.append(f"__{str(messages[i].author)}:__ {messages[i].content}")
  messagelist = '\n'.join(messages_list)
  embed= discord.Embed(title=f"{context.author} purged {number} messages!", description=messagelist,colour=discord.Colour.gold(), timestamp=datetime.now())
  embed.add_field(name="in:" ,value= context.channel.mention, inline=True)
  await client.get_channel(logchannel).send(embed=embed)


@client.event
async def on_raw_reaction_add(payload=None):
    guild = discord.utils.get(client.guilds, id=serverID)
    role = discord.utils.get(guild.roles, name='Notifications')
    role2 = discord.utils.get(guild.roles, name='Downtown Singaporian')
    role3 = discord.utils.get(guild.roles, name = 'Minecraft')
    thirdclass= discord.utils.get(guild.roles, name = 'Third Class')
    singaporian = discord.utils.get(guild.roles, name = 'Singaporian')
    jokechannelsrole = discord.utils.get(guild.roles, name = 'Joke Channels Access')
    if payload is not None:
        if payload.message_id==msgID:
            if str(payload.emoji)=="<:cozyluna:786789373735469066>":
                await payload.member.add_roles(role)
            elif str(payload.emoji)=="<:cozyeto:786789349253447690>":
                await payload.member.add_roles(role2)
            elif str(payload.emoji)=="<:uncozyeto:805915542702653440>":
                await payload.member.add_roles(role3)
        elif payload.message_id==msgID2:
            if str(payload.emoji)=="<:cozyeto:786789349253447690>":
                await payload.member.add_roles(singaporian)
                await payload.member.add_roles(thirdclass)
        elif payload.message_id==msgID3:
            if str(payload.emoji)=="<:cozyeto:786789349253447690>":
                await payload.member.add_roles(jokechannelsrole)

@client.event
async def on_raw_reaction_remove(payload=None):
    guild = discord.utils.get(client.guilds, id=serverID)
    role = discord.utils.get(guild.roles, name='Notifications')
    role2 = discord.utils.get(guild.roles, name='Downtown Singaporian')
    role3 = discord.utils.get(guild.roles, name = 'Minecraft')
    singaporian = discord.utils.get(guild.roles, name = 'Singaporian')
    jokechannelsrole = discord.utils.get(guild.roles, name = 'Joke Channels Access')
    user = get(guild.members, id=payload.user_id)
    if payload is not None:
        if payload.message_id == msgID:
            if str(payload.emoji)=="<:cozyluna:786789373735469066>":
                await user.remove_roles(role)
            elif str(payload.emoji)=="<:cozyeto:786789349253447690>":
                await user.remove_roles(role2)
            elif str(payload.emoji)=="<:uncozyeto:805915542702653440>":
                await user.remove_roles(role3)
        elif payload.message_id==msgID2:
            if str(payload.emoji)=="<:cozyeto:786789349253447690>":
                await user.remove_roles(singaporian)
        elif payload.message_id==msgID3:
            if str(payload.emoji)=="<:cozyeto:786789349253447690>":
                await user.remove_roles(jokechannelsrole)

@client.event
async def on_user_update(before, after):
  logs=client.get_channel(logchannel)
  if before.avatar != after.avatar:
    embed=discord.Embed(title=f"Avatar updated", description="**Before**:" ,colour=discord.Colour.blurple())
    embed.set_author(name=after, icon_url=after.avatar_url)
    embed.set_image(url=before.avatar_url)
    await logs.send(embed=embed)
    embed2=discord.Embed(title=" ", description="**After**:" ,colour=discord.Colour.blurple(), timestamp=datetime.now())
    embed2.set_image(url=after.avatar_url)
    embed2.set_footer(text=before.id)
    await logs.send(embed=embed2)
  if before.name != after.name:
    embed=discord.Embed(title=f"Username updated", description=f"**Before**: {before.name}#{before.discriminator}\n **After**: {after.name}#{after.discriminator}" ,colour=discord.Colour.blurple(), timestamp=datetime.now())
    embed.set_author(name=after, icon_url=after.avatar_url)
    embed.set_footer(text=before.id)
    await logs.send(embed=embed)
  if before.discriminator != after.discriminator:
    embed=discord.Embed(title=f"Username updated", description=f"**Before**: {before.name}#{before.discriminator}\n **After**: {after.name}#{after.discriminator}" ,colour=discord.Colour.blurple(), timestamp=datetime.now())
    embed.set_author(name=after, icon_url=after.avatar_url)
    embed.set_footer(text=before.id)
    await logs.send(embed=embed)


# --
#await bot.change_presence(activity=discord.Game(name="a game"))
# --
#await bot.change_presence(activity=discord.Streaming(name="My Stream", url=my_twitch_url))
# --
#await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))
# --
#await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))


@client.event
async def on_ready():
  for guild in client.guilds:
    try:
      invites[guild.id] = await guild.invites()
    except:
      pass
  print('Online!')

keep_alive()
client.run(token)