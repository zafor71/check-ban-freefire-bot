import discord
import aiohttp
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from utils import check_ban , get_player_info , get_player_info_global

APPLICATION_ID = os.getenv("APPLICATION_ID")  # ID de 
TOKEN = os.getenv("TOKEN")  # Token du bot
MY_ID = os.getenv("MY_ID")
MY_ID_INT = int(MY_ID)

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Le bot est connecté en tant que {bot.user}")
    await bot.tree.sync()

# Commande pour afficher les guildes où le bot est présent
@bot.tree.command(name="guild_list", description="Affiche la liste des serveurs où le bot est ajouté.")
async def guild_list_command(interaction: discord.Interaction):
    # Afficher l'ID de l'utilisateur pour débogage
    print(f"ID de l'utilisateur qui a exécuté la commande : {interaction.user.id}")
    
    if interaction.user.id != MY_ID_INT:
        await interaction.response.send_message("❌ Vous n'avez pas la permission d'exécuter cette commande.")
        return

    guild_names = [guild.name for guild in bot.guilds]
    if not guild_names:
        await interaction.response.send_message("Le bot n'est ajouté dans aucun serveur.")
        return

    guild_list = "\n".join(guild_names)
    await interaction.response.send_message(f"Les serveurs où le bot est ajouté sont :\n{guild_list}")

    
@bot.tree.command(name="get_info", description="Obtenez des informations sur un joueur de Free Fire.")
@app_commands.describe(uid="UID à vérifier")
async def get_info_command(interaction: discord.Interaction, uid: str):
    await interaction.response.defer()  # Différer la réponse pour éviter les timeouts
    data_info = await get_player_info(uid)
    # Vérifier s'il y a une erreur
    if 'error' in data_info:
        await interaction.followup.send(f"❌ {data_info['error']}")
        return
    embed = discord.Embed(
        title="📜 Informations du joueur",
        description=f"""
**👤 COMPTE**
───────────────
🔹 **Pseudo:** {data_info['nickname']}
🔹 **UID:** {data_info['accountId']}
🔹 **Niveau:** {data_info['level']}
🔹 **Région:** {data_info['region']}
🔹 **Likes:** {data_info['liked']}
🔹 **Dernière connexion:** <t:{data_info['lastLoginAt']}:R>
🔹 **Signature:** {data_info['socialInfo']}

**🛡️ GUILDE**
───────────────
🏆 **Nom de la guilde:** {data_info['clanName']}
🆔 **ID de guilde:** {data_info['clanId']}
🔺 **Niveau de guilde:** {data_info['clanLevel']}
👥 **Membres actifs:** {data_info['memberNum']} / {data_info['capacity']}

**👑 Chef de Guilde**
───────────────
🎖️ **Pseudo du leader:** {data_info['nicknameChef']}
🆔 **UID du leader:** {data_info['clanCaptainId']}
🏅 **Niveau du leader:** {data_info['levelChef']}
⏳ **Dernière connexion:** <t:{data_info['lastLoginChef']}:R>

🔗 **Suivez l'admin (Hi Fredo)**
───────────────
📱 [Tiktok](https://www.tiktok.com/@thug.4ff)
🌐 [Site Web](https://free-fire-info.vercel.app/)
        """,
        color=0x0099ff,
        timestamp=discord.utils.utcnow(),
    )
    if data_info['avatar_image_url']:
        embed.set_image(url=data_info['avatar_image_url'])
    await interaction.followup.send(embed=embed)
@bot.tree.command(name="check_ban", description="Vérifier si un joueur est banni.")
@app_commands.describe(uid="UID du joueur à vérifier")
async def check_ban_command(interaction: discord.Interaction, uid: str):
    await interaction.response.defer()

    if not uid.isdigit() or len(uid) < 6:
        await interaction.followup.send("❌ **UID invalide.** Veuillez fournir un UID valide.")
        return

    try:

        global_info = await get_player_info_global(uid)
        if 'error' in global_info:
            await interaction.followup.send(f"❌ **Erreur :** {global_info['error']}")
            return
        ban_status = await check_ban(uid)
    except Exception as e:
        await interaction.followup.send(f"❌ **Une erreur est survenue :** {str(e)}")
        return

    if ban_status is None:
        await interaction.followup.send("❌ **Erreur lors de la vérification du bannissement.**")
        return

    embed = discord.Embed(
        title="🔍 Vérification de Bannissement",
        color=0xFF0000 if ban_status else 0x00FF00,  # Rouge si banni, vert sinon
    )

    if ban_status:
        embed.description = f"🚨 **Le compte de  {global_info['username']} ({uid}) est __BAN PERMANENT__ !**"
        embed.set_image(url="https://i.imgur.com/7DG7wIt.png")
    else:
        embed.description = f"✅ **Le compte de {global_info['username']} ({uid}) n'est PAS banni !**"
        embed.set_image(url="https://i.imgur.com/NGctM3a.jpeg")

    embed.set_footer(text="🔄 Données mises à jour en temps réel")
    await interaction.followup.send(embed=embed)

# Lancer le bot
bot.run(TOKEN)