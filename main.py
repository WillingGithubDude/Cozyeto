from keep_alive import keep_alive
import asyncio
import discord
import time
import os
import random
import datetime
import re
import tracemalloc
from datetime import timedelta, datetime
from discord.utils import get
from replit import db
from discord import Member
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
tracemalloc.start()

client = commands.Bot(command_prefix='eto ', intents=intents)

token = os.environ.get("DISCORD_BOT_SECRET")

permissions_error = 'You are not allowed to use this command!'

logchannel = 815379976047296542
logchannel2 = 818020807649394708
joinchannel = 799645293116391425
wordstorychannel = 824503746167177216
suggestchannel = 823075391186403348
botchannel = 798771440660906005
botrole = 823071010613362758
serverID = 786436071961395208
mutedrole = 'Muted'

@client.event
async def on_member_join(member):
    coolchannel = client.get_channel(joinchannel)
    await coolchannel.send('Welcome to the server ' + str(member.mention) + '"<:cozyeto:786789349253447690>!')
    embed= discord.Embed(
    title= str(member) + " joined the server!", description=" ", colour=discord.Colour.teal(), timestamp=datetime.now())
    await client.get_channel(logchannel).send(embed=embed)


@client.event
async def on_member_remove(member):
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

@client.command()
@commands.has_permissions(ban_members=True)
async def ghostban(ctx, member: discord.Member, *, reason=None):
    await ctx.messsage.delete()
    await member.ban(reason=reason)
    embed= discord.Embed(
    title= str(ctx.author) + " ghost banned " + str(member) + "!", description="Reason: "+ str(reason), colour=discord.Colour.dark_purple(),timestamp=datetime.now())
    await client.get_channel(logchannel).send(embed=embed)


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(permissions_error)



@client.command()
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member: discord.Member, *, nick=None):
    await ctx.message.delete()
    await member.edit(nick=nick)
    await ctx.send(str(member) + "'s nickname is now " + str(nick))
    embed= discord.Embed(title= str(ctx.author) + " changed " + str(member) + "'s nickname!", 
    description="Their nickmame is now " + str(nick),colour=discord.Colour.dark_purple(), timestamp=datetime.now())
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
async def mute(ctx, user : discord.Member, duration = 0, *, unit = None):
      role = discord.utils.get(ctx.message.guild.roles, name = mutedrole)
      await ctx.message.delete()
      await user.add_roles(role)
      if unit == "s":
          wait = 1 * duration
          msg="Muted " + str(user.mention) + " for " + str(duration) + " seconds!"
          await ctx.send(msg)
      elif unit == "m":
          wait = 60 * duration
          msg="Muted " + str(user.mention) + " for " + str(duration) + " minutes!"
          await ctx.send(msg)
      elif unit == "h":
          wait = 3600 * duration
          msg="Muted " + str(user.mention) + " for " + str(duration) + " hours!"
          await ctx.send(msg)
      else: 
        msg="Muted " + str(user.mention) + " permanently!"
        await ctx.send(msg)
      embed= discord.Embed(title= "A user has been muted!", 
      description=msg, colour=discord.Colour.dark_red(), timestamp=datetime.now())
      await client.get_channel(logchannel).send(embed=embed)
      await asyncio.sleep(wait)
      rolecheck = [role.name for role in user.roles]
      if mutedrole in rolecheck:
        await user.remove_roles(role)
        await ctx.send("{} has been unmuted!" .format(user.mention))
        embed= discord.Embed(title= str(user) + " was automatically unmuted", description=" ",colour=discord.Colour.dark_red(), timestamp=datetime.now())
        await client.get_channel(logchannel).send(embed=embed) 


@client.command()
@commands.has_permissions(ban_members=True)
async def unmute(ctx, member : discord.Member):
    role = discord.utils.get(ctx.message.guild.roles, name = mutedrole)
    await member.remove_roles(role)
    await ctx.send("Unmuted {}" .format(member.mention))
    embed= discord.Embed(title= str(ctx.author) + " unmuted " + str(member) + "!", description=" ",colour=discord.Colour.dark_red(), timestamp=datetime.now())
    await client.get_channel(logchannel).send(embed=embed)


@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(permissions_error)


@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(permissions_error)


@client.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    await ctx.message.delete()
    await member.send('You have been warned: ' + str(reason))
    await ctx.send('Warned ' + str(member) + ': ' + str(reason))
    embed= discord.Embed(
    title= str(ctx.author) + " warned " + str(member.mention) + "!", description="Reason: "+ str(reason), colour=discord.Colour.blue(),timestamp=datetime.now())
    await client.get_channel(logchannel).send(embed=embed)


@warn.error
async def warn_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(permissions_error)


@client.command()
@commands.has_permissions(administrator=True)
async def send(ctx, member : discord.Member, *, words):
  await ctx.message.delete()
  await member.send(str(words))
  await ctx.send('Sent "' + str(words) + '" to {}!' .format(member))


@send.error
async def send_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send('That user has DMs disabled!')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(permissions_error)


@client.command()
async def ping(ctx):
    ping = client.latency * 1000
    final = '%0.2f' % ping
    await ctx.send('Pong! `' + str(final) + ' ms`')


@client.command() 
async def type(ctx, *, message):
  user_regex = r"@&[a-zA-Z0-9]+"
  match = re.findall(user_regex, message)
  if match or "@everyone" in message or "@here" in message:
    await ctx.message.delete()
    await ctx.author.send('lol no')
    return
  else:
    await ctx.message.delete() 
    await ctx.channel.send(message)


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


@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, *, amount=0):
    await ctx.channel.purge(limit=amount + 1)
    embed= discord.Embed(title= str(ctx.author) + " purged " + str(amount) + " messages!", description=" ",colour=discord.Colour.gold(), timestamp=datetime.now())
    embed.add_field(name="in:" ,value= str(ctx.channel.mention), inline=True)
    await client.get_channel(logchannel).send(embed=embed)


@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(permissions_error)


@client.command()
@commands.has_permissions(manage_messages=True)
async def slowmode(ctx, seconds: int):
    await ctx.message.delete()
    await ctx.channel.edit(slowmode_delay=str(seconds))
    await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")
    embed= discord.Embed(
    title=str(ctx.author) + " changed the cooldown in " + str(ctx.channel), 
    description= "The cooldown is now: " + str(seconds) + " seconds", colour=discord.Colour.orange(), timestamp=datetime.now())
    await client.get_channel(logchannel).send(embed=embed)


@slowmode.error
async def slowmode_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(permissions_error)


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


@client.command()
async def profile(ctx, member: Member = None):
 if not member:
  member = ctx.author
 await ctx.send(member.avatar_url)


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
  embed= discord.Embed(title= str(ctx.author), description=str(message),colour=discord.Colour.blue(), timestamp=datetime.now())
  if ctx.channel == client.get_channel(botchannel):
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
  embed= discord.Embed(title= str(ctx.author) + " Changed cozyeto's status!", description= str(name),colour=discord.Colour.green(), timestamp=datetime.now())
  await client.get_channel(logchannel).send(embed=embed)


@status.error
async def status_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        msg = await ctx.send(permissions_error)
        await asyncio.sleep(5)
        await msg.delete()


@client.event
async def on_message(message):
  mainchannel = client.get_channel(wordstorychannel)
  if message.channel==mainchannel:
    if " " in message.content or "\n" in message.content:
        await message.author.send("No")
        await message.delete()
  await client.process_commands(message)
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
      def check(m):
        return message_after.author == user
      await message_after.delete()
  if role in message_after.author.roles: 
    pass
  else:
    await client.process_commands(message_after)
    embed=discord.Embed(title='A message by ' + str(message_before.author) + ' was edited!', description= "**Before:** \n" + str(message_before.content) + "\n **After:** \n" + str(message_after.content), colour=discord.Colour.orange(), timestamp=datetime.now())
    embed.add_field(name="In: ", value=str(message_before.channel.mention), inline=True)
    await client.get_channel(logchannel2).send(embed=embed)

@client.event
async def on_message_delete(message):
    embed=discord.Embed(title='A message by ' + str(message.author) + ' was deleted!', description=str(message.content), colour=discord.Colour.blue(), timestamp=datetime.now())
    embed.add_field(name="In: ", value=str(message.channel.mention), inline=True)
    await client.get_channel(logchannel2).send(embed=embed)


@client.event
async def on_raw_reaction_add(payload=None):
    msgID = 824502147507945472
    msgID2 = 824521761789837332
    guild = discord.utils.get(client.guilds, id=serverID)
    role = discord.utils.get(guild.roles, name='PingMe')
    role2 = discord.utils.get(guild.roles, name='Downtown Singaporian')
    role3 = discord.utils.get(guild.roles, name = 'Minecraft')
    singaporian = discord.utils.get(guild.roles, name = 'Singaporian')
    if payload is not None:
        if payload.message_id==msgID:
            if str(payload.emoji)=="<:cozyluna:786789373735469066>":
                await payload.member.add_roles(role)
            elif str(payload.emoji)=="<:cozyeto:786789349253447690>":
                await payload.member.add_roles(role2)
            elif str(payload.emoji)=="<:uncozyeto:805915542702653440>":
                await payload.member.add_roles(role3)
        if payload.message_id==msgID2:
            if str(payload.emoji)=="<:cozyeto:786789349253447690>":
                await payload.member.add_roles(singaporian)

@client.event
async def on_raw_reaction_remove(payload=None):
    msgID = 824502147507945472
    msgID2 = 824521761789837332
    guild = discord.utils.get(client.guilds, id=serverID)
    role = discord.utils.get(guild.roles, name='PingMe')
    role2 = discord.utils.get(guild.roles, name='Downtown Singaporian')
    role3 = discord.utils.get(guild.roles, name = 'Minecraft')
    singaporian = discord.utils.get(guild.roles, name = 'Singaporian')
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
    print('Online!')

# ____________________________________________________________________


keep_alive()
client.run(token)