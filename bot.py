import discord
import os
import asyncio
import re
import time
from discord.ext import commands
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
        "description": (
            f"Se está à procura de scripts, verifique:\n"
            f"{SCRIPT_CHANNELS}\n\n"
            f"Caso não encontre, diga o nome do jogo em {SCRIPT_FALLBACK}"
        ),
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
        "description": (
            f"Canais de executores por plataforma:\n"
            f"📱 **Android:** {EXECUTOR_ANDROID}\n"
            f"💻 **PC:** {EXECUTOR_PC}\n"
            f"🍎 **iOS:** {EXECUTOR_IOS}"
        ),
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
        "description": (
            f"Canais para reportar problemas:\n"
            f"📋 Soluções: {BUG_CHANNEL}\n"
            f"🎫 Ticket: {TICKET_CHANNEL}"
        ),
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
        "description": (
            f"Para bypass de encurtadores/key system,\n"
            f"abra um ticket em {TICKET_CHANNEL}"
        ),
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
        "description": (
            f"Caso esteja precisando de ajuda,\n"
            f"abra um ticket em {TICKET_CHANNEL}"
        ),
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
    """Verifica se o usuário está em cooldown."""
    if user_id not in user_cooldowns:
        return False
    elapsed = time.time() - user_cooldowns[user_id]
    return elapsed < COOLDOWN_SECONDS


def set_cooldown(user_id: int):
    """Define o timestamp do último acionamento do usuário."""
    user_cooldowns[user_id] = time.time()


def create_embed(category: str, user: discord.Member) -> discord.Embed:
    data = KEYWORDS[category]

    embed = discord.Embed(
        title=data["title"],
        description=data["description"],
        color=data["color"],
        timestamp=datetime.utcnow()
    )

    embed.set_author(
        name=f"Suporte Automático — {user.display_name}",
        icon_url=user.display_avatar.url
    )

    embed.set_footer(
        text=f"{data['footer']} | Esta mensagem será apagada em {DELETE_DELAY}s",
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
            scores[category] = {
                "score": score,
                "words": matched_words
            }

    if not scores:
        return None

    best_category = max(scores, key=lambda x: scores[x]["score"])
    best_score = scores[best_category]["score"]

    if best_score < 2:
        return None

    return (best_category, best_score)


@bot.event
async def on_ready():
    print(f"✅ Bot online como {bot.user}")
    print(f"🌐 Conectado em {len(bot.guilds)} servidor(es)")
    print(f"📊 {len(KEYWORDS)} categorias de suporte carregadas")
    print(f"⏱️ Cooldown por usuário: {COOLDOWN_SECONDS}s")

    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name="por mensagens | !ajuda"
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

    # === COOLDOWN POR USUÁRIO ===
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


# ============ COMANDOS ============

@bot.command(name="ajuda", aliases=["help", "comandos", "cmds"])
async def cmd_ajuda(ctx: commands.Context):
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
        embed.add_field(
            name=emoji_title,
            value=desc,
            inline=False
        )

    embed.set_footer(
        text=f"Basta enviar sua mensagem no chat que eu identifico automaticamente! | Cooldown: {COOLDOWN_SECONDS}s",
        icon_url=bot.user.display_avatar.url
    )

    await ctx.send(embed=embed)


@bot.command(name="ping")
async def cmd_ping(ctx: commands.Context):
    latency = round(bot.latency * 1000)

    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Latência: `{latency}ms`",
        color=COLOR_DEFAULT
    )

    await ctx.send(embed=embed)


@bot.command(name="testar", aliases=["test", "detectar"])
async def cmd_testar(ctx: commands.Context, *, texto: str):
    if not ctx.author.guild_permissions.manage_messages:
        return await ctx.send("❌ Você não tem permissão para usar este comando.")

    result = analyze_message(texto)

    if result:
        category, score = result
        embed = create_embed(category, ctx.author)
        embed.add_field(
            name="🧪 Modo Teste",
            value=f"Texto analisado: `{texto[:100]}`...",
            inline=False
        )
        embed.add_field(
            name="🎯 Pontuação",
            value=f"{score} pontos",
            inline=True
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send("🤷 Nenhuma categoria detectada para esse texto.")


@bot.command(name="stats")
async def cmd_stats(ctx: commands.Context):
    embed = discord.Embed(
        title="📊 Estatísticas do Bot",
        color=COLOR_DEFAULT,
        timestamp=datetime.utcnow()
    )

    embed.add_field(name="Servidores", value=str(len(bot.guilds)), inline=True)
    embed.add_field(name="Categorias", value=str(len(KEYWORDS)), inline=True)
    embed.add_field(name="Latência", value=f"{round(bot.latency * 1000)}ms", inline=True)

    total_keywords = sum(len(v["words"]) for v in KEYWORDS.values())
    embed.add_field(name="Palavras-chave", value=str(total_keywords), inline=True)
    embed.add_field(name="Cooldown", value=f"{COOLDOWN_SECONDS}s", inline=True)

    embed.set_footer(text=f"Bot: {bot.user}")

    await ctx.send(embed=embed)


# ============ INICIALIZAÇÃO ============
if __name__ == "__main__":
    if not TOKEN:
        print("❌ ERRO: Variável DISCORD_TOKEN não definida!")
        print("   Configure em: Railway → Variables → DISCORD_TOKEN")
        exit(1)

    bot.run(TOKEN)
