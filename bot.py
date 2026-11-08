import discord
from discord.ext import commands
import asyncio

# Configuración del bot
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Diccionario para controlar qué canales tienen una alerta activa
alertas_activas = {}

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Si alguien escribe #RAID
    if message.content.strip() == "#RAID":
        channel_id = message.channel.id
        
        # Evita que se dupliquen alertas en el mismo canal si ya hay una activa
        if channel_id in alertas_activas and alertas_activas[channel_id]:
            return

        alertas_activas[channel_id] = True
        await message.channel.send("🚨 **¡ALERTA DE RAID INICIADA!** 🚨 ¡Defiendan la base en Misión Evo!")

        # Bucle de spam cada 5 segundos hasta que reaccionen con ✅
        while alertas_activas.get(channel_id, False):
            # Enviar mensaje de aviso
            alerta_msg = await message.channel.send("@everyone ⚠️ **¡NOS SIGUEN RAIDENANDO! ¡NECESITAMOS APOYO URGENTE!** ⚠️")
            
            # Esperar 5 segundos comprobando si alguien reaccionó
            for _ in range(5):
                await asyncio.sleep(1)
                # Volver a buscar el mensaje actualizado para ver las reacciones
                try:
                    msg_actualizado = await message.channel.fetch_message(alerta_msg.id)
                    for reaction in msg_actualizado.reactions:
                        if str(reaction.emoji) == "✅":
                            # Si alguien reaccionó con ✅, detenemos la alarma
                            alertas_activas[channel_id] = False
                            await message.channel.send("✅ **¡Alerta desactivada! Base asegurada.** Buen trabajo.")
                            return
                except Exception:
                    pass
            
            # Si pasaron los 5 segundos y nadie reaccionó, el bucle continúa y envía otro mensaje

    await bot.process_commands(message)

# PEGA TU TOKEN DE BOT AQUÍ (mantenlo entre las comillas)
bot.run("MTU2ODc4MDEwMTE3MTAyMzg5Mw.G9ZTq1._s-05529OQbDO0Rdi_onShhncgxuX-LiFxbj7I")