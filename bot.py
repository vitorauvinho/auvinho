import discord
import aiohttp
import os

# ============================================================
# CONFIGURAÇÕES — valores vêm das variáveis de ambiente
# ============================================================
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")
CANAL_ID = int(os.getenv("CANAL_ID", "1341388033584267319"))
PREFIXO = "!"
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
                "body": {
                    "pergunta": pergunta
                }
            }
            
            async with session.post(N8N_WEBHOOK_URL, json=payload, timeout=30) as resp:
                if resp.status == 200:
                    print(f"✅ Pergunta enviada ao n8n: {pergunta}")
                else:
                    await message.channel.send("⚠️ Erro ao consultar a base. Tente novamente.")
                    print(f"❌ Erro n8n: {resp.status} - {await resp.text()}")
                    
    except Exception as e:
        await message.channel.send("⚠️ Erro de conexão. Tente novamente.")
        print(f"❌ Exceção: {e}")

client.run(DISCORD_TOKEN)
```

### 3️⃣ Confirmar Variáveis no Railway

As variáveis já estão configuradas no Railway (você me mostrou antes):
- ✅ `DISCORD_TOKEN` 
- ✅ `N8N_WEBHOOK_URL`
- ✅ `CANAL_ID`

Então o código vai funcionar, pegando os valores de lá!

### 4️⃣ Fazer o Commit Seguro

Agora sim, faça o commit no GitHub:
1. Cole o código corrigido (sem tokens)
2. Mensagem do commit: `"Corrige payload e remove tokens expostos"`
3. **Clique em "Commit changes"**
4. O GitHub não vai mais reclamar! ✅

### 5️⃣ Aguardar Deploy

O Railway vai detectar o commit e fazer redeploy automático (2-3 minutos).

---

## 🧪 Depois do Deploy, Teste:

No Discord:
```
!Quem está inadimplente?
