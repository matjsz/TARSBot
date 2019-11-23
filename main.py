import discord
import messages
import os
import youtube_dl
from discord.ext import commands
import time
from discord import Webhook, AsyncWebhookAdapter
from discord import FFmpegPCMAudio
from discord.utils import get
from discord import *
import youtube_dl

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('[ OK ] Logado como {0.user}!'.format(bot))
    status = "[ OK ]"

@bot.command(pass_content=True)
async def playms(ctx, url):
	autor = ctx.message.author
	mschannel = ctx.message.author.voice.channel
	if not channel:
		await ctx.send("@{} Você não está conectado á um canal de voz!".format(autor))
		return
	voice = get(bot.voice_clients, guild=ctx.guild)
	if voice and voice.is_connected():
		await voice.move_to(channel)
	else:
		voice = await mschannel.connect()

	song_there = os.path.isfile("song.mp3")
	try:
		if song_there:
			os.remove("song.mp3")
			print("Old-song removida")
	except PermissionError:
		print("Tentando deletar o arquivo de som, mas está tocando...")
		await ctx.send("**ERRO** ```Música tocando```")
		return

	await ctx.send(":white_check_mark: Conectado em {}".format(mschannel))
	await ctx.send(":arrow_forward: Preparando para tocar...")

	ydl_opts = {
		'format': 'bestaudio/best',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
	}

	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([url])

	for file in os.listdir("./"):
		if file.endswith(".mp3"):
			name = file
			print("Arquivo renomeado: {}\n".format(file))
			os.rename(file, "song.mp3")

	voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Sucesso!"))
	voice.source = discord.PCMVolumeTransformer(voice.source)
	voice.source.volume = 0.07

	nname = name.rsplit("-", 2)
	await ctx.send(":arrow_forward: Tocando: {}".format(nname))
	print("Tocando!\n")

@bot.command(pass_content=True)
async def stopms(ctx):
	mschannel = ctx.message.author.voice.channel
	server = ctx.message.guild
	voice_client = server.voice_client
	await ctx.send(":octagonal_sign: Saindo de {}".format(mschannel))
	await voice_client.disconnect()

@bot.command()
async def ver(ctx):
	await ctx.send(messages.vermsg)

@bot.command(pass_content=True)
async def clearchat(ctx, amount=50):
	msgchannel = ctx.message.channel
	await ctx.send(":wrench: **Limpando**...")
	time.sleep(1)
	await msgchannel.purge(limit = amount)
	time.sleep(1)
	await ctx.send("**Pronto!** :)")

@bot.command()
async def kick(ctx, member : discord.Member, *, reason=None, time='1 dia'):
	autor = ctx.message.author
	embed = discord.Embed(
		title = ':no_entry_sign: **Kick**',
		description = '@{} Foi kickado do servidor!'.format(member),
		colour = discord.Colour.blue()
		)

	embed.set_footer(text='O TARS é mal...')
	embed.set_author(name='@{}'.format(autor))
	embed.add_field(name='Razão', value='{}'.format(reason), inline=True)
	embed.add_field(name='Tempo', value='{}'.format(time))

	server = ctx.message.guild

	embeddm = discord.Embed(
		title=':no_entry_sign: **Kick**',
		description = 'Você foi kickado do servidor **{}**'.format(server),
		colour = discord.Colour.blue()
		)

	embeddm.set_footer(text='Iiih... deu ruim...')
	embeddm.set_author(name='Kickado por @{}'.format(autor))
	embeddm.add_field(name='Razão', value='{}'.format(reason), inline=True)
	embeddm.add_field(name='Tempo', value='{}'.format(time))

	await ctx.send(embed=embed)
	await member.send(embed=embeddm)
	await member.kick(reason=reason)

@bot.command()
async def ban(ctx, member : discord.Member, *, reason=None, time='**Permanente**'):
	autor = ctx.message.author
	embed = discord.Embed(
		title = ':no_entry_sign: **BAN**',
		description = '@{} Foi **banido** do servidor!'.format(member),
		colour = discord.Colour.red()
		)

	embed.set_footer(text='O TARS é MUITO mal...')
	embed.set_author(name='@{}'.format(autor))
	embed.add_field(name='Razão', value='{}'.format(reason), inline=True)
	embed.add_field(name='Tempo', value='{}'.format(time))

	server = ctx.message.guild

	embeddmban = discord.Embed(
		title=':no_entry_sign: **BAN**',
		description = 'Você foi **banido** do servidor **{}**'.format(server),
		colour = discord.Colour.red()
		)

	embeddmban.set_footer(text='Iiih... deu MUITO ruim...')
	embeddmban.set_author(name='banido por @{}'.format(autor))
	embeddmban.add_field(name='Razão', value='{}'.format(reason), inline=True)
	embeddmban.add_field(name='Tempo', value='{}'.format(time))

	await ctx.send(embed=embed)
	await member.send(embed=embeddmban)
	await member.kick(reason=reason)

@bot.command()
async def helpcmds(ctx, where=None):
	autor = ctx.message.author

	embed = discord.Embed(
		colour = discord.Colour.blue()
		)

	embed.set_author(name='Comandos do Tars')
	embed.add_field(name='!ver', value='Checa a versão do Tars', inline=False)
	embed.add_field(name='!clearchat (ADMIN)', value='Limpa o chat', inline=False)
	embed.add_field(name='!kick (ADMIN)', value='Kicka um usuário - uso: !kick [@usuário] [motivo]', inline=False)
	embed.add_field(name='!ban (ADMIN)', value='Bane um usuário - uso: !ban [@usuário] [motivo]', inline=False)
	embed.add_field(name='!playms', value='Toca uma música de uma URL - uso !playms [url]', inline=False)
	embed.add_field(name='!stopms', value='Para de reproduzir uma música', inline=False)

	embedhere = discord.Embed(
		title='Comandos do Tars',
		colour = discord.Colour.blue()
		)

	embedhere.set_author(name='help - Solicitado por {}'.format(autor))
	embedhere.add_field(name='!ver', value='Checa a versão do Tars', inline=False)
	embedhere.add_field(name='!clearchat (ADMIN)', value='Limpa o chat', inline=False)
	embedhere.add_field(name='!kick (ADMIN)', value='Kicka um usuário - uso: !kick [@usuário] [motivo]', inline=False)
	embedhere.add_field(name='!ban (ADMIN)', value='Bane um usuário - uso: !ban [@usuário] [motivo]', inline=False)
	embedhere.add_field(name='!playms', value='Toca uma música de uma URL - uso !playms [url]', inline=False)
	embedhere.add_field(name='!stopms', value='Para de reproduzir uma música', inline=False)

	if where == None:
		await ctx.send(embed=embedhere)
	elif where == "me":
		await autor.send('Olá {}! Aqui estão alguns comandos! :)'.format(autor))
		await autor.send(embed=embed)
	else:
		await ctx.send(embed=embedhere)


bot.run('NjA1MDg5NjExODc3ODQyOTU0.XdWEhQ.6RKMh9A6r2HM6eGNJO6gq7yo-Dw')