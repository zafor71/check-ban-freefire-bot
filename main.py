# import discord
# import aiohttp
# import os
# from discord.ext import commands
# from discord import app_commands
# from dotenv import load_dotenv
# from utils import check_ban 

# APPLICATION_ID = os.getenv("APPLICATION_ID")  # ID de 
# TOKEN = os.getenv("TOKENN")  # Token du bot
# MY_ID = os.getenv("MY_ID")
# MY_ID_INT = int(MY_ID)

# load_dotenv()
# intents = discord.Intents.default()
# intents.message_content = True
# bot = commands.Bot(command_prefix="!", intents=intents)


# @bot.event
# async def on_ready():
#     print(f"Le bot est connecté en tant que {bot.user}")
#     await bot.tree.sync()


# @bot.command(name="ID")
# async def check_ban_command(ctx, uid: str):
#     # Vérification que l'UID commence par !ID sans espace
#     if not uid.startswith("ID") or len(uid) <= 4:
#         await ctx.send("❌ **Commande invalide.** Utilisez !ID<UID> pour vérifier un bannissement.")
#         return

#     # Extraire l'UID en supprimant le préfixe "ID"
#     uid = uid[2:].strip()

#     # Vérification de la validité de l'UID
#     if not uid.isdigit() or len(uid) < 6:
#         await ctx.send("❌ **UID invalide.** Veuillez fournir un UID valide.")
#         return

#     try:
#         # Vérification du bannissement via une fonction (remplacez `check_ban` par votre logique réelle)
#         ban_status = await check_ban(uid)
#     except Exception as e:
#         await ctx.send(f"❌ **Une erreur est survenue :** {str(e)}")
#         return

#     # Si le statut de bannissement est None, il y a eu une erreur dans la vérification
#     if ban_status is None:
#         await ctx.send("❌ **Erreur lors de la vérification du bannissement.**")
#         return

#     # Récupération des informations de ban
#     nickname = ban_status.get("nickname", "Inconnu")  # Nom du joueur (si disponible)
#     is_banned = int(ban_status.get("is_banned"))  # Statut du bannissement
#     periode = int(ban_status.get("periode"))  # Période du bannissement

#     # Formater la période pour afficher la durée de l'interdiction
#     if periode == 1:
#         periode_str = "plus de 1 mois"
#     elif periode == 2:
#         periode_str = "plus de 3 mois"
#     elif periode == 3:
#         periode_str = "plus de 6 mois"
#     elif periode == 4:
#         periode_str = "plus de 1 an"
#     else:
#         periode_str = f"{periode} jours"

#     # Création de l'embed
#     embed = discord.Embed(
#         title="🔍 Vérification de Bannissement",
#         color=0xFF0000 if is_banned else 0x00FF00,  # Rouge si banni, vert sinon
#     )

#     # Si le joueur est banni
#     if is_banned:
#         embed.description = f"• **Compte banni**. Durée de l'interdiction : {periode_str}\n" \
#                             f"**Pseudo** : {nickname}\n" \
#                             f"**UID** : {uid}"
#         embed.set_image(url="https://i.ibb.co/tDnbYrK/standard-1.gif")  # Image si banni
#     else:
#         embed.description = f"✅ **Le compte {nickname}** (UID **{uid}**) n'est __PAS BANNI__ !\n\n" \
#                             f"**Pseudo** : {nickname}\n" \
#                             f"**UID** : {uid}"
#         embed.set_image(url="https://i.ibb.co/CshJSf8/standard-2.gif")  # Image si non banni

#     # Footer avec une mise à jour en temps réel
#     embed.set_footer(text="🔄 Données mises à jour en temps réel")

#     # Envoi de l'embed à l'utilisateur
#     await ctx.send(embed=embed)

# bot.run(TOKEN)



import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from utils import check_ban

load_dotenv()
APPLICATION_ID = os.getenv("APPLICATION_ID")  # ID de l'application
TOKEN = os.getenv("TOKENN")  # Token du bot

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Le bot est connecté en tant que {bot.user}")

import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from utils import check_ban

load_dotenv()
APPLICATION_ID = os.getenv("APPLICATION_ID")  # ID de l'application
TOKEN = os.getenv("TOKENN")  # Token du bot

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Le bot est connecté en tant que {bot.user}")

@bot.command(name="ID")
async def check_ban_command(ctx):
    content = ctx.message.content
    user_id = content[3:].strip()

    # Vérification si l'ID est un nombre
    if not user_id.isdigit():
        await ctx.send(f"{ctx.author.mention} ❌ **UID invalide !**\n➡️ Veuillez fournir un UID valide sous la forme : `!ID 123456789`")
        return

    try:
        ban_status = await check_ban(user_id)
    except Exception as e:
        await ctx.send(f"{ctx.author.mention} ⚠️ **Erreur lors de la vérification :**\n```{str(e)}```")
        return

    if ban_status is None:
        await ctx.send(f"{ctx.author.mention} ❌ **Impossible d'obtenir les informations.**\nVeuillez réessayer plus tard.")
        return

    # Récupération des données avec des valeurs par défaut
    is_banned = int(ban_status.get("is_banned", 0))
    period = ban_status.get("period", "N/A")

    # Vérification et formatage de la durée du ban
    if isinstance(period, int):
        period_str = f"⏳ Plus de **{period}** mois"
    else:
        period_str = "⏳ Durée indisponible"

    # Création de l'embed
    embed = discord.Embed(
        title="🔍 Vérification du bannissement",
        color=0xFF0000 if is_banned else 0x00FF00,
        timestamp=ctx.message.created_at
    )

    if is_banned:
        embed.description = (
            f"🚫 **Ce compte est banni !**\n"
            f"🔢 **ID :** `{user_id}`\n"
            f"📅 **Durée :** {period_str}\n"
        )
        embed.set_image(url="https://i.ibb.co/tDnbYrK/standard-1.gif")
    else:
        embed.description = (
            f"✅ **Ce compte n'est pas banni !**\n"
            f"🔢 **ID :** `{user_id}`\n"
     
        )
        embed.set_image(url="https://i.ibb.co/CshJSf8/standard-2.gif")


    # Affichage de l'avatar de l'utilisateur en haut à droite
    embed.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

    # Footer amélioré
    embed.set_footer(text="📌 Garena Free Fire - Données mises à jour en temps réel")

    # Réponse avec mention + embed
    await ctx.send(f"{ctx.author.mention}", embed=embed)

bot.run(TOKEN)
