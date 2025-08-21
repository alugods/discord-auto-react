import httpx
import asyncio
import discord
import json
import urllib.parse
from discord.ext import commands

with open("tokens_emojis.json", "r") as f:
    TOKEN_EMOJI_MAP = json.load(f)

TOKENS = list(TOKEN_EMOJI_MAP.keys())

TARGET_CHANNEL_ID = 1111111111111111
TARGET_USER_ID = 22222222222222222
DELAY_PER_TOKEN = 0.8 
DELAY_PER_EMOJI = 1 

bot = commands.Bot(command_prefix="!", self_bot=True)

@bot.event
async def on_ready():
    print(f"👂 Listening as {bot.user} | {len(TOKENS)} tokens loaded")

@bot.event
async def on_message(message):
    if message.channel.id != TARGET_CHANNEL_ID:
        return
    if message.author.id != TARGET_USER_ID:
        return
    if message.author.id == bot.user.id:
        return

    message_id = message.id
    channel_id = message.channel.id
    print(f"\n🟡 New message from target: {message.content}\nReacting with all tokens...")

    async def react_sequentially():
        for token, emojis in TOKEN_EMOJI_MAP.items():
            if isinstance(emojis, str): 
                emojis = [emojis]

            for emoji in emojis:
                emoji_encoded = urllib.parse.quote(emoji)
                url = f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{emoji_encoded}/@me"
                headers = {
                    "Authorization": token,
                    "User-Agent": "Mozilla/5.0",
                }

                try:
                    async with httpx.AsyncClient() as client:
                        r = await client.put(url, headers=headers)
                        print(f"✅ Token ...{token[-5:]} reacted with {emoji} → {r.status_code}")
                except Exception as e:
                    print(f"❌ Error token ...{token[-5:]} with {emoji}: {e}")

                await asyncio.sleep(DELAY_PER_EMOJI)

            await asyncio.sleep(DELAY_PER_TOKEN)

    await react_sequentially()

bot.run(TOKENS[0])

