import re
import os
import random
import discord
import pymongo
import asyncio
from modules.minesweeper import Game
#from modules import minesweeper as ms
from discord.ext import commands

cluster = pymongo.MongoClient(os.environ['Mongo-DB-secret'])
db = cluster["discord"]

class Fun(commands.Cog):
  """A list of fun commands"""

  def __init__(self, bot: commands.bot):
      self.bot = bot


  @commands.command(name="snipe", description="Gets the most recent deleted message within the last 30 seconds")
  async def snipe(self, ctx):
    msg = db["deleted_message"].find_one({"_id": ctx.channel.id})
    if msg == None:
      return await ctx.send("Couldn't find a message to snipe")
    attachments = msg["Attachments"]
    member = ctx.guild.get_member(msg["Author"])
    embed = discord.Embed(
        title = "Message sniped", 
        description = msg["Content"], 
        color = member.color)
    embed.set_author(
        name = member, 
        icon_url = member.avatar_url)
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
    db["deleted_message"].delete_one(msg)
    

  @commands.Cog.listener()
  async def on_message_delete(self, message):
    if message.author.id != 698344056475877397:
      data = db["deleted_message"]
      attachmentlist={}
      for i in range(0, len(message.attachments)):
        attachmentlist[f"filename{i}"]=message.attachments[i].filename
        attachmentlist[f"url{i}"]=message.attachments[i].url
      result = data.find_one({"_id": message.channel.id})
      if result:
        data.delete_one(result)
      data.insert_one({"_id": message.channel.id, "Author": message.author.id, "Content": message.content, "Attachments": attachmentlist})


  @commands.command(name="coinflip", aliases=["cf"], description="Flips a coin")
  async def coinflip(self, ctx):
      action= random.randint(0, 1)
      if(action == 0):
          flip= "Tails"
      elif(action == 1):
          flip= "Heads"
      embed= discord.Embed(title=f"{ctx.author.name} has flipped the coin!", description=f"The coin landed on {flip}!")
      await ctx.send(embed=embed)


  @commands.command(name="magic8ball", aliases=["m8b"], description="Tells your fortune")
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


  @commands.command(name="rps", description="Rock paper scissors")
  @commands.cooldown(1, 3, commands.BucketType.user)
  async def rps(self, ctx, defend):
    choices = ["r", "p", "s"]
    attack = str(random.choice(choices))
    if defend == "s" and attack == "s":
      await ctx.send("You picked `scissors`, I picked `scissors`. Draw!!")
    elif defend == "s" and attack == "r":
      await ctx.send("You picked `scissors`, I picked `rock`. You lost!")
    elif defend == "s" and attack == "p":
      await ctx.send("You picked `scissors`, I picked `paper`. You won!")
    elif defend == "p" and attack == "p":
      await ctx.send("You picked `paper`, I picked `paper`. Draw!")
    elif defend == "p" and attack == "s":
      await ctx.send("You picked `paper`, I picked `scissors`. You lost!")
    elif defend == "p" and attack == "r":
      await ctx.send("You picked `paper`, I picked `rock`. You won!")
    elif defend == "r" and attack == "r":
      await ctx.send("You picked `rock`, I picked `rock`. Draw!")
    elif defend == "r" and attack == "p":
      await ctx.send("You picked `rock`, I picked `paper`. You lost!")
    elif defend == "r" and attack == "s":
      await ctx.send("You picked `rock`, I picked `scissors`. You won!")


  @commands.command(name="tictactoe", aliases=["ttt"], description="Starts a game of Tic Tac Toe with another user or a bot")
  async def tictactoe(self, ctx, member: discord.Member=None):
    def get_computer_move(board):
      possiblemoves = [position for position in board if board[position] == "_"]
      move = None
      for symbol in ["o", "x"]:
        for position in possiblemoves:
          boardcopy = {position: board[position] for position in board}
          boardcopy[position] = symbol
          if is_winner(boardcopy, symbol):
            move = position
            return move

      if 5 in possiblemoves:
        move = 5
        return move

      edgemoves = []
      for position in possiblemoves:
        if position in [2, 4, 6, 8]:
          edgemoves.append(position)
      if edgemoves == []:
        move = random.choice(possiblemoves)
      else:
        move = random.choice(edgemoves)
      return move

    def convert(choice):
      letter = choice[0].lower()
      if letter == "a":
        add = 0
      elif letter == "b":
        add = 3
      elif letter == "c":
        add = 6
      return int(choice[1]) + add

    def is_winner(board, symbol):
      return (
      (board[1] == symbol and board[2] == symbol and board[3] == symbol) or  # top row
      (board[4] == symbol and board[5] == symbol and board[6] == symbol) or  # middle row
      (board[7] == symbol and board[8] == symbol and board[9] == symbol) or  # bottom row
      (board[1] == symbol and board[4] == symbol and board[7] == symbol) or  # first column
      (board[2] == symbol and board[5] == symbol and board[8] == symbol) or  # second column
      (board[3] == symbol and board[6] == symbol and board[9] == symbol) or  # third column
      (board[1] == symbol and board[5] == symbol and board[9] == symbol) or  # diagonal
      (board[3] == symbol and board[5] == symbol and board[7] == symbol)     # diagonal
      )

    chart = {
    1: "_", 2: "_", 3: "_",
    4: "_", 5: "_", 6: "_", 
    7: "_", 8: "_", 9: "_"
    }
    #msg = await ctx.send("Loading...")
    if member == None:
      while True:
        embed = discord.Embed(
        title = "Choose a tile",
        description = f"` 1 2 3\nA {chart[1]}|{chart[2]}|{chart[3]}\nB {chart[4]}|{chart[5]}|{chart[6]}\nC {chart[7]}|{chart[8]}|{chart[9]}`"
        )
        embed.set_footer(text="Type 'cancel' to end the game")
        #await msg.delete()
        await ctx.send(embed=embed)
        def check(message):
          return message.author == ctx.author and message.channel == ctx.channel
        x=True
        while x==True:
          tile = await self.bot.wait_for("message", check=check, timeout=30)
          if tile.content == "cancel":
            return await ctx.send("Ended the game.")
          if re.match("[abc][123]$", tile.content):
            coordinate = convert(tile.content)
            if chart[coordinate] == "_":
              chart[coordinate] = "x"
              if is_winner(chart, "x") == True:
                embed = discord.Embed(
                title = "You won!",
                description = f"`  1 2 3\nA {chart[1]}|{chart[2]}|{chart[3]}\nB {chart[4]}|{chart[5]}|{chart[6]}\nC {chart[7]}|{chart[8]}|{chart[9]}`"
                )
                return await ctx.send(embed=embed)
              x=False
            else:
              await ctx.send("That tile is already taken")
          else:
            await ctx.send("That's not a valid grid space")
        response = get_computer_move(chart)
        if response != None:
          chart[response] = "o"
          if is_winner(chart, "o"):
            embed = discord.Embed(
            title = "You lost...",
            description = f"`  1 2 3\nA {chart[1]}|{chart[2]}|{chart[3]}\nB {chart[4]}|{chart[5]}|{chart[6]}\nC {chart[7]}|{chart[8]}|{chart[9]}`"
            )
            return await ctx.send(embed=embed)
        else:
          embed = discord.Embed(
          title = "It's a tie!",
          description = f"`  1 2 3\nA {chart[1]}|{chart[2]}|{chart[3]}\nB {chart[4]}|{chart[5]}|{chart[6]}\nC {chart[7]}|{chart[8]}|{chart[9]}`"
          )
          return await ctx.send(embed=embed)
    else:
      turn = member
      symbols = {ctx.author: "x", member: "o"}
      while True:
        embed = discord.Embed(
        title = f"Choose a tile",
        description = f"`  1 2 3\nA {chart[1]}|{chart[2]}|{chart[3]}\nB {chart[4]}|{chart[5]}|{chart[6]}\nC {chart[7]}|{chart[8]}|{chart[9]}`"
        )
        embed.set_footer(text="Type 'cancel' to end the game")
        embed.set_author(name=turn, icon_url=turn.avatar_url)
        await ctx.send(embed=embed)
        def check(message):
          return message.author == turn and message.channel == ctx.channel
        x=True
        while x==True:
          tile = await self.bot.wait_for("message", check=check, timeout=60)
          if tile.content == "cancel":
            return await ctx.send("Ended the game.")
          if re.match("[abc][123]$", tile.content):
            coordinate = convert(tile.content)
            if chart[coordinate] == "_":
              chart[coordinate] = symbols[turn]
              if is_winner(chart, symbols[turn]) == True:
                embed = discord.Embed(
                title = "You won!",
                description = f"`  1 2 3\nA {chart[1]}|{chart[2]}|{chart[3]}\nB {chart[4]}|{chart[5]}|{chart[6]}\nC {chart[7]}|{chart[8]}|{chart[9]}`"
                )
                embed.set_author(name=turn, icon_url=turn.avatar_url)
                return await ctx.send(embed=embed)
              x=False
            else:
              await ctx.send("That tile is already taken")
          else:
            await ctx.send("That's not a valid grid space")
        for position in chart:
          if chart[position] == "_":
            break
        else:
          embed = discord.Embed(
          title = "It's a tie!",
          description = f"`  1 2 3\nA {chart[1]}|{chart[2]}|{chart[3]}\nB {chart[4]}|{chart[5]}|{chart[6]}\nC {chart[7]}|{chart[8]}|{chart[9]}`"
          )
          return await ctx.send(embed=embed)
        if turn == member:
          turn = ctx.author
        else:
          turn = member

  @commands.command(name="minesweeper", description="Starts a game of minesweeper", brief="instructions on how to play the game can be found here https://geekymint.com/how-to-play-minesweeper/")
  async def minesweeper(self, ctx):
    embed = discord.Embed(title = "Select your difficulty", description = ":one:: Beginner\n:two:: Easy\n:three:: Medium\n:four:: Hard")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("1️⃣")
    await msg.add_reaction("2️⃣")
    await msg.add_reaction("3️⃣")
    await msg.add_reaction("4️⃣")
    def check(reaction, member):
      return reaction.message == msg and member == ctx.author
    try:
      reaction, member = await self.bot.wait_for("reaction_add", check=check, timeout=10)
    except asyncio.TimeoutError:
      return await msg.clear_reactions()
    await msg.delete()
    minesweeper = Game(reaction.emoji)
    board = '\n'.join(minesweeper.get_board())
    embed = discord.Embed(title="Pick any tile to begin", description = f"`{board}`")
    embed.add_field(name = f"{minesweeper.difficulty} mode", value=f"Bombs left: {minesweeper.unmarked_bombs}\n", inline=False)
    embed.set_footer(text="Choose a tile by typing the letter and number like this: c3")
    message = await ctx.send(embed=embed)
    move = True
    def check(message):
        return (message.author == ctx.author) and (message.channel == ctx.channel)
    while move == True:
      try:
        msg = await self.bot.wait_for("message", check=check, timeout=20)
        x = int(minesweeper.convert(msg.content[0]))
        y = int(msg.content[1])-1
        await msg.delete()
        minesweeper.place_bombs({y: x})
        minesweeper.board[y][x].reveal(minesweeper.board)
        move = False
      except (IndexError, TypeError, ValueError, KeyError):
          await msg.delete()
          msg = await ctx.send("That's not a valid tile")
          await asyncio.sleep(5)
          await msg.delete()
      except asyncio.TimeoutError:
          return await ctx.send("Canceled command.")
    while True:
      board = "\n".join(minesweeper.get_board())
      embed = discord.Embed(title="Choose a tile", description=f"`{board}`")
      embed.add_field(name = f"{minesweeper.difficulty} mode", value=f"Bombs left: {minesweeper.unmarked_bombs}", inline=False)
      embed.set_footer(text="Type \"cancel\" to end the game, add \"flag\" at the end of your message to flag a tile")
      await message.edit(embed=embed)
      move = True
      while move == True:
        try:
          msg = await self.bot.wait_for("message", check=check, timeout=120)
          if msg.content == "cancel":
            return await ctx.send("Game canceled.")
          x = int(minesweeper.convert(msg.content[0]))
          y = int(msg.content[1])-1
          flag = bool("flag" in msg.content)
          await msg.delete()
          move = False
        except (IndexError, TypeError, ValueError, KeyError):
            await msg.delete()
            msg = await ctx.send("That's not a valid tile")
            await asyncio.sleep(5)
            await msg.delete()
        except asyncio.TimeoutError:
            return await ctx.send("Canceled command.")
      tile = minesweeper.board[y][x]
      result = minesweeper.play(tile, flag=flag)
      if result == False:
        board = "\n".join(minesweeper.get_board(showValues=True))
        embed = discord.Embed(title="Game over", description=f"`{board}`")
        embed.set_footer(text="Type 'eto minesweeper' to start a new game")
        return await ctx.send(embed=embed)
      elif result == True:
        board = "\n".join(minesweeper.get_board(showValues=True))
        embed = discord.Embed(title="You won!", description=f"`{board}`")
        embed.set_footer(text="Type 'eto minesweeper' to start a new game")
        return await ctx.send(embed=embed)

#----------------------------------------------------------------
#------------------------END COG HERE----------------------------
#----------------------------------------------------------------

def setup(bot: commands.Bot):
  bot.add_cog(Fun(bot))