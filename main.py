import os
import time
import importlib.util
from colorama import Fore, Style, init
from utils import checkforupdates
checkforupdates.check_for_all_updates()

init(autoreset=True)

menu_options = [
    "Check for Updates",
    "Settings",
    "Token Joiner / Leaver",
    "Token Checker",
    "Token Boost Sender",
    "Token Channel Spammer",
    "Token Nickchanger",
    "URL Sniper",
    "Server Cloner",
    "Email Cloner",
    "Token Voice Joiner",
    "Token Onliner",
    "Message Spammer"
]

colors = [
    Fore.LIGHTRED_EX,
    Fore.LIGHTGREEN_EX,
    Fore.LIGHTYELLOW_EX,
    Fore.LIGHTBLUE_EX,
    Fore.LIGHTMAGENTA_EX,
    Fore.LIGHTCYAN_EX,
    Fore.RED,
    Fore.GREEN,
    Fore.YELLOW,
    Fore.BLUE,
    Fore.MAGENTA,
    Fore.CYAN,
    Fore.WHITE
]

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def print_banner():
    ascii_banner = f"""{Fore.MAGENTA}
   ██████╗ █████╗ ███████╗██╗  ██╗██╗██╗██████╗ ███████╗
  ██╔════╝██╔══██╗╚══███╔╝██║  ██║██║██║██╔══██╗██╔════╝
  ██║     ███████║  ███╔╝ ███████║██║██║██████╔╝█████╗  
  ██║     ██╔══██║ ███╔╝  ██╔══██║██║██║██╔═══╝ ██╔══╝  
  ╚██████╗██║  ██║███████╗██║  ██║██║██║██║     ███████╗
   ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝╚═╝     ╚══════╝
{Style.RESET_ALL}"""
    print(ascii_banner)

def main_menu():
    clear()
    print_banner()
    print(f"{Fore.LIGHTWHITE_EX}╔══════════════════════════════════════════════════╗")
    print(f"{Fore.LIGHTWHITE_EX}║                  Discord Tool Menu              ║")
    print(f"{Fore.LIGHTWHITE_EX}╠══════════════════════════════════════════════════╣")
    for idx, option in enumerate(menu_options, 1):
        color = colors[idx % len(colors)]
        print(f"{color}║ {str(idx).rjust(2)}. {option.ljust(44)}║")
    print(f"{Fore.LIGHTWHITE_EX}╚══════════════════════════════════════════════════╝")
    return input(f"{Fore.LIGHTMAGENTA_EX}Enter your choice (1-13): {Style.RESET_ALL}")

def run_module(option_name):
    filename = option_name.replace(" ", "").replace("/", "").lower() + ".py"
    path = os.path.join("utils", filename)

    if os.path.isfile(path):
        spec = importlib.util.spec_from_file_location("module.name", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    else:
        print(Fore.RED + f"\n[ERROR] Module '{filename}' not found in utils/")
        time.sleep(2)

if __name__ == "__main__":
    while True:
        choice = main_menu()
        if choice.isdigit() and 1 <= int(choice) <= len(menu_options):
            selected_option = menu_options[int(choice) - 1]
            run_module(selected_option)
        else:
            print(Fore.RED + "\n[!] Invalid choice!")
            time.sleep(1)
