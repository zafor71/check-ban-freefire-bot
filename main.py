import discord
import aiohttp
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv


load_dotenv()


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


APPLICATION_ID = os.getenv("APPLICATION_ID")  # ID de l'application du bot
TOKEN = os.getenv("TOKEN")  # Token du bot
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")  # Clé d'API RapidAPI
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")  # Hôte RapidAPI

HEADERS = {
    'x-rapidapi-key': RAPIDAPI_KEY,
    'x-rapidapi-host': RAPIDAPI_HOST,
}


@bot.event
async def on_ready():
    print(f"Le bot est connecté en tant que {bot.user}")
    await bot.tree.sync()


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

async def get_player_info(player_id):
    try:
        if not player_id.isdigit():
            return {'error': 'Player ID doit être un entier valide.'}

        url = f"https://id-game-checker.p.rapidapi.com/ff-player-info/{player_id}/SG"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=HEADERS) as response:
                if response.status != 200:
                    return {'error': f"Erreur API: {response.status}"}

                response_data = await response.json()
                status = response_data.get('status')

                if status == 200:
                    data = response_data.get('data', {})
                    basic_info = data.get('basicInfo', {})
                    clan_basic_info = data.get('clanBasicInfo', {}) if data.get('clanBasicInfo') else {}
                    captain_basic_info = data.get('captainBasicInfo', {}) if data.get('captainBasicInfo') else {}

                    profile_info = data.get('profileInfo', {})
                    clothes_info = profile_info.get('clothes', {})
                    avatar_images = clothes_info.get('images', [None])

                    social_info = data.get('socialInfo', {})

                    result = {
                        'accountId': basic_info.get('accountId', 'N/A'),
                        'nickname': basic_info.get('nickname', 'N/A'),
                        'region': basic_info.get('region', 'N/A'),
                        'level': basic_info.get('level', 'N/A'),
                        'lastLoginAt': basic_info.get('lastLoginAt', 'N/A'),
                        'liked': basic_info.get('liked', 'N/A'),
                        'socialInfo': social_info.get('signature', 'N/A'),
                        'avatar_image_url': avatar_images[0] if avatar_images else 'N/A',
                        'clanId': clan_basic_info.get('clanId', 'N/A'),
                        'clanName': clan_basic_info.get('clanName', 'N/A'),
                        'clanLevel': clan_basic_info.get('clanLevel', 'N/A'),
                        'memberNum': clan_basic_info.get('memberNum', 'N/A'),
                        'capacity': clan_basic_info.get('capacity', 'N/A'),
                        'nicknameChef': captain_basic_info.get('nickname', 'N/A'),
                        'levelChef': captain_basic_info.get('level', 'N/A'),
                        'clanCaptainId': captain_basic_info.get('accountId', 'N/A'),
                        'lastLoginChef': captain_basic_info.get('lastLoginAt', 'N/A'),
                    }

                    return result

                elif status == 404:
                    return {'error': 'UID introuvable'}

                else:
                    return {'error': f"Erreur API: {status}"}

    except Exception as e:
        return {'error': f"Une erreur s'est produite : {str(e)}"}

async def get_player_info_global(player_id):
    try:
        if not player_id.isdigit():
            return {'error': 'Player ID doit être un entier valide.'}

        url = f"https://id-game-checker.p.rapidapi.com/ff-global/{player_id}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=HEADERS) as response:
                if response.status != 200:
                    return {'error': f"Erreur API: {response.status}"}

                response_data = await response.json()
                status = response_data.get('status')

                if status == 200:
                    data = response_data.get('data', {})
                    result = {
                        "username": data.get('username', 'N/A'),
                    }
                    return result

                elif status == 404:
                    return {'error': 'UID introuvable'}

                else:
                    return {'error': f"Erreur API: {status}"}

    except Exception as e:
        return {'error': f"Une erreur s'est produite : {str(e)}"}

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


async def check_ban(uid):
    api_url = f"https://api.paulalfredo.me/check_ban/uid={uid}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status != 200:
                    return None

                response_data = await response.json()
                if response_data.get("status") == 200:
                    is_banned = response_data.get("data", {}).get("is_banned", 0)
                    return is_banned != 0
                else:
                    return None

    except Exception as e:
        print(f"Erreur API : {e}")
        return None

# Lancer le bot
bot.run(TOKEN)