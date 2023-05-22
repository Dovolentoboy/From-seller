import disnake
from disnake.ext import commands
from pymongo import MongoClient

cluster = MongoClient('MONGODB LINK')
db = cluster.Vidacha
coll = db.users

class Shop_commands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        print('Команды магазина готовы')



    @commands.slash_command(name='check_reput',description='Посмотреть свою статистику покупателя')
    async def check_reput(self,ctx):
        embed = disnake.Embed(
            title=f'Статистика пользователя {ctx.author.mention}',
            description='Ваши предупреждения:\n'
            f'```{coll.find_one({"_id":ctx.author.id})["warns"]}```\n'
            f'Ваши покупки\n'
            f'```{coll.find_one({"_id":ctx.author.id})["purchase"]}```\n'
            f'Ваша репутация покупателя\n'
            f'```{coll.find_one({"_id":ctx.author.id})["reputation"]}```\n'
        )
        await ctx.send(embed=embed)

    @commands.slash_command(name='checked_user',description='Команда для владельца')
    async def checked_user(self,ctx,member:disnake.Member=None):
        embed = disnake.Embed(
                title=f'Статистика пользователя {member.mention}',
                description='Ваши предупреждения:\n'
                f'```{coll.find_one({"_id":member.id})["warns"]}```\n'
                f'Ваши покупки\n'
                f'```{coll.find_one({"_id":member.id})["purchase"]}```\n'
                f'Ваша репутация покупателя\n'
                f'```{coll.find_one({"_id":member.id})["reputation"]}```\n'
            )
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Shop_commands(bot))    
