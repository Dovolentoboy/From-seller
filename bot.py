import disnake
import os
from config import TOKEN
from disnake.ext import commands
from pymongo import MongoClient

bot = commands.Bot(command_prefix='.',intents=disnake.Intents.all())


cluster = MongoClient('MONGODB LINK')
db = cluster.Vidacha
coll = db.users


@bot.event
async def on_ready():
    print(f'Бот {bot.user.name} готов к работе!')
    await bot.change_presence(status=disnake.Status.online,activity=disnake.Game(name='/shop в чат ✅'))
    

    for guild in bot.guilds:
        for member in guild.members:
            post = {
                '_id':member.id,
                'warns':0,
                'purchase':0,
                'reputation':0
            }
            if coll.count_documents({'_id':member.id}) == 0:
                coll.insert_one(post)


@bot.event
async def on_member_join(member):
    embed= disnake.Embed(
        title='Добро пожаловать в магазин',
        description='Делайте покупки на сервере. Ничего более. Никаких ролей , ничего'
    )
    await member.send(embed=embed)

    for guild in bot.guilds:
        for member in guild.members:
            post = {
                '_id':member.id,
                'warns':0,
                'purchase':0,
                'reputation':10
            }
            if coll.count_documents({'_id':member.id}) == 0:
                coll.insert_one(post)



for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and not filename.startswith("_"):
        bot.load_extension(f"cogs.{filename[:-3]}")



bot.run(TOKEN)
