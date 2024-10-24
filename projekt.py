# Toolbox
# Bygg en toolbox bestående av flera Python-script som kan användas för penetrationstester eller inom IT-säkerhet.

# Använd dig av de tekniker och paket som vi gått igenom under kursen eller kunskap du har sedan tidigare.


# Krav för varje verktyg:
# Verktyget ska använda minst ett externt Python-bibliotek (t.ex. requests, shodan, cryptography, scapy, nmap osv).

# Verktyget ska använda argparse och kunna köras med argument från terminalen (undantag om verktyget inte behöver ta någon input från användaren)

# Verktyget ska innehålla en README-fil med instruktioner om hur verktyget används, exempelkörningar och kända begränsningar.


# För Godkänt krävs:
# Minst tre verktyg från olika kategorier (viktigt: Du får använda dina verktyg från laborationerna. Men se till att de följer kraven för uppgiften)

# Verktygen ska innehålla tydliga instruktioner för användning

# Koden ska innehålla grundläggande felhantering (t.ex. try-except), inmatningsvalidering och vara strukturerad i funktioner.


# För Väl godkänt:
# Inkludera ytterligare/mer avancerade funktioner såsom logging, rapportgenerering eller ett mainscript som importerar de andra skripten och interaktivt låter användaren köra dem

# Implementera fler än tre verktyg för att visa din kunskap av fler Python-paket

# Verktygen ska vara väl dokumenterade
import subprocess
import nmapscanner
import hashtool
import crypto_tool

def menu():
    menu_dict = {
        "1": "nmap Portscanner",
        "2": "hashTool",
        "3":"cryptool"
    }

    for keys,values in menu_dict.items():
        print(f"{keys}. {values}")

    choice: str = input("Ange val: ")

    if choice == "1":
        args = input("commands: ")
        nm_scan = subprocess.run(["python","nmapscanner.py", *args],
            capture_output=True
            # ,capture_stderr=True
            ,text=True, check=True)
        print(nm_scan.stdout)
    if choice == "2":
        print("hello")
        hashtool.main()
    if choice == "3":
        crypto_tool


menu()















# import keyboard
# import os
# import hashtool
# import labb1
# import crypto_tool

# def display_menu(selected):
#     os.system('cls' if os.name == 'nt' else 'cls')
#     print("Toolbox")
#     print(f"1. Encypt/Decrypt tool  {"<--" if selected == 1 else ''} ")
#     print(f"2. nmap portscanner  {"<--" if selected == 2 else ''}")
#     print(f"3. Verktyg som knäcker hashade lösenord  {"<--" if selected == 3 else ''}")
#     print(f"4. Exit {"<--" if selected == 4 else ''}")

# def main():
#     selected = 1

#     display_menu(selected)
#     while True:
#         if keyboard.is_pressed('down'):
#             selected = selected + 1 if selected < 4 else 1
#             while keyboard.is_pressed('down'):
#                 pass
#             display_menu(selected)

#         elif keyboard.is_pressed("up"):
#             selected = selected - 1 if selected > 1 else 4
#             while keyboard.is_pressed('up'):
#                 pass
#             display_menu(selected)
#         elif keyboard.is_pressed("enter"):
#             while keyboard.is_pressed('enter'):
#                 pass
#             os.system('cls' if os.name == 'nt' else 'cls')
#             if selected == 1:
#                 crypto_tool.main()
#             elif selected == 2:
#                 print("nmap")
#             elif selected == 3:
#                 print("hash verktyg")
#             elif selected == 4:
#                 print("exiting")
#                 break