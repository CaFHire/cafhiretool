import json

CONFIG_PATH = os.path.join("utils", "config.json")
PROXY_PATH = os.path.join("utils", "proxy.txt")

def load_config():
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w") as f:
            json.dump({"use_proxy": False}, f, indent=4)
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

def load_proxies():
    if not os.path.exists(PROXY_PATH):
        return []
    with open(PROXY_PATH, "r") as f:
        return [line.strip() for line in f if line.strip()]

def settings_menu():
    config = load_config()
    proxies = load_proxies()
    while True:
        clear()
        print_banner()
        print(f"{Fore.CYAN}Settings Menu:")
        print(f"{Fore.LIGHTWHITE_EX}1. Use Proxy: {Fore.YELLOW}{config.get('use_proxy', False)}")
        print(f"{Fore.LIGHTWHITE_EX}2. Loaded Proxies: {Fore.YELLOW}{len(proxies)} found")
        print(f"{Fore.LIGHTWHITE_EX}3. Back to main menu")

        choice = input(f"\n{Fore.LIGHTMAGENTA_EX}Select option to toggle (1-3): {Style.RESET_ALL}")
        if choice == "1":
            config["use_proxy"] = not config.get("use_proxy", False)
            save_config(config)
            print(f"{Fore.GREEN}[✓] use_proxy set to {config['use_proxy']}")
            time.sleep(1)
        elif choice == "2":
            print(f"{Fore.LIGHTBLUE_EX}Proxies:")
            for proxy in proxies:
                print(f" - {proxy}")
            input(f"{Fore.LIGHTMAGENTA_EX}\nPress Enter to return...")
        elif choice == "3":
            break
        else:
            print(Fore.RED + "[!] Invalid choice")
            time.sleep(1)
