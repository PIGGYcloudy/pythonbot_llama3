from dotenv import load_dotenv
import os
import discord
from discord import Intents, Client, Message
from discord.ext import commands

import response

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
URL = os.getenv('URL')

bot = commands.Bot(command_prefix='!', intents=Intents.all())

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('Message was empty because intents were not enabled probably')
        return
    
    is_private = user_message[0] == '?'
    if is_private:
        user_message = user_message[1:]

    try:
        bot_response = response.get_response(user_message)
        await message.author.send(bot_response) if is_private else await message.channel.send(bot_response)
    except Exception as e:
        print(e)

@bot.command()
async def emo(ctx):
    def check(msg):
        return msg.author == ctx.author
    
    await ctx.send('Initializing...It may takes about 3 minutes...\n\"exit\" to end the conversation.')
    get_emo_response = response.get_response()
    await ctx.send(next(get_emo_response))
    while True:
        # 等待使用者回覆訊息
        message = await bot.wait_for('message', check=check)

        if message.content.lower() == 'exit':
            await ctx.send(get_emo_response.send(message.content))
            break

        try:
            # 根據生成器的回應進行回覆
            bot_response = get_emo_response.send(message.content)
            if bot_response:
                await ctx.send(bot_response)
            else:
                await ctx.send("Error: Empty response from the generator.")
                break
        except StopIteration:
            # 如果生成器結束了，可以選擇終止或重新開始
            await ctx.send("No more responses left.")
            break
    # global on_msg
    # on_msg = True
    # @bot.event
    # async def on_message(message: Message):
    #     global on_msg
    #     if not on_msg:
    #         return
    #     if message.author == bot.user:
    #         return
    #     try:
    #         await message.channel.send(get_emo_response.send(message.content))
    #     except StopIteration:
    #         await message.channel.send("再見掰掰~")
    #         on_msg = False

@bot.event
async def on_ready():
    print(f'\n{bot.user} is now running\nInvite Link -> {URL}\n')


def main():
    global on_msg
    on_msg = False
    bot.run(token=TOKEN)

if __name__ == '__main__':
    main()