import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask
import threading
from utils import check_ban

# Initialisation de Flask
app = Flask(__name__)


load_dotenv()
APPLICATION_ID = os.getenv("APPLICATION_ID")
TOKEN = os.getenv("TOKENN")


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


nomBot = "None"

# Route Flask pour afficher l'état du bot
@app.route('/')
def home():
    global nomBot
    return f"Bot {nomBot} is working"


def run_flask():
    app.run(host='0.0.0.0', port=10000)


threading.Thread(target=run_flask).start()


@bot.event
async def on_ready():
    global nomBot
    nomBot = f"{bot.user}"
    print(f"Le bot est connecté en tant que {bot.user}")


@bot.command(name="ID")
async def check_ban_command(ctx):
    content = ctx.message.content
    user_id = content[3:].strip()

    # Vérification si l'ID est un nombre
    if not user_id.isdigit():
        await ctx.send(
            f"{ctx.author.mention} ❌ **UID invalide !**\n➡️ Veuillez fournir un UID valide sous la forme : `!ID 123456789`")
        return

    try:
        ban_status = await check_ban(user_id)
    except Exception as e:
        await ctx.send(f"{ctx.author.mention} ⚠️ **Erreur lors de la vérification :**\n```{str(e)}```")
        return

    if ban_status is None:
        await ctx.send(
            f"{ctx.author.mention} ❌ **Impossible d'obtenir les informations.**\nVeuillez réessayer plus tard.")
        return

 
    is_banned = int(ban_status.get("is_banned", 0))
    period = ban_status.get("period", "N/A")
    
    id = f"`{user_id} `"


    if isinstance(period, int):
        period_str = f"` plus de {period} mois`"
    else:
        period_str = " indisponible"

    embed = discord.Embed(
        color=0xFF0000 if is_banned else 0x00FF00,
        timestamp=ctx.message.created_at
    )
    
    if is_banned:
        embed.title = "**▌ Compte banni 🛑 **\n"             
        embed.description = (
                            f"•**Ce compte a été confirmé comme utilisant des hacks.**\n."
                            f"•**Durée de la suspension : {period_str}**\n" + \
                            f"•**ID du joueur : `{id}`**\n")
        embed.set_image(url="https://i.ibb.co/tDnbYrK/standard-1.gif")
    else:
        embed.title = "**▌ Compte non banni ✅ **\n"
        embed.description =(f"•**Aucune preuve suffisante pour confirmer l'utilisation de hacks sur ce compte.**\n"+ \
                            f"•**ID du joueur : `{id}`**\n")
        embed.set_image(url="https://i.ibb.co/CshJSf8/standard-2.gif")

    embed.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
    embed.set_footer(text="📌 Check ban free fire")

    await ctx.send(f"{ctx.author.mention}", embed=embed)


bot.run(TOKEN)
