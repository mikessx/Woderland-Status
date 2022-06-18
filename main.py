import datetime
import psutil
from psutil._common import bytes2human
import discord
from discord.ext import commands
import json

#cpu_percent = psutil.cpu_percent(interval=1)
#mem_percent = psutil.virtual_memory().percent
#disck_percent = psutil.disk_usage('/').percent
#total_mem = psutil.virtual_memory().total
#free_mem = psutil.virtual_memory().available
#total_disk = psutil.disk_usage('/').total
#
#print("----------------- <In Utilizzo> -----------------")
#
#print('CPU:', cpu_percent, '%')
#print('Memoria:', mem_percent, '%')
#print('Disco:', disck_percent, '%')
#print('Memoria totale:', bytes2human(total_mem))
#print('Memoria libera:', bytes2human(free_mem))
#print('Disco totale:', bytes2human(total_disk))

print("----------------- <Logger> -----------------")

config = json.load(open('config.json'))
token = config['token']
prefix = config['prefix']
emb_color = int(config['color'], 0)

activity = discord.Game(name=f"{prefix}help")
client = commands.Bot(command_prefix=prefix, activity=activity)

client.remove_command('help')


@client.event
async def on_ready():
  print("Il Bot è pronto per l'utilizzo!")
  print("Attualmente sono connesso come: {}".format(client.user.name))
  try:
    with open('logchannel.json', 'r') as f:
        cfg = json.load(f)
        for guild in cfg:
         logch = cfg[guild]
         onlnch = client.get_channel(int(logch))
         today = datetime.datetime.now()
         date_time = today.strftime("%m/%d/%Y, %H:%M:%S")
         #await onlnch.send(f"Back online, {date_time}")
         embed = discord.Embed(title="Tornato Online!", description=date_time, color=emb_color)
         embed.set_thumbnail(url="https://c.tenor.com/0AVbKGY_MxMAAAAC/check-mark-verified.gif")
         await onlnch.send(embed=embed)
  except:
      print("Nessun canale di log configurato!")


@client.command()
async def dedicato(ctx):
    await ctx.channel.trigger_typing()
    cpu_percent = psutil.cpu_percent(interval=1)
    mem_percent = psutil.virtual_memory().percent
    disck_percent = psutil.disk_usage('/').percent
    total_mem = psutil.virtual_memory().total
    free_mem = psutil.virtual_memory().available
    total_disk = psutil.disk_usage('/').total
    embed = discord.Embed(title="Stato Attuale del **Dedicato**", description="", color=emb_color)
    embed.add_field(name="CPU In Uso:", value=f"{cpu_percent}%", inline=False)
    embed.add_field(name="Memoria In Uso:", value=f"{mem_percent}%", inline=False)
    embed.add_field(name="Disco In Uso:", value=f"{disck_percent}%", inline=False)
    embed.add_field(name="Memoria Totale:", value=bytes2human(total_mem), inline=False)
    embed.add_field(name="Memoria Libera:", value=bytes2human(free_mem), inline=False)
    embed.add_field(name="Disco Totale:", value=bytes2human(total_disk), inline=False)
    await ctx.send(embed=embed)

@client.command()
async def help(ctx):
    embed = discord.Embed(title="Comandi disponibili", description="Il Prefix impostato è {}, passa nel config per cambiarlo!".format(prefix), color=emb_color)
    embed.add_field(name="`dedicato`", value="Mostra lo stato attuale del **Dedicato**", inline=False)
    embed.add_field(name="`help`", value="Mostra la lista dei comandi disponibili", inline=False)
    embed.add_field(name="`setlogch`", value="Imposta il canale di log", inline=False)
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(administrator=True)
async def setlogch(ctx, channel: discord.TextChannel = None):
    if channel == None:
        try:
            with open("logchannel.json", 'r') as f:
                cfg = json.loads(f.read())
                cfg.pop(str(ctx.guild.id))
                json.dump(cfg, open("logchannel.json", 'w'))
                await ctx.message.reply(f"Il Canale di log è stato rsettato da {ctx.author}")
        except:
            await ctx.message.reply("Non c'è un canale di log configurato!")

    else:

     with open("logchannel.json", "r") as f:
        cfg = json.load(f)

     cfg[str(ctx.guild.id)] = channel.id
     with open("logchannel.json", "w") as f:
        json.dump(cfg, f, indent=4)
        embed = discord.Embed(title="Success",
                              description=f"Ho impostato il canale dei log a {channel.mention}!",
                              colour=emb_color)
        await ctx.message.reply(embed=embed)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Comando non trovato!')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Manca un parametro!')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('Non hai i permessi necessari per eseguire il comando!')
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send('Non ho i permessi necessari per eseguire il comando!')
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send('Questo comando è in cooldown! Riprova in %.2fs' % error.retry_after)


try:
    client.run(token)
except:
    print("Errore di connessione! Hai problemi con il token?")
