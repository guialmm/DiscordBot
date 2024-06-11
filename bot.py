import discord  
import random
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = "!", intents=intents)

pessoa = 383979046507249675
emoji_macaco = "🐵"

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

bot.remove_command('help')

@bot.command(aliases=['ajuda'])
async def help(ctx):
    MyEmbed = discord.Embed(title="Comandos do Bot", description="Lista de comandos disponíveis", color = discord.Color.dark_purple())
    MyEmbed.add_field(name="!ping", value="Retorna Pong!", inline=False)
    MyEmbed.add_field(name="!dado <maximo>", value="Rola um dado do número máximo que você escolhe", inline=False)
    MyEmbed.add_field(name="!coinflip", value="Joga uma moeda", inline=False)
    clear_aliases = ', '.join(['!'+alias for alias in bot.get_command('clear').aliases])
    MyEmbed.add_field(name=f"!clear <quantidade> (Outros comandos: {clear_aliases})", value="Apaga a quantidade de mensagens que você escolher", inline=False)
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
        await ctx.send("O limite de mensagens foi atingido, só consigo apagar entre 1 e 500 mensagens por vez.")
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
        banned_users = [entry async for entry in ctx.guild.bans()]  # Convert async generator to list
        
        if not banned_users:
            await ctx.send("Não há usuários banidos.")
            return

        member = member.lower().strip()
        
        # Check if member is a mention
        if member.startswith("<@") and member.endswith(">"):
            member = member[2:-1]
            if member.startswith("!"):
                member = member[1:]

        for ban_entry in banned_users:
            user = ban_entry.user

            if str(user.id) == member or user.name.lower() == member:
                await ctx.guild.unban(user)
                await ctx.send(f"{user.name} (ID: {user.id}) foi desbanido do servidor.")
                return

        await ctx.send(f"Não foi possível desbanir {member}. Usuário não encontrado na lista de banidos.")
    except Exception as e:
        await ctx.send(f"Ocorreu um erro ao tentar desbanir {member}. Tente utilizar o comando neste formato: '!unban <ID do usuário ou nome do usuário>'. Se o problema persistir, verifique se o ID ou o nome de usuário estão corretos e tente novamente.")

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Você não tem permissão para executar esse comando.")
    else:
        await ctx.send("Ocorreu um erro ao tentar desbanir. Tente utilizar o comando neste formato: '!unban <ID do usuário ou nome do usuário>'. Se o problema persistir, verifique se o ID ou o nome de usuário estão corretos e tente novamente.")


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
        await ctx.send("Por favor, mencione um membro para mutar seu fone.")
        return

    await member.edit(deafen=True)
    await ctx.send(f"{member.display_name} seu fone foi mutado.")

@mutefone.error
async def mutefone_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Você não tem permissão para executar esse comando.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def unmutefone(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send("Por favor, mencione um membro para desmutar seu fone.")
        return

    await member.edit(deafen=False)
    await ctx.send(f"{member.display_name} seu fone foi desmutado.")

@unmutefone.error
async def unmutefone_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Você não tem permissão para executar esse comando.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def voicekick(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send("Por favor, mencione um membro para expulsar do canal de voz.")
        return

    await member.edit(voice_channel=None)
    await ctx.send(f"{member.display_name} foi expulso do canal de voz.")

@voicekick.error
async def voicekick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Você não tem permissão para executar esse comando.")


bot.run("MTI0ODM2NTUyNzI2MTI1MzcyMw.G-ga0y.lbzit-u297Qs7FWxUVfyyigCvOy8pA19c_lnfs")