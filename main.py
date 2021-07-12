from keep_alive import keep_alive
import discord 
import os
import json
from discord.ext import commands

intents = discord.Intents.default()
allowed_mentions = discord.AllowedMentions(everyone=False, roles=False)
intents.members = True
command_prefix = 'eto ', 'Eto '
bot = commands.Bot(command_prefix='eto ', intents=intents, help_command=None, allowed_mentions = allowed_mentions)
token = os.environ.get("DISCORD_BOT_SECRET")

bot.load_extension("commands")
bot.load_extension("log_module")
bot.load_extension("modmail_module")

@bot.command(name="reload", description="Reloads a cog", usage="eto reload (cog name)")
@commands.has_permissions(administrator=True)
async def reload(ctx, cog=None):
  if cog==None:
      for extension in bot.extensions:
        bot.reload_extension(extension)
      await ctx.send("Reloaded cozyeto")
      print("Reloaded cozyeto")
  else:
      bot.reload_extension(cog)
      await ctx.send("Done")
      print(f"Reloaded {cog}")

@reload.error
async def reload_error(ctx, error):
  await ctx.send("Could not reload that cog")
  raise error


@bot.event
async def on_ready():
  with open("data/invites.json") as f:
    invites = json.load(f)
    for guild in bot.guilds:
      for invite in await guild.invites():
        invites[invite.code] = invite.uses
    i = []
    for invite in invites:
      if invite not in {inv.code for inv in await guild.invites()}:
        i.append(invite)
    for item in i:
      invites.pop(item)
  with open("data/invites.json", "w") as f:
    json.dump(invites, f)
  print('Online!')


keep_alive()
bot.run(token)
