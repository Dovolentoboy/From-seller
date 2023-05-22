import disnake
from disnake.ext import commands
from typing import Optional
from pymongo import MongoClient


cluster = MongoClient('MONGODB LINK')
db = cluster.Vidacha
coll = db.users



class oplata_check_bariga(disnake.ui.View):
    def __init__ (self):
        super().__init__(timeout=None)
        self.value : Optional[bool] = None

    @disnake.ui.button(label='Да,оплатил',style=disnake.ButtonStyle.green)
    async def yep_oplata(self,button:disnake.Button,interaction:disnake.Interaction):
        await interaction.send(content='Выдаю +rep и +покупку')
        self.value = True
        self.stop()
    
    @disnake.ui.button(label='Не оплатил',style=disnake.ButtonStyle.danger)
    async def nope_oplata(self,button:disnake.Button,interaction:disnake.Interaction):
        await interaction.send(content='Выдаю пред и -rep')
        self.value = False
        self.stop()


class checked_oplata(disnake.ui.View):
    def __init__ (self):
        super().__init__(timeout=None)
        self.value : Optional[bool]=None


    @disnake.ui.button(label='Оплатил',style=disnake.ButtonStyle.green)
    async def ne_oplatil_button(self,button:disnake.Button,interaction:disnake.Interaction):
        view = oplata_check_bariga()
        category = interaction.guild.get_channel(1081323038076846222)
        channel = await interaction.guild.create_text_channel(name=f'Покупка пользователя {interaction.user}  {interaction.user.id}',category=category,position=1)
        embed = disnake.Embed(
            title='Проверка оплаты',
            description=f'<@839490293447524384>, оплатил ли {interaction.user} свой заказ?'
        )
        await channel.send(content='<@839490293447524384>')
        await channel.send(embed=embed,view=view)
        await interaction.send(content='✅',ephemeral=True)
        await view.wait()
        if view.value:
           embed = disnake.Embed(
               title='Оплата успешна',
               description='Вашу оплату заметил продавец. +rep \n' 
                                       'Скоро вам напишут , ожидайте ⌛'
           )
           url = 'https://cdn.discordapp.com/attachments/1059163568915890316/1081322038704214077/pngtree-shop-icon-in-neon-style-png-image_2071229.jpg'
           embed.set_thumbnail(url=url)
           await interaction.user.send(embed=embed)
           coll.update_one(
            {
            '_id':interaction.user.id
            },
            {
            '$inc':{
                'reputation':1,
                'purchase': 1
            }
            }
        )
        else:
            embed = disnake.Embed(
                title='Выдача предупреждения',
                description='Это заготовленное сообщение для пользователей бота\n'
                                    'Т.к вы нажали на кнопку "Я оплатил",но оплаты не поступило. Думаю стоит задуматься о своем повидении\n '
                                    'Вам выносится первое предупреждение . За последующие разы наказание будет строже.\n '
                                    'С любовью создатель сервера '
            )
            url = 'https://cdn.discordapp.com/attachments/1059163568915890316/1081322038704214077/pngtree-shop-icon-in-neon-style-png-image_2071229.jpg'
            embed.set_thumbnail(url=url)
            await interaction.user.send(embed=embed)
            coll.update_one(
            {
            '_id':interaction.user.id
            },
            {
            '$inc':{
                'warns':1,
                'reputation':-1
            }
            }
        )
            
        self.value = False
        self.stop()
    
    @disnake.ui.button(label='Не Оплатил',style=disnake.ButtonStyle.danger)
    async def oplatil_button(self,button:disnake.Button,interaction:disnake.Interaction):
        await interaction.send(content='✅',ephemeral=True)
        self.value = True
        self.stop()



class confirmation(disnake.ui.View):
    def __init__ (self):
        super().__init__(timeout=20)
        self.value : Optional[bool]=None


    @disnake.ui.button(emoji='✅')
    async def yes_button(self,button:disnake.Button,interaction:disnake.Interaction):
        self.value = True
        self.stop()
    

    @disnake.ui.button(emoji='❌')
    async def cansel_button(self,button:disnake.Button,interaction:disnake.Interaction):
        self.value = False
        self.stop()


class button_shop(disnake.ui.View):
    def __init__ (self):
        super().__init__(timeout=300)
        self.value: Optional[bool] = None
    

    @disnake.ui.button(label='Магазин',emoji='🧺')
    async def magazine(self,button:disnake.Button,interaction:disnake.Interaction):
        view = purchases_button()
        embed = disnake.Embed(
            title='Секс шоп "Анал Максима"',
            description=f'Ниже представлены товары,которые вы можете купить'
        )
        await interaction.send(embed=embed,view=view)
        





class purchases_button(disnake.ui.View):
    def __init__ (self):
        super().__init__(timeout=None)
        self.value: Optional[bool] = None
    

    @disnake.ui.button(label='Нитро 400 руб',style=disnake.ButtonStyle.blurple)
    async def vibrator_button(self,button:disnake.Button,interaction:disnake.Interaction,style=disnake.ButtonStyle.blurple):
        view = confirmation()
        view2 = checked_oplata()
        embed = disnake.Embed(
            title='Нитро',
            description='Вы точно хотите купить данный товар?'
        )
        await interaction.send(embed=embed,view=view,ephemeral=True)
        await view.wait()



        #писанина с принятием
        if view is None:
            await interaction.delete_original_message(delay=1)
            await interaction.send(content='Вы не успели',ephemeral=True)

        elif view.value:
            embed = disnake.Embed(
                title='Нитро',
                description='Теперь вы должны оплатить, у вас 5 минут. В комментариях к оплате укажите свой Discord tag и id. Хотя первого будет достаточно\n'
                'В случае если вы нажали кнопку "не оплатил" случайно, вам потребуется доказать случай оплаты.\n'
                'Мои реквизиты:\n'
                'Тут типо карта\n'
                'Еще какая-то херня',
                color=disnake.Color.from_rgb(0,0,255)
                )
            url = 'https://cdn.discordapp.com/attachments/1059163568915890316/1081322038704214077/pngtree-shop-icon-in-neon-style-png-image_2071229.jpg'
            embed.set_thumbnail(url=url)
            await interaction.delete_original_message(delay=1) 
            await interaction.send(embed=embed,ephemeral=True,view=view2)
            await view2.wait()
            if view2 is None:
                await interaction.delete_original_message(delay=1)
                await interaction.send(content='Вы не успели',ephemeral=True)
            elif view2.value:
                await interaction.delete_original_message(delay=1)
                await interaction.send(content='Ну как бы да. Иди дальше смотри,что хочешь,проверяльщик)',ephemeral=True)
                
            else:
                await interaction.delete_original_message(delay=1)
                await interaction.send(content='Продавец все проверил и вам в личные сообщение пришло уведомление о результате. Советую ознакомиться',ephemeral=True)
   
        else:
            embed = disnake.Embed(
                title='Продолжайте покупки',
                description='Удачи с выбором)',
                color=disnake.Color.from_rgb(0,0,255)
            )
            url = 'https://cdn.discordapp.com/attachments/1059163568915890316/1081322038704214077/pngtree-shop-icon-in-neon-style-png-image_2071229.jpg'
            embed.set_thumbnail(url=url)
            await interaction.delete_original_message(delay=1)
            await interaction.send(embed=embed,ephemeral=True)
    
    @disnake.ui.button(label='Горничная Максим 1000 руб',style=disnake.ButtonStyle.blurple)
    async def putana_button(self,button:disnake.Button,interaction:disnake.Interaction,style=disnake.ButtonStyle.blurple):
        view = confirmation()
        view2 = checked_oplata()
        embed = disnake.Embed(
            title='Горничная',
            description='Вы точно хотите купить данный товар?'
        )
        await interaction.send(embed=embed,view=view,ephemeral=True)
        await view.wait()



        #писанина с принятием
        if view is None:
            await interaction.delete_original_message(delay=1)
            await interaction.send(content='Вы не успели',ephemeral=True)

        elif view.value:
            embed = disnake.Embed(
                title='Горничная',
                description='Теперь вы должны оплатить, у вас 5 минут. В комментариях к оплате укажите свой Discord tag и id. Хотя первого будет достаточно\n'
                'В случае если вы нажали кнопку "не оплатил" случайно, вам потребуется доказать случай оплаты.\n'
                'Мои реквизиты:\n'
                'Тут типо карта\n'
                'Еще какая-то херня',
                color=disnake.Color.from_rgb(0,0,255)
                )
            url = 'https://cdn.discordapp.com/attachments/1059163568915890316/1081322038704214077/pngtree-shop-icon-in-neon-style-png-image_2071229.jpg'
            embed.set_thumbnail(url=url)
            await interaction.delete_original_message(delay=1) 
            await interaction.send(embed=embed,ephemeral=True,view=view2)

            #внутри писанины еще писанина
            await view2.wait()
            if view2 is None:
                await interaction.delete_original_message(delay=1)
                await interaction.send(content='Вы не успели',ephemeral=True)
            elif view2.value:
                await interaction.delete_original_message(delay=1)
                await interaction.send(content='Ну как бы да. Иди дальше смотри,что хочешь,проверяльщик)',ephemeral=True)
                
            else:
                await interaction.delete_original_message(delay=1)
                await interaction.send(content='Продавец все проверил и вам в личные сообщение пришло уведомление о результате. Советую ознакомиться',ephemeral=True)
   
        else:
            embed = disnake.Embed(
                title='Продолжайте покупки',
                description='Удачи с выбором)',
                color=disnake.Color.from_rgb(0,0,255)
            )
            url = 'https://cdn.discordapp.com/attachments/1059163568915890316/1081322038704214077/pngtree-shop-icon-in-neon-style-png-image_2071229.jpg'
            embed.set_thumbnail(url=url)
            await interaction.delete_original_message(delay=1)
            await interaction.send(embed=embed,ephemeral=True)
        
        
            
    @disnake.ui.button(label='Интимки Максима 1669 руб',style=disnake.ButtonStyle.blurple)
    async def intim_button(self,button:disnake.Button,interaction:disnake.Interaction):
        view = confirmation()
        view2 = checked_oplata()
        embed = disnake.Embed(
            title='Интимки',
            description='Вы точно хотите купить данный товар?'
        )
        await interaction.send(embed=embed,view=view,ephemeral=True)
        await view.wait()



        #писанина с принятием
        if view is None:
            await interaction.delete_original_message(delay=1)
            await interaction.send(content='Вы не успели',ephemeral=True)

        elif view.value:
            embed = disnake.Embed(
                title='Интимки',
                description='Теперь вы должны оплатить, у вас 5 минут. В комментариях к оплате укажите свой Discord tag и id. Хотя первого будет достаточно\n'
                'В случае если вы нажали кнопку "не оплатил" случайно, вам потребуется доказать случай оплаты.\n'
                'Мои реквизиты:\n'
                'Тут типо карта\n'
                'Еще какая-то херня',
                color=disnake.Color.from_rgb(0,0,255)
                )
            url = 'https://cdn.discordapp.com/attachments/1059163568915890316/1081322038704214077/pngtree-shop-icon-in-neon-style-png-image_2071229.jpg'
            embed.set_thumbnail(url=url)
            await interaction.delete_original_message(delay=1) 
            await interaction.send(embed=embed,ephemeral=True,view=view2)

            #внутри писанины еще писанина
            await view2.wait()
            if view2 is None:
                await interaction.delete_original_message(delay=1)
                await interaction.send(content='Вы не успели',ephemeral=True)
            elif view2.value:
                await interaction.delete_original_message(delay=1)
                await interaction.send(content='Ну как бы да. Иди дальше смотри,что хочешь,проверяльщик)',ephemeral=True)
                
            else:
                await interaction.delete_original_message(delay=1)
                await interaction.send(content='Продавец все проверил и вам в личные сообщение пришло уведомление о результате. Советую ознакомиться',ephemeral=True)
   
        else:
            embed = disnake.Embed(
                title='Продолжайте покупки',
                description='Удачи с выбором)',
                color=disnake.Color.from_rgb(0,0,255)
            )
            url = 'https://cdn.discordapp.com/attachments/1059163568915890316/1081322038704214077/pngtree-shop-icon-in-neon-style-png-image_2071229.jpg'
            embed.set_thumbnail(url=url)
            await interaction.delete_original_message(delay=1)
            await interaction.send(embed=embed,ephemeral=True)
        
    
   

class shop_commands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot 
        print('Кнопки магазина готовы')

    @commands.slash_command(name='shop',)
    async def shop(self,ctx):
        view=button_shop()
        embed = disnake.Embed(
            title='Магазин различных приблуд',
            description='Чтобы купить что-то нажмите кнопку ниже'
        )
        await ctx.send(embed=embed,view=view)








def setup(bot):
    bot.add_cog(shop_commands(bot))
