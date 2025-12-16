import requests, time

def ghost_pool():
    print("Base — Ghost Pool Reviver (zero volume for days → sudden buys)")
    # pair → last_volume_time
    ghosts = {}

    while True:
        try:
            r = requests.get("https://api.dexscreener.com/latest/dex/pairs/base")
            now = time.time()

            for pair in r.json().get("pairs", []):
                addr = pair["pairAddress"]
                vol24 = pair.get("volume", {}).get("h24", 0) or 0
                age_days = (now - pair.get("pairCreatedAt", 0) / 1000) / 86400

                if age_days < 3: continue  # too young

                if addr not in ghosts:
                    if vol24 < 100:
                        ghosts[addr] = now  # mark as ghost if dead
                    continue

                silence_days = (now - ghosts[addr]) / 86400
                if silence_days > 3 and vol24 > 20_000:
                    token = pair["baseToken"]["symbol"]
                    print(f"GHOST POOL AWAKENED\n"
                          f"{token} dead for {silence_days:.1f} days\n"
                          f"Sudden ${vol24:,.0f} volume\n"
                          f"https://dexscreener.com/base/{addr}\n"
                          f"→ Zombie revival — coordinated pump or real interest?\n"
                          f"{'GHOST'*30}")
                    del ghosts[addr]

                if vol24 > 1000:
                    ghosts[addr] = now  # still alive

        except:
            pass
        time.sleep(12)

if __name__ == "__main__":
    ghost_pool()
