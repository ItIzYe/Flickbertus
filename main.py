import discord
from discord.ext import commands, tasks
from itertools import cycle
import os
import youtube_dl
intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True, bans =True, voice_states= True)
client = commands.Bot(command_prefix = '+', intents = intents)


status = cycle(['God', 'Life', 'Humans'])

@client.event
async def on_ready():
	await client.change_presence(status=discord.Status.idle)
	change_status.start()
	print('You are logged in as {0.user}'.format(client))

@tasks.loop(seconds=30)
async def change_status():
	await client.change_presence(activity=discord.Game(next(status)))

@client.event
async def on_member_join(member):
	guild = client.get_guild(814121011326222418)
	channel = guild.get_channel(814121011397918726)
	await channel.send(f' :rocket: Willkommen auf {guild.name} {member.mention} :rocket:')
	await member.send(f'Hi {member.mention}! Wir freuen uns das du auf unseren Server ```{guild.name}``` gekommen bist. bitte lese dir die Regeln durch undakzeptiere sie :white_check_mark: um Zugriff auf die restlichen Kanäle zu erhalten. Solltest du noch fragen haben melde dich einfach beim Support oder öffne ein Ticket :thumbsup:. Wir wünschen dir viel Spaß! :rocket::rocket: ')

@client.command(aliases= ['INFO', 'info'])
async def Info(ctx):
  await ctx.send('Name: Flickbertus#8879, Version: 1.0.0, Author: ItIzYe') #zeigt ein paar Infos zu dem Bot

@client.command(aliases= ['bot', 'BOT'])
async def Bot(ctx):
  await ctx.send('Dieser Bot wurde von ItIzYe mithilfe von Python programmiert') #zeigt ein paar Infos zu dem Bot

@client.command(aliases= ['willkommen', 'WILLKOMMEN'])
async def Willkommen(ctx):
  await ctx.send('Willkommen auf dem Server. Wir hoffen, dass du hier Spaß hast!') #sendet eine Willkommensnachricht, falls nicht automatisch geschehen

@client.command(aliases = ['Ping', 'PING'])
async def ping(ctx):
	await ctx.send(f'Pong! {round(client.latency * 1000)}ms') #zeigt dir deinen Ping

@client.command(aliases= ['Clear', 'CLEAR']) #Lösche eine bestimmte Anzahl an Nachrichten
@commands.has_permissions(manage_messages= True)
async def clear(ctx, amount : int):
	await ctx.channel.purge(limit=amount)
	await ctx.send('Die Nachrichten wurden erfolgreich gelöscht :white_check_mark:')

@client.command(aliases= ['Kick', 'KICK']) #Kicke eine Person vom Server
@commands.has_permissions(kick_members= True)
async def kick(ctx, member : discord.Member, *, reason =None):
	await member.kick(reason = reason)
	await ctx.send(f' {member.mention} wurde erfolgreich gekickt')

@client.command(aliases= ['Ban', 'BAN']) #Banne eine Person vom Server
@commands.has_permissions(ban_members= True)
async def ban(ctx, member : discord.Member, *, reason =None):
	await member.ban(reason = reason)
	await ctx.send(f' {member.mention} wurde rfolgreich gebannt')

@client.command()
@commands.has_permissions(ban_members= True) #Entbanne eine Person
async def unban(ctx, *, member ):
	banned_users = await ctx.guild.bans()
	member_name, member_discriminator = member.split('#')

	for ban_entry in banned_users:
		user = ban_entry.user

		if (user.name, user.discriminator) == (member_name, member_discriminator):
			await ctx.guild.unban(user)
			await ctx.send(f'{user.mention} wurde entbannt! :white_check_mark: ')
			return

@clear.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(' :x: Bitte gebe an, wieviele Nachrichten gelöscht werden sollen :x: ')

@client.command(aliases= ['Invite', 'INVITE']) #sendet einen Invitelink für den Bot
async def invite(ctx):
	await ctx.send(' https://discord.com/api/oauth2/authorize?client_id=828717079951573042&permissions=8&scope=bot ')

@ban.error
async def ban_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(' :x: Bitte gebe an, wer gebannt werden soll :x: ')

@kick.error
async def kick_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(' :x: Bitte gebe an, wer gekickt werden soll :x: ')

@client.command(pass_context = True) #Lässt den Bot einem Voice Channel joinen
async def join(ctx):
	if (ctx.author.voice):
		channel = ctx.message.author.voice.channel
		await channel.connect()
	else:
		await ctx.send('Bitte begebe dich zuerst in einen Voice Channel')

@client.command(pass_context=True) #Lässt den Bot den Voice Channel verlassen
async def leave(ctx):
	if (ctx.voice_client):
		await ctx.guild.voice_client.disconnect()
		await ctx.send('Ich habe den Voice Channel verlassen')
	else:
	  await ctx.send('Ich bin in keinem Voice Channel')

@client.command(aliases = ['Report', 'REPORT']) #Reporte einen Member
async def report(ctx, member : discord.Member, *, reason):
	guild = client.get_guild(814121011326222418)
	channel_report= guild.get_channel(814121012303233043)
	await channel_report.send (f' {member.mention} wurde von {ctx.message.author.mention} reportet.Grund: -' + (reason))

@report.error
async def report_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(' :x: Bitte gebe an, wer reportet werden soll, und warum er/sie reportet wird :x: ')



client.run(os.getenv('TOKEN'))
