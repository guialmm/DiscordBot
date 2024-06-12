import discord
import random
import yt_dlp as youtube_dl
import asyncio
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

pessoa = 383979046507249675
emoji_macaco = "🐵"

queues = {}

@bot.event
async def on_ready():
    print("O bot está pronto.")

@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return

    if msg.author.id == pessoa:
        await msg.add_reaction(emoji_macaco)

    username = msg.author.display_name

    if msg.content == "salve":
        await msg.channel.send("salve, " + username)

    await bot.process_commands(msg)

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def dado(ctx, maximo: int):
    await ctx.send(random.randint(1, maximo))

@bot.command()
async def coinflip(ctx):
    await ctx.send(random.choice(["Cara", "Coroa"]))

@bot.remove_command('help')
@bot.command(aliases=['ajuda'])
async def help(ctx):
    MyEmbed = discord.Embed(title="Comandos do Bot", description="Lista de comandos disponíveis", color=discord.Color.dark_purple())
    MyEmbed.add_field(name="!ping", value="Retorna Pong!", inline=False)
    MyEmbed.add_field(name="!dado <maximo>", value="Rola um dado do número máximo que você escolhe", inline=False)
    MyEmbed.add_field(name="!coinflip", value="Joga uma moeda", inline=False)
    MyEmbed.add_field(name="!clear <quantidade>", value="Apaga a quantidade de mensagens que você escolher", inline=False)
    MyEmbed.add_field(name="!edit servername <nome>", value="Altera o nome do servidor", inline=False)
    MyEmbed.add_field(name="!kick <membro> <motivo>", value="Expulsa um membro do servidor", inline=False)
    MyEmbed.add_field(name="!ban <membro> <motivo>", value="Bane um membro do servidor", inline=False)
    MyEmbed.add_field(name="!unban <membro>", value="Desbane um membro do servidor", inline=False)
    MyEmbed.add_field(name="!mute <membro>", value="Muta o microfone de um membro do servidor", inline=False)
    MyEmbed.add_field(name="!unmute <membro>", value="Desmuta o microfone de um membro do servidor", inline=False)
    MyEmbed.add_field(name="!mutefone <membro>", value="Muta o fone de um membro do servidor", inline=False)
    MyEmbed.add_field(name="!unmutefone <membro>", value="Desmuta o fone de um membro do servidor", inline=False)
    MyEmbed.add_field(name="!voicekick <membro>", value="Expulsa um membro do canal de voz", inline=False)
    await ctx.send(embed=MyEmbed)

@bot.command(aliases=['limpar', 'apagar'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, quantidade: int):
    if quantidade < 1 or quantidade > 100:
        await ctx.send("O limite de mensagens foi atingido, só consigo apagar entre 1 e 100 mensagens por vez.")
        return
    quantidade = min(quantidade, 100)
    await ctx.send(f"Apagando o chat em {quantidade} mensagens...")
    await ctx.channel.purge(limit=quantidade)
    await ctx.send(f"{ctx.author.mention}, {quantidade} mensagens foram apagadas.")

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Você não tem permissão para executar esse comando.")

@bot.event
async def on_member_join(member):
    guild = member.guild
    guildname = guild.name
    dmchannel = await member.create_dm()
    await dmchannel.send(f"Bem-vindo a {guildname}, {member.display_name}!")

@bot.group()
async def edit(ctx):
    pass

@edit.command()
@commands.has_permissions(manage_guild=True)
async def servername(ctx, *, name):
    await ctx.guild.edit(name=name)
    await ctx.send(f"Nome do servidor alterado para {name}")

@servername.error
async def servername_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Você não tem permissão para executar esse comando.")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member.display_name} foi kickado do servidor.")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Você não tem permissão para executar esse comando.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member.display_name} foi banido do servidor.")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Você não tem permissão para executar esse comando.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member=None):
    if member is None:
        await ctx.send("Uso: !unban <ID do usuário ou nome do usuário>")
        return

    try:
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"{user.name}#{user.discriminator} foi desbanido do servidor.")
                return

        await ctx.send(f"{member} não foi encontrado na lista de banidos.")
    except Exception as e:
        await ctx.send(f"Ocorreu um erro ao tentar desbanir {member}.")

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Você não tem permissão para executar esse comando.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def mute(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send("Por favor, mencione um membro para mutar.")
        return

    await member.edit(mute=True)
    await ctx.send(f"{member.display_name} foi mutado.")

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Você não tem permissão para executar esse comando.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def unmute(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send("Por favor, mencione um membro para desmutar.")
        return

    await member.edit(mute=False)
    await ctx.send(f"{member.display_name} foi desmutado.")

@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Você não tem permissão para executar esse comando.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def mutefone(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send("Por favor, mencione um membro para mutar o fone.")
        return

    await member.edit(deafen=True)
    await ctx.send(f"{member.display_name} teve o fone mutado.")

@mutefone.error
async def mutefone_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Você não tem permissão para executar esse comando.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def unmutefone(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send("Por favor, mencione um membro para desmutar o fone.")
        return

    await member.edit(deafen=False)
    await ctx.send(f"{member.display_name} teve o fone desmutado.")

@unmutefone.error
async def unmutefone_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Você não tem permissão para executar esse comando.")

@bot.command()
@commands.has_permissions(move_members=True)
async def voicekick(ctx, member: discord.Member):
    if member.voice is None:
        await ctx.send("Esse membro não está em um canal de voz.")
        return

    await member.move_to(None)
    await ctx.send(f"{member.display_name} foi expulso do canal de voz.")

@voicekick.error
async def voicekick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Você não tem permissão para executar esse comando.")

@bot.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("Você precisa estar em um canal de voz para usar esse comando.")
        return

    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()
        await ctx.send("Conectado ao canal de voz.")
    else:
        await ctx.voice_client.move_to(voice_channel)
        await ctx.send("Movido para o canal de voz.")

# Definição da função play_next
async def play_next(ctx):
    guild_id = ctx.guild.id
    voice_client = ctx.voice_client

    if guild_id in queues and queues[guild_id]:
        audio_url = queues[guild_id].pop(0)
        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        voice_client.play(discord.FFmpegPCMAudio(audio_url, **ffmpeg_options), after=lambda e: bot.loop.create_task(play_next(ctx)))
    else:
        await asyncio.sleep(300)
        if guild_id in queues and not queues[guild_id] and not voice_client.is_playing():
            await voice_client.disconnect()

@bot.command()
async def play(ctx, *, query):
    if ctx.author.voice is None:
        await ctx.send("Você precisa estar em um canal de voz para usar esse comando.")
        return

    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()
        await ctx.send("Conectado ao canal de voz.")

    guild_id = ctx.guild.id
    voice_client = ctx.voice_client

    # Verifica se a entrada é uma URL ou um título de música
    if "youtube.com" in query or "youtu.be" in query:
        url = query
    else:
        # Se for um título de música, pesquisa no YouTube
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            }
            # Pesquisa no YouTube pelo título fornecido
            search_query = f"ytsearch1:{query}"
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(search_query, download=False)
                url = info['entries'][0]['url']  # Pega o link da primeira entrada dos resultados

        except youtube_dl.utils.DownloadError:
            await ctx.send("Ocorreu um erro ao tentar extrair a URL do vídeo. Certifique-se de que o título está correto.")
            return

    if guild_id not in queues:
        queues[guild_id] = []

    queues[guild_id].append(url)

    if not voice_client.is_playing():
        await play_next(ctx)

@bot.command()
async def skip(ctx):
    if ctx.voice_client is not None:
        ctx.voice_client.stop()
        await play_next(ctx)

@bot.command()
async def pause(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.pause()

@bot.command()
async def resume(ctx):
    if ctx.voice_client.is_paused():
        ctx.voice_client.resume()

@bot.command()
async def stop(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()

@bot.command()
async def queue(ctx):
    guild_id = ctx.guild.id
    if guild_id in queues and queues[guild_id]:
        queue_list = ""
        for index, audio_url in enumerate(queues[guild_id]):
            try:
                ydl_opts = {
                    'quiet': True,
                    'skip_download': True,
                    'extract_flat': True,
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(audio_url, download=False)
                    title = info.get('title', 'Desconhecido')
                queue_list += f"{index + 1}. {title}\n"
            except Exception as e:
                queue_list += f"{index + 1}. Desconhecido\n"
        
        embed = discord.Embed(title="Lista de músicas na fila", description=queue_list, color=discord.Color.blue())
        await ctx.send(embed=embed)
    else:
        await ctx.send("Não há músicas na fila.")


bot.run("MTI0ODM2NTUyNzI2MTI1MzcyMw.G0oyAA.41Pdmej82LOkdfKUILwGXSO-cq7G0I6Y2sBdOw")
