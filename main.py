import requests, re, time

def style(text, color="cyan"):
    colors = {
        "green": "\033[1;32m",
        "cyan": "\033[1;36m",
        "blue": "\033[1;34m",
        "red": "\033[1;31m",
        "reset": "\033[0m",
        "yellow": "\033[1;33m",
        "magenta": "\033[1;35m"
    }
    return f"{colors.get(color, '')}{text}{colors['reset']}"

def print_intro():
    print(style("\nEnter Facebook cookie:", "yellow"))

def fetch_eaag(cookie):
    print(style("\n[INFO] Attempt 1 to generate token...", "cyan"))
    print(style("[INFO] Fetching coockie EAAG token...", "cyan"))

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; Mobile)",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": cookie
    }
    try:
        res = requests.get("https://business.facebook.com/business_locations", headers=headers)
        token_match = re.search(r"EAAG\w+", res.text)
        if token_match:
            print(style("\n[SUCCESS] fb cookie!\n", "green"))
            return token_match.group()
        else:
            print(style("[ERROR] EAAG token not found!", "red"))
            return None
    except Exception as e:
        print(style(f"[ERROR] {e}", "red"))
        return None

def convert_to_eaad(eaag):
    print(style(" 🌐 ── Tool Running📶 ────────────────────── 🔑", "cyan"))
    print(style("wait 10 second dont use ctrl Z/C terminal is running prosses", "red"))
    time.sleep(3)
    print(style(" 🌐 ── Tool Running📶 ────────────────────── 🔑", "cyan"))

    print(style("\n[INFO] Requesting initial access token...", "cyan"))
    url = "https://graph.facebook.com/v19.0/oauth/access_token"
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': '6628568379',
        'client_secret': '62f8ce9f74b12f84c123cc23437a4a32',
        'fb_exchange_token': eaag
    }
    res = requests.get(url, params=params)
    if "access_token" in res.text:
        print(style("[SUCCESS] Initial access token fetched!", "green"))
        print(style("\n[INFO] Converting EAAG TO EAAB", "cyan"))
        eaad = res.json()["access_token"]
        print(style("\n[SUCCESS] EAAB TO token: EAAD\n", "green"))
        print(style("[✓] Successfully Token Generated: ", "green") + eaad + "\n")
        return eaad
    else:
        print(style("[ERROR] Failed to convert EAAG to EAAD", "red"))
        return None

if __name__ == "__main__":
    print_intro()
    cookie = input("> ").strip()
    if not cookie or "sb=" not in cookie:
        print(style("[ERROR] Invalid cookie format. Must contain sb=", "red"))
    else:
        eaag = fetch_eaag(cookie)
        if eaag:
            convert_to_eaad(eaag)
