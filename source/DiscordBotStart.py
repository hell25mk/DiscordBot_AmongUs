#---------------------------------------------------------------------------------------
# bot起動する部分（イベントやコマンドは別に記述）
#
#---------------------------------------------------------------------------------------

import os, sys, discord, json
from discord.ext import commands
import Cogs.AmongUsCommands as game

bot = commands.Bot(command_prefix = "/")
botMessageChannelID = 780022724063526934

@bot.event
async def on_ready():
    game.setup(bot)
    botMessage = "Bot起動"
    channel = bot.get_channel(botMessageChannelID)
    await channel.send(botMessage)

jsonFile = os.path.dirname(__file__) + "/DiscodeApiKey.json"

with open(jsonFile) as file:
    keyData = json.load(file)
    print("Success: jsonファイルを読み込みました")

bot.run(keyData["token_key"])
