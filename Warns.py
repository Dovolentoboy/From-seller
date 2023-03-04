import disnake
from disnake.ext import commands
from pymongo import MongoClient


cluster = MongoClient('mongodb+srv://Dovolentoboy:a600370@cluster0.6wxtw41.mongodb.net/test')
db = cluster.Vidacha
coll = db.users



class Warns(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        print('Варны готовы')

    
    @commands.slash_command(name='warn',description='Выдать предупреждение')
    async def warn(self,ctx,member:disnake.Member, reason = 'Не указана'):
        if member == ctx.author or member.bot:
            await ctx.send('Нельзя выдать себе пред')
        embed = disnake.Embed(
            title='Выдача предупреждения',
            description=f'Пользователю {member.mention} выдано предупреждение по причине : {reason}',

        )
        await ctx.send(embed=embed)
        embed = disnake.Embed(
            title='Выдача предупреждения',
            description=f'Вам выдано предупреждение по причине : **{reason}** просим больше так не делать'
            )
        await member.send(embed=embed)
        coll.update_one(
            {
            '_id':member.id
            },
            {
            '$inc':{
            'warns':1
            }
            }
        )
    
    @commands.slash_command(name='unwarn',description='Снять предупреждение')
    async def unwarn(self,ctx,member:disnake.Member):
        if member == ctx.author or member.bot:
            await ctx.send('Нельзя снять с себя пред')
        embed = disnake.Embed(
            title='Снятие предупреждения',
            description=f'Пользователю {member.mention} сняли предупреждение',

        )
        await ctx.send(embed=embed)
        embed = disnake.Embed(
            title='Снятие предупреждения',
            description=f'С вас снято предупреждение'
            )
        await member.send(embed=embed)
        coll.update_one(
            {
            '_id':member.id
            },
            {
            '$inc':{
            'warns':-1
            }
            }
        )


def setup(bot):
    bot.add_cog(Warns(bot))