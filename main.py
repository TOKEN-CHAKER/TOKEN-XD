import requests
import time

def extract_eaag_token(cookie):
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Cookie': cookie
    }
    response = requests.get('https://business.facebook.com/business_locations/', headers=headers)
    eaag = None
    if 'EAAG' in response.text:
        start = response.text.find('EAAG')
        end = response.text.find('"', start)
        eaag = response.text[start:end]
    return eaag

def convert_to_eaad(eaag):
    url = 'https://graph.facebook.com/v19.0/oauth/access_token'
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': '124024574287414',  # Valid client_id
        'client_secret': 'dd5b2e83c77b2b2e90e8b4f7d9d85eaf',  # Valid secret
        'fb_exchange_token': eaag
    }
    response = requests.get(url, params=params)
    if response.status_code == 200 and 'access_token' in response.json():
        return response.json()['access_token']
    else:
        print("[ERROR] Failed to convert EAAG to EAAD")
        print(response.text)
        return None

# Put your real Facebook cookie here
cookie = "YOUR_FACEBOOK_COOKIE_HERE"

print("[INFO] Attempt 1 to generate token...")
print("[INFO] Fetching cookie EAAG token...")

eaag_token = extract_eaag_token(cookie)
if eaag_token:
    print("[SUCCESS] EAAG token fetched successfully!")
    print("🌐 ── Tool Running📶 ────────────────────── 🔑")
    print("wait 10 second don't use Ctrl+Z/C, terminal is running process")
    time.sleep(10)
    print("🌐 ── Requesting initial access token...")

    eaad_token = convert_to_eaad(eaag_token)
    if eaad_token:
        print("✅ [SUCCESS] EAAD Token Generated:")
        print(eaad_token)
    else:
        print("❌ [ERROR] Failed to convert to EAAD.")
else:
    print("❌ [ERROR] Invalid or expired Facebook cookie.")
