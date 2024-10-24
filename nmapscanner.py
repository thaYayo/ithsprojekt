import argparse
import nmap
import pprint
import os
import json 
## ips for scanning 45.33.32.156 176.28.50.165
## Detta script har endast testats på Windows 10
## Jag är den enda som har arbetat på denna script

def main():
    parser = argparse.ArgumentParser(description="nmap portscanner")
    parser.add_argument("-v", "--verbose", action="store_true", help="Visar utökad info")

    subparsers = parser.add_subparsers(dest='command')

    scan_ip = subparsers.add_parser("scan", help= 'scannar ipadress/er.')
    scan_ip.add_argument("ip", type=str, help="Ange ipadress/er som ska skannas", nargs = '+')
    scan_ip.add_argument("-s","--save", help="sparar resultat av scan till json fil | scan <ipadress/er> -s <fil namn>" )
    scan_ip.add_argument("-p","--port",type=str, help="ange portar som önskas skanna | scan <ipadress/er> -p <port>" )


    read_file = subparsers.add_parser("read", help="läser ip adresser från fil")
    read_file.add_argument("file", help="ange fil som ska läsas")

    args = parser.parse_args()

    if args.command == "scan":
        if args.port:
            resultat = scan_host(args.ip, args.port)
        if args.save:
            create_file_json(args.save,resultat)
        else:
            resultat = scan_host(args.ip)
        pprint.pprint(resultat)

    if args.command == "read":
        läs_result = scan_fil(args.file)
        pprint.pprint(läs_result)



# function för att skanna ipadresser.
def scan_host(ipadress, port=None):
    #dictionary för att spara resultat av skannen
    result = {}

    nm = nmap.PortScanner()
    # for loop för att skanna varenda ipadress som användaren skriver då split() functionen delar in 1 sträng till en lista med flera element med avskiljaren som man anger inom ()
    for ip in ipadress:
        #spara resultatet i en variabel så att man kan använda den senare
        if port:
            scan_result = nm.scan(ip,f"-p {port}")
            result = scan_result
        else:
            scan_result = nm.scan(ip)
            result[ip] = scan_result["scan"][ip]['tcp']
        # Ger resualt dict ip adress som key och scan_result som value
        # for loop för att ta bort services delen av skannen då den bara överflödig info. ipadresser får alla keys och scanresult lagrar alla values i result dict
        # result[ip]["nmap"]['scaninfo']['tcp'].pop("services")

    return result

def create_file_json(filename,resultat):
## funktion för att skapa .json fil med resultat av skanning
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            file.write(json.dumps(resultat, sort_keys=True, indent=4))
        print(f"File was created: {filename} \n")
    else:
        print(f"File already exists: {filename} \n")

def scan_fil(filename):
    ## läsa av innehåll av fil vars innehåll ska användas som ip adresser för skanning
    ## kan endast läsa av filer i samma folder
    file_result = []
    with open(filename, "r") as file:
        for files in file:
            file_result.append(files.strip())
            resultat = scan_host(file_result)
        return resultat


if __name__ == "__main__":
    main()


# def main():

#     while True:
#         #startmeny
#         print("1. Skanna IP-adresser")
#         print("2. Skanna ip adress(er) från fil")
#         print("3. Spara resultat av skanning som .txt fil")
#         print("4. Spara resultat av skanning som json fil")
#         print("5. Avsluta program")
#         print("")

#         choice = input("Ange val: ")

#         if choice == '1':
#             ipadress = input("Ange IP-adress(er) som önskas skanna (separera adresserna med ','): ").split(",")
#             global resultat
#             resultat = scan_host(ipadress)
#             pprint.pprint(resultat)
#         elif choice == '2':
#             filnamn = input("Ange fil: ")
#             resultat = läs_fil(filnamn)
#             pprint.pprint(resultat)
#         elif choice == '3':
#             filename = input("Ange filnamn: ")
#             create_txtfile(filename)
#         elif choice == '4':
#             json_filename = input("Ange filnamn: ")
#             create_file_json(json_filename)
#         elif choice == '5':
#             break