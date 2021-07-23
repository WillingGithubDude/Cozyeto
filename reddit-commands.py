import os
import asyncpraw
import discord
import random
from discord.ext import commands

reddit = asyncpraw.Reddit(
  client_id='Di6v2QIrEy8qdwvL3evwSQ',
  client_secret=os.environ['reddit-app-secret'],
  user_agent='u/willing-reddit-dude | discord bot: https://replit.com/@WillingDude/Cozyeto')

class NSFW(commands.Cog):
  """NSFW commands"""

  def __init__(self, bot:commands.Bot):
      self.bot = bot

  @commands.group(name="nsfw", description="A command group used for NSFW commands", usage="eto nsfw (subcommand)", invoke_without_command=True)
  async def nsfw(self, ctx):
    if ctx.invoked_subcommand==None:
      if ctx.channel.is_nsfw():
        await ctx.invoke(self.bot.get_command("nsfw pic"))
      else:
        await ctx.send("This command can only be used in a channel marked as NSFW")

  @nsfw.command(name="pic", description="Sends a naughty image from r/gonewild", usage="eto nsfw pic", aliases=("image", "picture"))
  async def pic(self, ctx):
    if ctx.channel.is_nsfw():
      subreddit = await reddit.subreddit('gonewild')
      post_list = [post async for post in subreddit.new() if post.stickied==False and post.url.startswith("https://i.imgur.com") and post.url.endswith(".jpg")]
      submission = random.choice(post_list)
      embed=discord.Embed(title=submission.title, url=f"https://www.reddit.com{submission.permalink}")
      print(submission.url)
      embed.set_footer(text=f"{submission.score} upvotes, {submission.num_comments} comments")
      embed.set_image(url=submission.url)
      await ctx.send(embed=embed)
    else:
      await ctx.send("This command can only be used in a channel marked as NSFW")

  @nsfw.command(name="gif", description="Sends a naughty gif from r/gifsgonewild", usage="eto nsfw gif")
  async def gif(self, ctx):
    if ctx.channel.is_nsfw():
      subreddit = await reddit.subreddit('gifsgonewild')
      post_list = [post async for post in subreddit.new() if post.stickied==False]
      submission = random.choice(post_list)
      embed=discord.Embed(title=submission.title, url=f"https://www.reddit.com{submission.permalink}")
      print(submission.url)
      embed.set_footer(text=f"{submission.score} upvotes, {submission.num_comments} comments")
      await ctx.send(embed=embed)
      await ctx.send(submission.url)
    else:
      await ctx.send("This command can only be used in a channel marked as NSFW")
    

  @nsfw.command(name="cumslut", description="Sends a naughty image from r/cumsluts", usage="eto nsfw cumslut", aliases=("cumsluts", "cum"))
  async def cumslut(self, ctx):
    if ctx.channel.is_nsfw():
      subreddit = await reddit.subreddit('cumsluts')
      post_list = [post async for post in subreddit.new() if post.stickied==False and post.url.startswith("https://i.imgur.com") and post.url.endswith(".jpg")]
      submission = random.choice(post_list)
      embed=discord.Embed(title=submission.title, url=f"https://www.reddit.com{submission.permalink}")
      print(submission.url)
      embed.set_image(url=submission.url)
      embed.set_footer(text=f"{submission.score} upvotes, {submission.num_comments} comments")
      await ctx.send(embed=embed)
    else:
      await ctx.send("This command can only be used in a channel marked as NSFW")

  

def setup(bot: commands.Bot):
    bot.add_cog(NSFW(bot))