import disnake
from disnake.ext import commands
from pymongo import MongoClient

cluster = MongoClient('mongodb+srv://Dovolentoboy:a600370@cluster0.6wxtw41.mongodb.net/test')
db = cluster.Vidacha
coll = db.users




class purchase(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        print('Команды покупок готовы!')

    @commands.slash_command(name='pluspur',description='Добавить покупку')
    async def pluspur(self,ctx,member:disnake.Member):
        embed = disnake.Embed(
            title='Запись покупки',
            description=f'Просим прощения за доставленные неудобства . Покупка засчитана'
        )
        await member.send(embed=embed)
        coll.update_one(
            {
            '_id':member.id
            },
            {
            '$inc':{
                'purchase':1
            }
            }
        )


def setup(bot):
    bot.add_cog(purchase(bot))