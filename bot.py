import discord
import os
import asyncio
import re
import time
from discord.ext import commands
from discord import app_commands
from datetime import datetime

# ============ CONFIGURAÇÕES ============
TOKEN = os.getenv("DISCORD_TOKEN")

# Canais
SCRIPT_CHANNELS = os.getenv("SCRIPT_CHANNELS", "<#1489324273787994283>, <#1471600341081653268>")
SCRIPT_FALLBACK = os.getenv("SCRIPT_FALLBACK", "<#1481259934418210930>")

EXECUTOR_ANDROID = os.getenv("EXECUTOR_ANDROID", "<#1471600113112580146>")
EXECUTOR_PC = os.getenv("EXECUTOR_PC", "<#1471600244897874074>")
EXECUTOR_IOS = os.getenv("EXECUTOR_IOS", "<#1471600184197910692>")

BUG_CHANNEL = os.getenv("BUG_CHANNEL", "<#1476555789811454077>")
TICKET_CHANNEL = os.getenv("TICKET_CHANNEL", "<#1471604674422509692>")

DELETE_DELAY = int(os.getenv("DELETE_DELAY", "10"))
COOLDOWN_SECONDS = int(os.getenv("COOLDOWN_SECONDS", "20"))

# Cores dos embeds
COLOR_SCRIPT = 0x3498db
COLOR_EXECUTOR = 0x2ecc71
COLOR_BUG = 0xe74c3c
COLOR_KEY = 0x9b59b6
COLOR_HELP = 0xf39c12
COLOR_DEFAULT = 0x95a5a6
COLOR_ANTIGAMBLE = 0xff0000

# ============ SISTEMA ANTI-APOSTA ============
OWNER_ID = 1252758938693144696

# Palavras-chave de apostas
GAMBLING_KEYWORDS = [
    "crypto", "cassino", "casino", "bonus", "bônus", "usdt", "bet",
    "betano", "bank card", "withdrawal", "withdraw", "promo", "promocode",
    "promo code", "promotion", "promoção", "gambling", "gamble",
    "aposta", "apostas", "betting", "wager", "wagering", "stake",
    "stake.com", "1xbet", "pixbet", "blaze", "double", "roleta",
    "roleta online", "crash game", "plinko", "aviator", "mines",
    "slots", "slot", "jackpot", "free spin", "free spins",
    "deposit bonus", "welcome bonus", "sign up bonus", "no deposit",
    "cashback", "rakeback", "vip club", "vip-club", "vip bonus",
    "crypto casino", "bitcoin casino", "btc casino", "eth casino",
    "tether", "binance", "binance pay", "crypto withdrawal",
    "withdraw success", "withdrawal success", "saque", "saque realizado",
    "ganhei", "ganhei na", "ganhei na blaze", "ganhei na bet",
    "luzewin", "luzewin.com", "vyro", "cryptocurrency casino",
    "$5600", "$5000", "$10000", "5600 usdt", "5000 usdt",
    "receive usdt", "usdt received", "+5600", "+5000",
]

# Estado do sistema anti-aposta
gambling_config = {
    "log_channel_id": None,
    "active": True,
}

# ============ SISTEMA DE DETECÇÃO INTELIGENTE ============
KEYWORDS = {
    "script": {
        "words": [
            "script", "scripts", "cheat", "cheats", "hack", "hacks",
            "mod menu", "modmenu", "mod", "mods", "exploit", "exploits",
            "farm", "auto farm", "autofarm", "auto-click", "autoclick",
            "injetor", "injector", "dll", "lua", "roblox script",
            "script de", "script para", "tem script", "algum script",
            "sct", "scrit", "scrpit", "scrip", "scrips",
            "simulador", "simulator", "tycoon", "obby", "obby script",
            "speed run", "speedrun", "auto parry", "autoparry",
            "kill aura", "killaura", "fly", "noclip", "teleport",
            "esp", "wallhack", "aimbot", "triggerbot", "bhop",
            "auto-dodge", "auto collect", "auto click",
            "macro", "macros", "bot", "bots", "automação",
            "scripting", "programa", "programinha", "aplicativo",
            "tem como", "como faço", "como usar", "tutorial script",
            "onde acho", "onde encontro", "onde tá", "onde esta",
            "preciso de", "quero um", "algum", "alguem tem",
            "passa", "manda", "dropa", "drop", "link", "download",
        ],
        "weight": 1,
        "title": "📜 Scripts & Cheats",
        "description": None,
        "color": COLOR_SCRIPT,
        "emoji": "📜",
        "footer": "Dica: Mencione o nome exato do jogo para melhor ajuda!"
    },

    "executor": {
        "words": [
            "executor", "executores", "exploit tool", "exploitation",
            "injetor", "injector", "injetar", "inject",
            "executor android", "executor pc", "executor ios",
            "executor mobile", "executor celular", "executor iphone",
            "roblox executor", "roblox exploit", "level 7",
            "level 8", "unc", "sunc", "api", "wrapper",
            "dll injector", "process hacker", "cheat engine",
            "android executor", "pc executor", "ios executor",
            "mobile executor", "free executor", "paid executor",
            "melhor executor", "qual executor", "qual o melhor",
            "recomenda executor", "indica executor", "sugere executor",
            "preciso de executor", "quero executor", "tem executor",
            "como executar", "como injetar", "como usar executor",
            "instalar executor", "baixar executor", "download executor",
            "executor funciona", "executor atualizado", "executor 2026",
            "bypass", "bypas", "by pass", "anti-cheat", "anticheat",
        ],
        "weight": 1,
        "title": "⚙️ Executores",
        "description": None,
        "color": COLOR_EXECUTOR,
        "emoji": "⚙️",
        "footer": "Escolha o executor compatível com seu dispositivo!"
    },

    "bug": {
        "words": [
            "bug", "bugs", "bugado", "bugada", "bugou", "bugando",
            "crash", "crasha", "crashei", "crasheou", "crashing",
            "erro", "erros", "error", "errors", "falha", "falhou",
            "quebrou", "quebrado", "broken", "not working",
            "não funciona", "nao funciona", "parou", "parou de funcionar",
            "trava", "travando", "travou", "travado", "freeze",
            "congelou", "congelando", "lag", "lagg", "lagando",
            "fps", "fps baixo", "low fps", "performance",
            "desconectou", "disconnect", "kick", "kicked", "ban",
            "tela preta", "black screen", "white screen", "tela branca",
            "não abre", "nao abre", "não inicia", "nao inicia",
            "fechou sozinho", "fecha sozinho", "fecha sozinha",
            "runtime error", "exception", "null pointer", "stack trace",
            "problema", "problemas", "issue", "issues", "glitch",
            "glitchou", "glitchnado", "visual bug", "audio bug",
            "não carrega", "nao carrega", "loading infinito",
            "infinito loading", "stuck", "preso", "presa",
            "não responde", "nao responde", "sem resposta",
            "timeout", "time out", "demora", "demorando",
            "lento", "lenta", "devagar",
            "morri sozinho", "morreu sozinho", "morri do nada",
            "perdi itens", "sumiu", "desapareceu", "não salva",
            "nao salva", "progresso perdido", "resetou",
        ],
        "weight": 1,
        "title": "🐛 Reportar Bug",
        "description": None,
        "color": COLOR_BUG,
        "emoji": "🐛",
        "footer": "Inclua prints e detalhes do erro no ticket para agilizar!"
    },

    "key": {
        "words": [
            "key", "keys", "chave", "chaves", "key system",
            "bypass", "bypas", "by pass", "bypassar", "bypasse",
            "encurtador", "encurtadores", "linkvertise", "lootlabs",
            "work.ink", "paste", "pastecode", "pastebin",
            "key bypass", "bypass key", "pular key", "pular chave",
            "como pular", "como bypassar", "como tirar",
            "tirar key", "remover key", "sem key", "without key",
            "free key", "key grátis", "key gratis", "gerar key",
            "gerador", "generator", "auto key", "key bot",
            "bypass bot", "bot de bypass", "bot de key",
            "resolver", "solucionar", "contornar", "evitar",
            "link encurtado", "short link", "ad link", "adfly",
            "mediafire", "mega", "drive", "download link",
            "preciso de key", "quero key", "tem key", "alguma key",
            "key não funciona", "key invalida", "key expirada",
            "como pegar key", "onde pego key", "onde acho key",
        ],
        "weight": 1,
        "title": "🔑 Key System & Bypass",
        "description": None,
        "color": COLOR_KEY,
        "emoji": "🔑",
        "footer": "Nosso suporte pode ajudar com bypass de encurtadores!"
    },

    "help": {
        "words": [
            "socorro", "ajuda", "help", "suporte", "support",
            "preciso de ajuda", "preciso ajuda", "quero ajuda",
            "me ajuda", "me ajudem", "alguém me ajuda", "alguem me ajuda",
            "não sei", "nao sei", "como faz", "como faço", "como fazer",
            "tutorial", "tutoriais", "guia", "guias", "guide",
            "duvida", "dúvida", "duvidas", "dúvidas", "question",
            "pergunta", "perguntas", "perguntar", "queria saber",
            "gostaria de saber", "como que", "como é que",
            "não entendi", "nao entendi", "confuso", "confusa",
            "perdido", "perdida", "não sei o que fazer", "nao sei o que fazer",
            "onde", "onde fica", "onde está", "onde esta",
            "como chego", "como acesso", "como entro",
            "como uso", "como utilizo", "como funciona",
            "não consigo", "nao consigo", "impossível", "impossivel",
            "difícil", "dificil", "complicado", "complexo",
            "estou com problema", "to com problema", "tô com problema",
            "deu ruim", "deu errado", "algo de errado",
            "mod", "moderador", "admin", "administrador", "staff",
            "atendimento", "atender", "responder", "responde",
            "urgente", "urgência", "emergência", "emergencia",
            "importante", "importantíssimo", "preciso muito",
            "desesperado", "desesperada", "triste", "frustrado",
            "odeio", "não aguento", "nao aguento", "cansei",
        ],
        "weight": 1,
        "title": "🆘 Central de Ajuda",
        "description": None,
        "color": COLOR_HELP,
        "emoji": "🆘",
        "footer": "Nossa equipe responde o mais rápido possível!"
    },
}

# Palavras que anulam a detecção (contexto negativo)
NEGATIVE_CONTEXT = [
    "não quero", "nao quero", "não preciso", "nao preciso",
    "não gosto", "nao gosto", "odeio", "não uso", "nao uso",
    "anti script", "anti-cheat", "reportar script", "denunciar",
]

# ============ COOLDOWN POR USUÁRIO ============
user_cooldowns = {}

# ============ BOT ============
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None,
    case_insensitive=True
)


def is_on_cooldown(user_id: int) -> bool:
    if user_id not in user_cooldowns:
        return False
    elapsed = time.time() - user_cooldowns[user_id]
    return elapsed < COOLDOWN_SECONDS


def set_cooldown(user_id: int):
    user_cooldowns[user_id] = time.time()


def get_description(category: str) -> str:
    if category == "script":
        return "Se está à procura de scripts, verifique:
" + SCRIPT_CHANNELS + "

Caso não encontre, diga o nome do jogo em " + SCRIPT_FALLBACK
    elif category == "executor":
        return "Canais de executores por plataforma:
📱 **Android:** " + EXECUTOR_ANDROID + "
💻 **PC:** " + EXECUTOR_PC + "
🍎 **iOS:** " + EXECUTOR_IOS
    elif category == "bug":
        return "Canais para reportar problemas:
📋 Soluções: " + BUG_CHANNEL + "
🎫 Ticket: " + TICKET_CHANNEL
    elif category == "key":
        return "Para bypass de encurtadores/key system,
abra um ticket em " + TICKET_CHANNEL
    elif category == "help":
        return "Caso esteja precisando de ajuda,
abra um ticket em " + TICKET_CHANNEL
    return ""


def create_embed(category: str, user: discord.Member) -> discord.Embed:
    data = KEYWORDS[category]
    embed = discord.Embed(
        title=data["title"],
        description=get_description(category),
        color=data["color"],
        timestamp=datetime.utcnow()
    )
    embed.set_author(
        name="Suporte Automático — " + user.display_name,
        icon_url=user.display_avatar.url
    )
    embed.set_footer(
        text=data["footer"] + " | Esta mensagem será apagada em " + str(DELETE_DELAY) + "s",
        icon_url=bot.user.display_avatar.url if bot.user else None
    )
    return embed


def analyze_message(content: str) -> tuple | None:
    content_lower = content.lower()
    for neg in NEGATIVE_CONTEXT:
        if neg in content_lower:
            return None
    scores = {}
    for category, data in KEYWORDS.items():
        score = 0
        matched_words = []
        for word in data["words"]:
            pattern = r'\b' + re.escape(word.lower()) + r'\b'
            matches = len(re.findall(pattern, content_lower))
            if matches == 0:
                if word.lower() in content_lower:
                    matches = 1
            if matches > 0:
                score += matches * data["weight"]
                matched_words.append(word)
        if len(matched_words) >= 3:
            score += 2
        if len(matched_words) >= 5:
            score += 3
        if len(matched_words) >= 2:
            score += 1
        if score > 0:
            scores[category] = {"score": score, "words": matched_words}
    if not scores:
        return None
    best_category = max(scores, key=lambda x: scores[x]["score"])
    best_score = scores[best_category]["score"]
    if best_score < 2:
        return None
    return (best_category, best_score)


# ============ FUNÇÕES ANTI-APOSTA ============

def check_gambling_text(text: str) -> list:
    if not text:
        return []
    text_lower = text.lower()
    matches = []
    for keyword in GAMBLING_KEYWORDS:
        if keyword.lower() in text_lower:
            matches.append(keyword)
    return matches


async def send_gambling_log(guild: discord.Guild, message: discord.Message, matched_keywords: list, image_url: str = None):
    log_channel_id = gambling_config.get("log_channel_id")
    if not log_channel_id:
        return
    log_channel = guild.get_channel(log_channel_id)
    if not log_channel:
        return
    embed = discord.Embed(
        title="🚫 Imagem de Aposta Detectada",
        description="Mensagem de " + message.author.mention + " foi apagada automaticamente.",
        color=COLOR_ANTIGAMBLE,
        timestamp=datetime.utcnow()
    )
    embed.set_author(
        name=message.author.display_name,
        icon_url=message.author.display_avatar.url
    )
    embed.add_field(
        name="👤 Usuário",
        value=message.author.mention + " (`" + str(message.author.id) + "`)",
        inline=False
    )
    embed.add_field(
        name="📋 Palavras detectadas",
        value=", ".join("`" + k + "`" for k in matched_keywords[:10]),
        inline=False
    )
    embed.add_field(
        name="💬 Conteúdo original",
        value=message.content[:1000] if message.content else "*(sem texto)*",
        inline=False
    )
    embed.add_field(name="📍 Canal", value=message.channel.mention, inline=True)
    embed.add_field(
        name="🕐 Horário",
        value="<t:" + str(int(message.created_at.timestamp())) + ":F>",
        inline=True
    )
    if image_url:
        embed.set_image(url=image_url)
    embed.set_footer(text="ID da mensagem: " + str(message.id))
    await log_channel.send(embed=embed)


# ============ EVENTOS ============

@bot.event
async def on_ready():
    print("✅ Bot online como " + str(bot.user))
    print("🌐 Conectado em " + str(len(bot.guilds)) + " servidor(es)")
    print("📊 " + str(len(KEYWORDS)) + " categorias de suporte carregadas")
    print("🎰 Anti-aposta: " + ("ATIVO" if gambling_config["active"] else "INATIVO"))
    print("⏱️ Cooldown por usuário: " + str(COOLDOWN_SECONDS) + "s")
    try:
        synced = await bot.tree.sync()
        print("🔄 " + str(len(synced)) + " slash commands sincronizados")
    except Exception as e:
        print("⚠️ Erro ao sincronizar slash commands: " + str(e))
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name="por mensagens | /ajuda"
    )
    await bot.change_presence(activity=activity)


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    if message.guild is None:
        return
    if message.author.bot:
        return

    # === ANTI-APOSTA ===
    if gambling_config.get("active", True):
        for attachment in message.attachments:
            if attachment.content_type and attachment.content_type.startswith("image/"):
                filename_matches = check_gambling_text(attachment.filename)
                text_matches = check_gambling_text(message.content)
                all_matches = list(set(filename_matches + text_matches))
                if all_matches:
                    try:
                        await message.delete()
                    except (discord.Forbidden, discord.NotFound):
                        pass
                    await send_gambling_log(
                        message.guild, message, all_matches, attachment.url
                    )
                    return

        for embed in message.embeds:
            if embed.image and embed.image.url:
                text_matches = check_gambling_text(message.content)
                url_matches = check_gambling_text(embed.image.url)
                title_matches = check_gambling_text(embed.title or "")
                desc_matches = check_gambling_text(embed.description or "")
                all_matches = list(set(text_matches + url_matches + title_matches + desc_matches))
                if all_matches:
                    try:
                        await message.delete()
                    except (discord.Forbidden, discord.NotFound):
                        pass
                    await send_gambling_log(
                        message.guild, message, all_matches, embed.image.url
                    )
                    return

    # === COOLDOWN ===
    if is_on_cooldown(message.author.id):
        return
    result = analyze_message(message.content)
    if result:
        category, score = result
        set_cooldown(message.author.id)
        embed = create_embed(category, message.author)
        sent = await message.channel.send(embed=embed)
        await asyncio.sleep(DELETE_DELAY)
        try:
            await sent.delete()
        except discord.NotFound:
            pass
    await bot.process_commands(message)


# ============ SLASH COMMANDS ============

@bot.tree.command(name="ajuda", description="Mostra a central de suporte automático")
async def slash_ajuda(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🤖 Central de Suporte Automático",
        description="Eu detecto automaticamente o que você precisa! Aqui estão as categorias:",
        color=COLOR_DEFAULT,
        timestamp=datetime.utcnow()
    )
    categories_info = [
        ("📜 Scripts", "script", "Palavras como: script, cheat, hack, mod menu, auto farm..."),
        ("⚙️ Executores", "executor", "Palavras como: executor, inject, exploit, level 7, bypass..."),
        ("🐛 Bugs & Erros", "bug", "Palavras como: bug, crash, erro, não funciona, travou..."),
        ("🔑 Key & Bypass", "key", "Palavras como: key, bypass, encurtador, linkvertise..."),
        ("🆘 Ajuda Geral", "help", "Palavras como: ajuda, socorro, help, não sei, tutorial..."),
    ]
    for emoji_title, key, desc in categories_info:
        embed.add_field(name=emoji_title, value=desc, inline=False)
    embed.set_footer(
        text="Basta enviar sua mensagem no chat que eu identifico automaticamente! | Cooldown: " + str(COOLDOWN_SECONDS) + "s",
        icon_url=bot.user.display_avatar.url
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="ping", description="Mostra a latência do bot")
async def slash_ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description="Latência: `" + str(latency) + "ms`",
        color=COLOR_DEFAULT
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="testar", description="Testa a detecção de uma mensagem")
@app_commands.describe(texto="Texto para analisar")
@app_commands.checks.has_permissions(manage_messages=True)
async def slash_testar(interaction: discord.Interaction, texto: str):
    result = analyze_message(texto)
    if result:
        category, score = result
        embed = create_embed(category, interaction.user)
        embed.add_field(
            name="🧪 Modo Teste",
            value="Texto analisado: `" + texto[:100] + "`...",
            inline=False
        )
        embed.add_field(name="🎯 Pontuação", value=str(score) + " pontos", inline=True)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("🤷 Nenhuma categoria detectada para esse texto.")


@bot.tree.command(name="stats", description="Mostra estatísticas do bot")
async def slash_stats(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📊 Estatísticas do Bot",
        color=COLOR_DEFAULT,
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="Servidores", value=str(len(bot.guilds)), inline=True)
    embed.add_field(name="Categorias", value=str(len(KEYWORDS)), inline=True)
    embed.add_field(name="Latência", value=str(round(bot.latency * 1000)) + "ms", inline=True)
    total_keywords = sum(len(v["words"]) for v in KEYWORDS.values())
    embed.add_field(name="Palavras-chave", value=str(total_keywords), inline=True)
    embed.add_field(name="Cooldown", value=str(COOLDOWN_SECONDS) + "s", inline=True)
    embed.set_footer(text="Bot: " + str(bot.user))
    await interaction.response.send_message(embed=embed)


# ============ SLASH COMMANDS ANTI-APOSTA ============

@bot.tree.command(name="channel", description="Define o canal de log para detecção de apostas")
@app_commands.describe(canal="Canal onde os logs serão enviados")
async def slash_channel(interaction: discord.Interaction, canal: discord.TextChannel):
    if interaction.user.id != OWNER_ID:
        return await interaction.response.send_message("❌ Apenas o dono pode usar este comando.", ephemeral=True)
    gambling_config["log_channel_id"] = canal.id
    embed = discord.Embed(
        title="✅ Canal de Log Configurado",
        description="Logs de detecção de apostas serão enviados em " + canal.mention,
        color=COLOR_EXECUTOR
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="active", description="Ativa ou desativa o sistema anti-aposta")
@app_commands.describe(estado="true para ativar, false para desativar")
@app_commands.choices(estado=[
    app_commands.Choice(name="Ativar", value="true"),
    app_commands.Choice(name="Desativar", value="false"),
])
async def slash_active(interaction: discord.Interaction, estado: app_commands.Choice[str]):
    if interaction.user.id != OWNER_ID:
        return await interaction.response.send_message("❌ Apenas o dono pode usar este comando.", ephemeral=True)
    if estado.value == "true":
        gambling_config["active"] = True
        status = "ATIVADO"
        color = COLOR_EXECUTOR
    else:
        gambling_config["active"] = False
        status = "DESATIVADO"
        color = COLOR_BUG
    embed = discord.Embed(
        title="🎰 Sistema Anti-Aposta " + status,
        description="O sistema de detecção de imagens de apostas está agora **" + status + "**.",
        color=color
    )
    await interaction.response.send_message(embed=embed)


# ============ INICIALIZAÇÃO ============
if __name__ == "__main__":
    if not TOKEN:
        print("❌ ERRO: Variável DISCORD_TOKEN não definida!")
        print("   Configure em: Railway → Variables → DISCORD_TOKEN")
        exit(1)
    bot.run(TOKEN)
