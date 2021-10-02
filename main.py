import tweepy
import discord
from discord.ext import tasks
import json
import os
from datetime import datetime, timedelta, timezone

IS_PRIME_NUMBER = 0
IS_NOT_PRIME_NUMBER = 1
JST = timezone(timedelta(hours=+9), 'JST')
KEYS = json.load(open('Prime_API_keys.json'))
CK = KEYS['CONSUMER_KEY']
CS = KEYS['CONSUMER_SECRET']
AT = KEYS['ACCESS_TOKEN']
AS = KEYS['ACCESS_SECRET']
DISCORD_TOKEN = KEYS['DISCORD_TOKEN']
# CK = os.environ['CK']
# CS = os.environ['CS']
# AT = os.environ['AT']
# AS = os.environ['AS']
# DISCORD_TOKEN = os.environ['DISCORD_TOKEN']

class NotifyPrimeNumber(discord.Client):
    def __init__(self):
        super().__init__()
        auth = tweepy.OAuthHandler(CK, CS)
        auth.set_access_token(AT, AS)
        self.api = tweepy.API(auth)

    def tweet(self, text):
        self.api.update_status(text)

    async def on_ready(self):
        for channel in self.get_all_channels():
            if str(channel.category) == 'テキストチャンネル' and channel.name == '一般':
                self.my_channel = channel
                self.check_prime_number.start()
        await print('起動しました')

    @tasks.loop(hours=24)
    async def check_prime_number(self, tz=JST):
        result = None
        now = datetime.now(tz)
        date_now = str(now)[:10].replace('-', '')
        date_now = int(date_now)

        for i in range(2, date_now):
            if date_now % i == 0:
                result = IS_NOT_PRIME_NUMBER
                break
        else:
            result = IS_PRIME_NUMBER

        if result == IS_PRIME_NUMBER:
            self.tweet(f'今日({date_now})は素数の日です！')
            await self.my_channel.send(f'今日({date_now})は素数の日です！')

    def run_bot(self, token=DISCORD_TOKEN):
        self.run(token)

app = NotifyPrimeNumber()
app.run_bot()