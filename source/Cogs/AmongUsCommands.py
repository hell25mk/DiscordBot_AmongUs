#---------------------------------------------------------------------------------------
# イベントとコマンド群
#
#---------------------------------------------------------------------------------------

import sys
from discord.ext import commands

class AmongUs(commands.Cog):
    
    #一般ID : 779775394521415703
    #botのお部屋ID : 779990499112517632
    #bot通知 : 780022724063526934

    botRoomChannelID = 779990499112517632
    botMessageChannelID = 780022724063526934
    botMessage = ""
    survivor = []   # 生存者のIDリスト
    deceased = []   # 死亡者のIDリスト

    def __init__(self, bot):
        self.bot = bot

    # ミュートとかの変更関数
    # list ... VC設定をするUserIDリスト
    # f_mute ... サウンドミュートフラグ：True or False
    # f_deafen ... ミュートフラグ：True or False
    def voice_settings(self, *list, f_mute, f_deafen):
        for member in list:
            await member.edit(mute=f_mute)
            await member.edit(deafen=f_deafen)

    #メッセージにリアクションされたとき
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        #送信者がbotなら無視する
        #if reaction.message.author.bot:
        #    return

        self.botMessage = f"【{user.name} ({user.id})】が{reaction.emoji}を押しました"
        await reaction.message.channel.send(self.botMessage)

    #ボイスチャンネルに誰かが入退室したとき
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        channel = self.bot.get_channel(self.botMessageChannelID)
        if before.channel is None:
            self.botMessage = f"【{member.name}】が【ボイスチャンネル:{after.channel.name}】に入室しました"
            await channel.send(self.botMessage)

        if after.channel is None:
            self.botMessage = f"【{member.name}】が【ボイスチャンネル:{before.channel.name}】から退室しました"
            await channel.send(self.botMessage)
    
    #参加者募集
    @commands.command()
    async def start(self, ctx):
        self.botMessage = "プレイヤーはこちらのチャットにリアクションしてください"
        message = await ctx.send(self.botMessage)
        await message.add_reaction("\N{RAISED HAND}")
        await message.add_reaction("\N{SKULL AND CROSSBONES}")

    #タスクモード
    @commands.command()
    async def task(self, ctx):
        self.botMessage = "このコマンドで全員ミュートになる予定です"
        await ctx.send(self.botMessage)

        # 生存者は話せないし聞こえない
        # 死んだ人は話せる
        self.voice_settings(self, self.survivor, True, True)
        self.voice_settings(self, self.deceased, False, False)

    #会議モード
    @commands.command()
    async def talk(self, ctx):
        self.botMessage = "このコマンドで死んでる人以外のミュートを解除する予定です"
        await ctx.send(self.botMessage)

        # 生存者は話せる
        # 死んだ人は話せない
        self.voice_settings(self, self.survivor, False, False)
        self.voice_settings(self, self.deceased, True, False)

    #bot終了
    @commands.command()
    async def stop(self, ctx):
        try:
            botMessage = "Bot終了"
            channel = self.bot.get_channel(self.botMessageChannelID)
            await channel.send(botMessage)
            #例外エラー出るけど現状どうしようもない
            await self.bot.logout()
        except:
            print("EnvironmentError")
            self.bot.clear()
            print("Bot Clear")

def setup(bot):
    bot.add_cog(AmongUs(bot))

