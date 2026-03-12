import discord
import aiohttp
import os

# ============================================================
# CONFIGURAÇÕES — preencha os valores abaixo
# ============================================================
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "COLE_SEU_TOKEN_AQUI")
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "https://vitorpomodoro.app.n8n.cloud/webhook/auvo-bot")
CANAL_ID = int(os.getenv("CANAL_ID", "0"))  # ID do canal onde o bot vai responder
PREFIXO = "!"  # O bot só responde mensagens que começam com ! (ex: !pergunta O que é a Auvo?)
# ============================================================

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Bot conectado como {client.user}")

@client.event
async def on_message(message):
    # Ignora mensagens do próprio bot
    if message.author == client.user:
        return

    # Só responde no canal configurado
    if CANAL_ID and message.channel.id != CANAL_ID:
        return

    # Só responde se começar com o prefixo !
    if not message.content.startswith(PREFIXO):
        return

    # Remove o prefixo e pega a pergunta
    pergunta = message.content[len(PREFIXO):].strip()

    if not pergunta:
        await message.channel.send("❓ Digite uma pergunta após o `!`. Ex: `!O que é a Auvo?`")
        return

    # Avisa que está processando
    await message.channel.send("⏳ Consultando a base de conhecimento...")

    # Envia para o n8n
    try:
        async with aiohttp.ClientSession() as session:
            payload = {
                "pergunta": pergunta,
                "autor": str(message.author),
                "canal": str(message.channel)
            }
            async with session.post(N8N_WEBHOOK_URL, json=payload) as resp:
                if resp.status == 200:
                    print(f"✅ Pergunta enviada ao n8n: {pergunta}")
                else:
                    await message.channel.send("⚠️ Erro ao consultar a base. Tente novamente.")
                    print(f"❌ Erro n8n: {resp.status}")
    except Exception as e:
        await message.channel.send("⚠️ Erro de conexão. Tente novamente.")
        print(f"❌ Exceção: {e}")

client.run(DISCORD_TOKEN)
