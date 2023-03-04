import disnake
from disnake.ext import commands
from pymongo import MongoClient

cluster = MongoClient('mongodb+srv://Dovolentoboy:a600370@cluster0.6wxtw41.mongodb.net/test')
db = cluster.Vidacha
coll = db.users




class reputation(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        print('Команды репутации готовы!')




    @commands.slash_command(name='plusrep',description='Добавить репутацию')
    async def plusrep(self,ctx,member:disnake.Member,count = int()):
        embed = disnake.Embed(
            title='Выдача репутации',
            description=f'Пользователю {member.mention} выдано {count} репутации',
            color=disnake.Color.from_rgb(0,0,255)
        )
        await ctx.send(embed)
        await member.send(
            embed=disnake.Embed(
            title='Выдача репутации',
            description=f'Вам выдано {count} репутации'
            )
            )
        coll.update_one(
            {
            '_id':member.id
            },
            {
            '$inc':{
                'reputation':count
            }
            }
        )
    
    @commands.slash_command(name='minusrep',description='Снять репутацию')
    async def minusrep(self,ctx,member:disnake.Member,count = int()):
        embed = disnake.Embed(
            title='Cнятие репутации',
            description=f'Пользователю {member.mention} снято {count} репутации',
            color=disnake.Color.from_rgb(0,0,255)
        )
        await ctx.send(embed)
        await member.send(
            embed=disnake.Embed(
            title='Выдача репутации',
            description=f'С вас снято {count} репутации'
            )
            )
        coll.update_one(
            {
            '_id':member.id
            },
            {
            '$inc':{
                'reputation':-count
            }
            }
        )

def setup(bot):
    bot.add_cog(reputation(bot))