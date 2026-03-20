import discord
import aiohttp
import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
PREFIXO = "!"

CANAIS = {
    1341388033584267319: {
        "n8n": os.getenv("WEBHOOK_N8N_FINANCEIRO", "https://vitorpomodoro.app.n8n.cloud/webhook/auvo-bot"),
        "discord": "https://discord.com/api/webhooks/1481657595667415274/q_U8HYZNJUS59KFG05YGls1xY9oISEKuQfHe1o6NoTYGk-uZxwhCT-3dlT65cJjdFj_B",
        "nome": "financeiro"
    },
    1484613247326879947: {
        "n8n": os.getenv("WEBHOOK_N8N_ENABLEMENT", "https://vitorpomodoro.app.n8n.cloud/webhook/enablement"),
        "discord": "https://discord.com/api/webhooks/1484613269808349214/y_v4EQExz6Y_BevuNU77-DaLol2J6Gk5E8bCW7mDGPeK39JAyFPtFPsRA3k6nlQQ_IzM",
        "nome": "enablement"
    },
    1484613476411510825: {
        "n8n": os.getenv("WEBHOOK_N8N_ACOMPANHAMENTO", "https://vitorpomodoro.app.n8n.cloud/webhook/acompanhamento"),
        "discord": "https://discord.com/api/webhooks/1484613495260446730/e7dmRytsqZVhMji7oKwYkJn8NRgXnIOjmc0iam3dXcVY6YSsRmTHpQ7aepgM-pbmQeTz",
        "nome": "acompanhamento"
    },
}

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Bot conectado como {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    canal = CANAIS.get(message.channel.id)
    if not canal:
        return

    if not message.content.startswith(PREFIXO):
        return

    pergunta = message.content[len(PREFIXO):].strip()
    if not pergunta:
        await message.channel.send("❓ Digite uma pergunta após o `!`. Ex: `!O que é a Auvo?`")
        return

    await message.channel.send("⏳ Consultando a base de conhecimento...")

    try:
        async with aiohttp.ClientSession() as session:
            payload = {
                "body": {
                    "pergunta": pergunta
                }
            }

            async with session.post(canal["n8n"], json=payload, timeout=30) as resp:
                if resp.status == 200:
                    print(f"✅ [{canal['nome']}] Pergunta enviada: {pergunta}")
                else:
                    await message.channel.send("⚠️ Erro ao consultar a base. Tente novamente.")
                    print(f"❌ [{canal['nome']}] Erro n8n: {resp.status} - {await resp.text()}")

    except Exception as e:
        await message.channel.send("⚠️ Erro de conexão. Tente novamente.")
        print(f"❌ [{canal['nome']}] Exceção: {e}")

client.run(DISCORD_TOKEN)
