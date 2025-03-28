import aiohttp
import os
from dotenv import load_dotenv


<<<<<<< HEAD
load_dotenv()


RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")  # Clé d'API RapidAPI
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")  # Hôte RapidAPI

HEADERS = {
    'x-rapidapi-key': RAPIDAPI_KEY,
    'x-rapidapi-host': RAPIDAPI_HOST,
}
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
=======
load_dotenv() 
import aiohttp

>>>>>>> sauvegarde-commits
async def check_ban(uid):
    api_url = f"https://api.paulalfredo.me/check_ban/{uid}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status != 200:
                    return None

                response_data = await response.json()
                if response_data.get("status") == 200:
<<<<<<< HEAD
                    is_banned = response_data.get("data", {}).get("is_banned", 0)
                    return is_banned != 0
                else:
                    return None
    except Exception as e:
        print(f"Erreur API : {e}")
        return None

=======
                    data = response_data.get("data")

                    return {
                        "is_banned": data.get("is_banned", 0),
                        "nickname": data.get("nickname", ""),
                        "period": data.get("period", 0),
                        "region": data.get('region',0 )
                    }
                else:
                    return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
>>>>>>> sauvegarde-commits
