import discord
import os
import asyncio
from discord.ext import commands

# ============ CONFIGURAÇÕES ============
TOKEN = os.getenv("DISCORD_TOKEN")  # Railway vai injetar isso

# IDs dos canais (você pode mudar depois via variáveis de ambiente)
SCRIPT_CHANNELS = os.getenv("SCRIPT_CHANNELS", "<#1489324273787994283>, <#1471600341081653268>")
SCRIPT_FALLBACK = os.getenv("SCRIPT_FALLBACK", "<#1481259934418210930>")

EXECUTOR_ANDROID = os.getenv("EXECUTOR_ANDROID", "<#1471600113112580146>")
EXECUTOR_PC = os.getenv("EXECUTOR_PC", "<#1471600244897874074>")
EXECUTOR_IOS = os.getenv("EXECUTOR_IOS", "<#1471600184197910692>")

DELETE_DELAY = int(os.getenv("DELETE_DELAY", "10"))  # segundos

# ============ BOT ============
intents = discord.Intents.default()
intents.message_content = True  # Necessário para ler conteúdo das mensagens

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot online como {bot.user}")
    print(f"🌐 Conectado em {len(bot.guilds)} servidor(es)")


@bot.event
async def on_message(message):
    # Ignora mensagens do próprio bot
    if message.author == bot.user:
        return

    # Ignora DMs
    if message.guild is None:
        return

    content_lower = message.content.lower()

    # ============ DETECÇÃO DE PALAVRAS-CHAVE ============

    # 1. Palavras "script" ou "Script"
    if "script" in content_lower:
        reply = (
            f"Se está a procura de um script, verifique {SCRIPT_CHANNELS}, "
            f"caso não encontrar, diga o nome do jogo que deseja ter o script em {SCRIPT_FALLBACK}"
        )
        sent = await message.channel.send(reply)
        await asyncio.sleep(DELETE_DELAY)
        await sent.delete()
        return

    # 2. Palavras "executor" ou "Executor"
    if "executor" in content_lower:
        reply = (
            f"Caso está a procura de executores, verifique {EXECUTOR_ANDROID} para android, "
            f"{EXECUTOR_PC} para pc e {EXECUTOR_IOS} para ios"
        )
        sent = await message.channel.send(reply)
        await asyncio.sleep(DELETE_DELAY)
        await sent.delete()
        return

    # Processa comandos normais (se houver)
    await bot.process_commands(message)


# ============ COMANDOS ÚTEIS ============

@bot.command()
async def ping(ctx):
    """Verifica se o bot está online."""
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! Latência: `{latency}ms`")


# ============ INICIALIZAÇÃO ============
if __name__ == "__main__":
    if not TOKEN:
        print("❌ ERRO: Variável DISCORD_TOKEN não encontrada!")
        print("   Defina DISCORD_TOKEN nas variáveis de ambiente do Railway.")
        exit(1)

    bot.run(TOKEN)
