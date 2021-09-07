import discord
import os
import pymongo
from discord.ext import commands
from keep_alive import keep_alive


intents = discord.Intents.default()
allowed_mentions = discord.AllowedMentions(everyone=False, roles=False)
intents.members = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or('eto '), intents=intents, help_command=None, allowed_mentions = allowed_mentions)
token = os.environ.get("Bot_Token")
db = pymongo.MongoClient(os.environ['Mongo-DB-secret'])
if db:
    print("Successfully connected to Singapore database.")
else:
    raise "Could not connect to Singapore database"

for extension in os.listdir("extensions"):
  if extension.endswith(".py"):
    bot.load_extension(f"extensions.{extension[:len(extension)-3]}")

@bot.command(name="reload", description="Reloads an extension")
@commands.has_permissions(administrator=True)
async def reload(ctx, extension=None):
  if extension==None:
      for extension in bot.extensions.copy():
        bot.reload_extension(f"extensions.{extension}")
      await ctx.send("Reloaded cozyeto")
      print("Reloaded cozyeto")
  else:
      bot.reload_extension(f"extensions.{extension}")
      await ctx.send("Done")
      print(f"Reloaded {extension}")


@reload.error
async def reload_error(ctx, error):
  if isinstance(error, commands.ExtensionNotFound):
    await ctx.send("Could not find that cog")
  else:
    await ctx.send("Could not reload that cog")
    raise error


@bot.event
async def on_ready():
  print('Online!')


keep_alive()
bot.run(token)