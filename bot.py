import discord
import random
import yt_dlp as youtube_dl
import asyncio
import subprocess
import json
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

id_do_servidor = SEU_ID
guild_object = discord.Object(id=id_do_servidor)

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await self.tree.sync(guild=guild_object)
            self.synced = True
        print(f"Entramos como {self.user}.")

@bot.tree.command(guild=guild_object, name="ping", description="Retorna Pong!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@bot.tree.command(guild=guild_object, name="dado", description="Rola um dado com o número máximo especificado.")
@app_commands.describe(maximo="Número máximo do dado")
async def dado(interaction: discord.Interaction, maximo: int):
    await interaction.response.send_message(str(random.randint(1, maximo)))

@bot.tree.command(guild=guild_object, name="coinflip", description="Joga uma moeda.")
async def coinflip(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(["Cara", "Coroa"]))

@bot.tree.command(guild=guild_object, name="help", description="Mostra a lista de comandos disponíveis.")
async def help(interaction: discord.Interaction):
    MyEmbed = discord.Embed(title="Comandos do Bot", description="Lista de comandos disponíveis", color=discord.Color.dark_purple())
    MyEmbed.add_field(name="/ping", value="Retorna Pong!", inline=False)
    MyEmbed.add_field(name="/dado <maximo>", value="Rola um dado do número máximo que você escolhe", inline=False)
    MyEmbed.add_field(name="/coinflip", value="Joga uma moeda", inline=False)
    MyEmbed.add_field(name="/clear <quantidade>", value="Apaga a quantidade de mensagens que você escolher", inline=False)
    MyEmbed.add_field(name="/edit_servername <nome>", value="Altera o nome do servidor", inline=False)
    MyEmbed.add_field(name="/kick <membro> <motivo>", value="Expulsa um membro do servidor", inline=False)
    MyEmbed.add_field(name="/ban <membro> <motivo>", value="Bane um membro do servidor", inline=False)
    MyEmbed.add_field(name="/unban <membro>", value="Desbane um membro do servidor", inline=False)
    MyEmbed.add_field(name="/mute <membro>", value="Muta o microfone de um membro do servidor", inline=False)
    MyEmbed.add_field(name="/unmute <membro>", value="Desmuta o microfone de um membro do servidor", inline=False)
    MyEmbed.add_field(name="/mutefone <membro>", value="Muta o fone de um membro do servidor", inline=False)
    MyEmbed.add_field(name="/unmutefone <membro>", value="Desmuta o fone de um membro do servidor", inline=False)
    MyEmbed.add_field(name="/voicekick <membro>", value="Expulsa um membro do canal de voz", inline=False)
    await interaction.response.send_message(embed=MyEmbed)

@bot.tree.command(guild=guild_object, name="clear", description="Apaga uma quantidade de mensagens.")
@app_commands.describe(quantidade="Quantidade de mensagens a serem apagadas (entre 1 e 100)")
@commands.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, quantidade: int):
    if quantidade < 1 or quantidade > 100:
        await interaction.response.send_message("O limite de mensagens foi atingido, só consigo apagar entre 1 e 100 mensagens por vez.")
        return
    quantidade = min(quantidade, 100)
    await interaction.channel.purge(limit=quantidade)
    await interaction.response.send_message(f"{quantidade} mensagens foram apagadas.", ephemeral=True)

@bot.tree.error
async def clear_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)

@bot.event
async def on_member_join(member):
    guild = member.guild
    guildname = guild.name
    dmchannel = await member.create_dm()
    await dmchannel.send(f"Bem-vindo a {guildname}, {member.display_name}!")

@bot.tree.command(guild=guild_object, name="edit_servername", description="Altera o nome do servidor.")
@app_commands.describe(name="Novo nome do servidor")
@commands.has_permissions(manage_guild=True)
async def servername(interaction: discord.Interaction, name: str):
    await interaction.guild.edit(name=name)
    await interaction.response.send_message(f"Nome do servidor alterado para {name}")

@bot.tree.error
async def servername_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)

@bot.tree.command(guild=guild_object, name="kick", description="Expulsa um membro do servidor.")
@app_commands.describe(member="Membro a ser expulso", reason="Razão da expulsão")
@commands.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    await member.kick(reason=reason)
    await interaction.response.send_message(f"{member.display_name} foi kickado do servidor.")

@bot.tree.error
async def kick_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)

@bot.tree.command(guild=guild_object, name="ban", description="Bane um membro do servidor.")
@app_commands.describe(member="Membro a ser banido", reason="Razão do banimento")
@commands.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    await member.ban(reason=reason)
    await interaction.response.send_message(f"{member.display_name} foi banido do servidor.")

@bot.tree.error
async def ban_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)

@bot.tree.command(guild=guild_object, name="unban", description="Desbane um membro do servidor.")
@app_commands.describe(member="ID ou nome do membro a ser desbanido")
@commands.has_permissions(ban_members=True)
async def unban(interaction: discord.Interaction, member: str = None):
    if member is None:
        await interaction.response.send_message("Uso: /unban <ID do usuário ou nome do usuário>")
        return

    try:
        banned_users = await interaction.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await interaction.guild.unban(user)
                await interaction.response.send_message(f"{user.name}#{user.discriminator} foi desbanido do servidor.")
                return

        await interaction.response.send_message(f"{member} não foi encontrado na lista de banidos.")
    except Exception as e:
        await interaction.response.send_message(f"Ocorreu um erro ao tentar desbanir {member}.")

@bot.tree.error
async def unban_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)

@bot.tree.command(guild=guild_object, name="mute", description="Muta o microfone de um membro do servidor.")
@app_commands.describe(member="Membro a ser mutado")
@commands.has_permissions(mute_members=True)
async def mute(interaction: discord.Interaction, member: discord.Member = None):
    if member is None:
        await interaction.response.send_message("Por favor, mencione um membro para mutar.")
        return

    await member.edit(mute=True)
    await interaction.response.send_message(f"{member.display_name} foi mutado.")

@bot.tree.error
async def mute_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)

@bot.tree.command(guild=guild_object, name="unmute", description="Desmuta o microfone de um membro do servidor.")
@app_commands.describe(member="Membro a ser desmutado")
@commands.has_permissions(mute_members=True)
async def unmute(interaction: discord.Interaction, member: discord.Member = None):
    if member is None:
        await interaction.response.send_message("Por favor, mencione um membro para desmutar.")
        return

    await member.edit(mute=False)
    await interaction.response.send_message(f"{member.display_name} foi desmutado.")

@bot.tree.error
async def unmute_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)

@bot.tree.command(guild=guild_object, name="mutefone", description="Muta o fone de um membro do servidor.")
@app_commands.describe(member="Membro a ser mutado")
@commands.has_permissions(deafen_members=True)
async def mutefone(interaction: discord.Interaction, member: discord.Member = None):
    if member is None:
        await interaction.response.send_message("Por favor, mencione um membro para mutar o fone.")
        return

    await member.edit(deafen=True)
    await interaction.response.send_message(f"{member.display_name} teve o fone mutado.")

@bot.tree.error
async def mutefone_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)

@bot.tree.command(guild=guild_object, name="unmutefone", description="Desmuta o fone de um membro do servidor.")
@app_commands.describe(member="Membro a ser desmutado")
@commands.has_permissions(deafen_members=True)
async def unmutefone(interaction: discord.Interaction, member: discord.Member = None):
    if member is None:
        await interaction.response.send_message("Por favor, mencione um membro para desmutar o fone.")
        return

    await member.edit(deafen=False)
    await interaction.response.send_message(f"{member.display_name} teve o fone desmutado.")

@bot.tree.error
async def unmutefone_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)

@bot.tree.command(guild=guild_object, name="voicekick", description="Expulsa um membro do canal de voz.")
@app_commands.describe(member="Membro a ser expulso")
@commands.has_permissions(move_members=True)
async def voicekick(interaction: discord.Interaction, member: discord.Member):
    if member.voice is None:
        await interaction.response.send_message("Esse membro não está em um canal de voz.")
        return

    await member.move_to(None)
    await interaction.response.send_message(f"{member.display_name} foi expulso do canal de voz.")

@bot.tree.error
async def voicekick_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)

@bot.tree.command(guild=guild_object, name="join", description="Entra no canal de voz do autor.")
async def join(interaction: discord.Interaction):
    if interaction.user.voice is None:
        await interaction.response.send_message("Você precisa estar em um canal de voz para usar esse comando.")
        return

    voice_channel = interaction.user.voice.channel
    if interaction.guild.voice_client is None:
        await voice_channel.connect()
        await interaction.response.send_message("Conectado ao canal de voz.")
    else:
        await interaction.guild.voice_client.move_to(voice_channel)
        await interaction.response.send_message("Movido para o canal de voz.")

async def play_next(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    voice_client = interaction.guild.voice_client

    if guild_id in queues and queues[guild_id]:
        audio_url = queues[guild_id].pop(0)
        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        voice_client.play(discord.FFmpegPCMAudio(audio_url, **ffmpeg_options), after=lambda e: bot.loop.create_task(play_next(interaction)))
    else:
        await asyncio.sleep(300)
        if guild_id in queues and not queues[guild_id] and not voice_client.is_playing():
            await voice_client.disconnect()

@bot.tree.command(guild=guild_object, name="play", description="Toca uma música do YouTube.")
@app_commands.describe(query="URL ou título da música")
async def play(interaction: discord.Interaction, query: str):
    print("Iniciando o comando play...")
    await interaction.response.send_message("Processando seu pedido...", ephemeral=True)

    if interaction.user.voice is None:
        await interaction.followup.send("Você precisa estar em um canal de voz para usar esse comando.")
        return

    voice_channel = interaction.user.voice.channel
    if interaction.guild.voice_client is None:
        await voice_channel.connect()
        await interaction.followup.send("Conectado ao canal de voz.")
    else:
        print("Bot já está conectado ao canal de voz.")

    guild_id = interaction.guild.id
    voice_client = interaction.guild.voice_client

    if "youtube.com" in query or "youtu.be" in query:
        url = query
        print(f"URL recebida: {url}")
    else:
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
            search_query = f"ytsearch1:{query}"
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(search_query, download=False)
                url = info['entries'][0]['url']
                print(f"URL extraída da pesquisa: {url}")
        except youtube_dl.utils.DownloadError:
            await interaction.followup.send("Ocorreu um erro ao tentar extrair a URL do vídeo. Certifique-se de que o título está correto.")
            return

    # Baixando e extraindo a URL direta do áudio
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info['url']

    if guild_id not in queues:
        queues[guild_id] = []

    queues[guild_id].append(audio_url)
    print(f"URL adicionada à fila: {audio_url}")

    if not voice_client.is_playing():
        print("Iniciando a reprodução da próxima música.")
        await play_next(interaction)
    else:
        print("Já está tocando uma música, adicionado à fila.")

    await interaction.followup.send("Adicionado à fila.")


async def play_next(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    voice_client = interaction.guild.voice_client

    if guild_id in queues and queues[guild_id]:
        audio_url = queues[guild_id].pop(0)
        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        voice_client.play(discord.FFmpegPCMAudio(audio_url, **ffmpeg_options), after=lambda e: bot.loop.create_task(play_next(interaction)))
    else:
        await asyncio.sleep(300)
        if guild_id in queues and not queues[guild_id] and not voice_client.is_playing():
            await voice_client.disconnect()

@bot.tree.command(guild=guild_object, name="skip", description="Pula para a próxima música na fila.")
async def skip(interaction: discord.Interaction):
    if interaction.guild.voice_client is not None:
        interaction.guild.voice_client.stop()
        await play_next(interaction)
    await interaction.channel.send("Música pulada.")

@bot.tree.command(guild=guild_object, name="pause", description="Pausa a música atual.")
async def pause(interaction: discord.Interaction):
    if interaction.guild.voice_client.is_playing():
        interaction.guild.voice_client.pause()
        await interaction.channel.send("Música pausada.")

@bot.tree.command(guild=guild_object, name="resume", description="Retoma a música pausada.")
async def resume(interaction: discord.Interaction):
    if interaction.guild.voice_client.is_paused():
        interaction.guild.voice_client.resume()
        await interaction.channel.send("Música retomada.")

@bot.tree.command(guild=guild_object, name="stop", description="Para a música atual.")
async def stop(interaction: discord.Interaction):
    if interaction.guild.voice_client.is_playing():
        interaction.guild.voice_client.stop()
        await interaction.channel.send("Música parada.")


@bot.tree.command(guild=guild_object, name="queue", description="Mostra a lista de músicas na fila.")
async def queue(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    if guild_id in queues and queues[guild_id]:
        queue_list = ""
        for index, audio_url in enumerate(queues[guild_id]):
            try:
                # Executar o ffprobe para obter informações do arquivo de áudio
                cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_entries', 'format=tags:title', audio_url]
                result = subprocess.run(cmd, capture_output=True, text=True)
                metadata = result.stdout
                metadata_json = json.loads(metadata)
                
                # Extrair o título da música do metadata
                title = metadata_json['format']['tags']['title'] if 'format' in metadata_json and 'tags' in metadata_json['format'] else 'Desconhecido'
                
                queue_list += f"{index + 1}. {title}\n"
            except Exception as e:
                queue_list += f"{index + 1}. Desconhecido\n"
        
        embed = discord.Embed(title="Lista de músicas na fila", description=queue_list, color=discord.Color.blue())
        await interaction.channel.send(embed=embed)
    else:
        voice_client = interaction.guild.voice_client
        if voice_client and (voice_client.is_playing() or voice_client.is_paused()):
            current_song = voice_client.source.title
            await interaction.channel.send(f"Atualmente está tocando: {current_song}\nNão há mais músicas na fila.")
        else:
            await interaction.channel.send("Não há músicas na fila.")

@bot.tree.command(guild=guild_object, name="leave", description="Desconecta do canal de voz.")
async def leave(interaction: discord.Interaction):
    if interaction.guild.voice_client is not None:
        await interaction.guild.voice_client.disconnect()
        await interaction.channel.send("Desconectado do canal de voz.")
    else:
        await interaction.channel.send("Não estou conectado a nenhum canal de voz.")

bot.run("TOKEN")
