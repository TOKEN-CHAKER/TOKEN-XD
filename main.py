import requests
import re
import time
import sys

def print_banner():
    print("""
\033[1;32m
════════════════════════════════════════════
🔐 Broken Nadeem | FB EAAD Token Extractor 🔓
════════════════════════════════════════════
\033[0m
""")

def extract_eaag(cookie):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Mobile)',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cookie': cookie
    }

    print("🔁 [INFO] Token निकालने की कोशिश हो रही है...")
    try:
        res = requests.get('https://business.facebook.com/business_locations', headers=headers)
        eaag = re.search(r'EAAG\w+', res.text)
        if eaag:
            token = eaag.group()
            print(f"✅ [EAAG Token]: {token[:30]}... 🔥")
            return token
        else:
            print("❌ EAAG टोकन नहीं मिला। Cookie सही नहीं या expired है।")
            return None
    except Exception as e:
        print(f"[ERROR] {e}")
        return None

def convert_to_eaad(eaag_token):
    print("🔁 [INFO] EAAG से EAAD token generate कर रहे हैं...")
    url = f"https://graph.facebook.com/v19.0/oauth/access_token"
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': '6628568379',
        'client_secret': '62f8ce9f74b12f84c123cc23437a4a32',
        'fb_exchange_token': eaag_token
    }

    try:
        res = requests.get(url, params=params)
        if 'access_token' in res.text:
            eaad = res.json()['access_token']
            print(f"\n✅ [EAAD Token Generated Successfully] 🔐\n\n{eaad}\n")
            return eaad
        else:
            print("❌ EAAD token नहीं बना। शायद token expire या invalid है।")
            return None
    except Exception as e:
        print(f"[ERROR] {e}")
        return None

if __name__ == "__main__":
    print_banner()
    fb_cookie = input("🔐 Facebook Cookie डालो (sb=... से शुरू):\n> ").strip()
    
    if not fb_cookie or not "sb=" in fb_cookie:
        print("⚠️ सही Cookie दो। Cookie sb= से शुरू होती है।")
        sys.exit()

    eaag_token = extract_eaag(fb_cookie)
    if eaag_token:
        convert_to_eaad(eaag_token)
